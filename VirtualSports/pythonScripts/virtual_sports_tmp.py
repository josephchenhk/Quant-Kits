# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:33:40 2017

@author: joseph.chen
"""
import json
import statsmodels.api as sm
import numpy as np
import csv

from mle import BirthProcess
from sql_connector import SQLConnector

class VirtualSports(object):
    
    def __init__(self):        
        self.sql = SQLConnector()
        self.lambda_k = []
        self.mu_k = []
        self.lambda_xy = []
        self.mu_xy = []
        self.lambda_t = []
        self.mu_t = []
        self.lambda_tt = []
        self.mu_tt = []
        self.pmatrix = []
             
    def close(self):
        self.sql.close()
        
    def get_params(self, league_id, home_team_id, away_team_id):
        # league parameters
        query = ("SELECT * " +
                 "FROM `inplay_league_params` " + 
                 "WHERE `league_id` = %s ")
        params = (league_id,)
        league_params = self.sql.execute(query,params)[0]
        league_id, gamma, lambda_, mu, rho, xi = league_params
        
        # home team parameters
        query = ("SELECT * " +
                 "FROM `inplay_team_params` " + 
                 "WHERE `league_id` = %s " +
                 "AND `team_id` = %s ")
        params = (league_id, home_team_id)
        home_params = self.sql.execute(query,params)[0]
        league_id, h_team_id, h_team_name, alpha_h, beta_h = home_params 
        
        # away team parameters
        params = (league_id, away_team_id)
        away_params = self.sql.execute(query,params)[0]
        league_id, a_team_id, a_team_name, alpha_a, beta_a = away_params 
        
        lambda_ = json.loads(lambda_)
        mu = json.loads(mu)
        rho = json.loads(rho)
        xi = json.loads(xi)
        
        return alpha_h, beta_h, alpha_a, beta_a, gamma, lambda_, mu, rho, xi
        
        
    def get_pmatrix(self, league_id, home_team_id, away_team_id, t, hg, ag):
        alpha_h, beta_h, alpha_a, beta_a, gamma, lambda_, mu, rho, xi = (
                self.get_params(league_id, home_team_id, away_team_id)
                )
        N = 10 # p-matrix dimension
        NTimeStep = 541
        p_matrix = np.zeros((N,N))
        p_matrix[hg][ag] = 1
        #timestamps = list(range(t,90*60,10)) # default time step = 10s
        timestamps = np.linspace(t,90*60,NTimeStep)
        timestamps = [t*1.0/90./60. for t in timestamps] # normalized timestamps
        p_matrix_T = self.cal_pmatrix2(timestamps, p_matrix, alpha_h, alpha_a, beta_h, beta_a, gamma, lambda_, mu, rho, xi, hg, ag)
        #print(self.pmatrix[0])
        #print(p_matrix_T)
        return p_matrix_T
         
    def cal_pmatrix(self, timestamps, p_matrix, alpha_h, alpha_a, beta_h, beta_a, gamma, lambda_params, mu_params, rho, xi,
                 score_x, score_y, N=10):
        for n in range(len(timestamps)-1):
            t0 = timestamps[n]
            t1 = timestamps[n+1]
            dt = t1-t0
            lambda_t0 = self.cal_lambda(t0, score_x, score_y, alpha_h, beta_a, gamma, lambda_params, rho, xi)
            mu_t0 = self.cal_lambda(t0, score_x, score_y, alpha_a, beta_h, 1.0, mu_params, rho, xi, False)
     
            p_matrix1 = np.roll(p_matrix,1,axis=0)

            p_matrix1[0] = np.zeros(N)  # p_matrix[i-1][j]
            p_matrix2 = np.roll(p_matrix,1,axis=1)
            p_matrix2[:,0] = np.zeros(N) # p_matrix[i][j-1]
            p_matrix = (lambda_t0*dt*(1-mu_t0*dt)*p_matrix1
                        + (1-lambda_t0*dt)*mu_t0*dt*p_matrix2
                        + (1-lambda_t0*dt)*(1-mu_t0*dt)*p_matrix
                        )
            adjust_factor = 1.0/sum(sum(p_matrix))
            p_matrix = adjust_factor*p_matrix
            if n<3:
                self.pmatrix.append(p_matrix)
        
        return p_matrix

    def cal_pmatrix2(self, timestamps, p_matrix, alpha_h, alpha_a, beta_h, beta_a, gamma, lambda_params, mu_params, rho, xi,
                 score_x, score_y, N=10):
        
        _upperScore_x = score_x + 1
        _upperScore_y = score_y + 1
        for n in range(len(timestamps)-1):
            t0 = timestamps[n]
            t1 = timestamps[n+1]
            dt = t1-t0
            lambda_t0 = self.cal_lambda(t0, score_x, score_y, alpha_h, beta_a, gamma, lambda_params, rho, xi)
            mu_t0 = self.cal_lambda(t0, score_x, score_y, alpha_a, beta_h, 1.0, mu_params, rho, xi, False)
     
#            p_matrix1 = np.roll(p_matrix,1,axis=0)
#
#            p_matrix1[0] = np.zeros(N)  # p_matrix[i-1][j]
#            p_matrix2 = np.roll(p_matrix,1,axis=1)
#            p_matrix2[:,0] = np.zeros(N) # p_matrix[i][j-1]
#            p_matrix = (lambda_t0*dt*(1-mu_t0*dt)*p_matrix1
#                        + (1-lambda_t0*dt)*mu_t0*dt*p_matrix2
#                        + (1-lambda_t0*dt)*(1-mu_t0*dt)*p_matrix
#                        )
            
            # Sth WRONG here.
#            for x in range(0,10):
#                for y in range(0,10):
#                    p_matrix[x][y] = p_matrix[x][y]*(1-lambda_t0[x][y]*dt)*(1-mu_t0[x][y]*dt)
#                    if x>score_x:
#                        p_matrix[x][y] += p_matrix[x-1][y]*lambda_t0[x][y]*dt*(1-mu_t0[x][y]*dt)
#                    if y>score_y:
#                        p_matrix[x][y] += p_matrix[x][y-1]*(1-lambda_t0[x][y]*dt)*mu_t0[x][y]*dt
            
            p_matrix0 = np.copy(p_matrix)
            for x in range(0,10):
                for y in range(0,10):
                    p_matrix[x][y] = p_matrix0[x][y]*(1-lambda_t0[x][y]*dt)*(1-mu_t0[x][y]*dt)
                    if x>score_x and x<=_upperScore_x:
                        p_matrix[x][y] += p_matrix0[x-1][y]*lambda_t0[x-1][y]*dt*(1-mu_t0[x-1][y]*dt)                        
                    if y>score_y and y<=_upperScore_y:
                        p_matrix[x][y] += p_matrix0[x][y-1]*(1-lambda_t0[x][y-1]*dt)*mu_t0[x][y-1]*dt
                        
            _upperScore_x += 1
            _upperScore_y += 1         
                    
#            if n==0:
#                print(p_matrix[0][0], p_matrix[0][1], p_matrix[1][0])                          
            
            if n==0:
                print("Before normalization: %s"%p_matrix[0][0])
            adjust_factor = 1.0/sum(sum(p_matrix))
            p_matrix = adjust_factor*p_matrix
            if n==0:
                print("After normalization: %s"%p_matrix[0][0])               
            if n<3:
                print(p_matrix[0][0], p_matrix[0][1], p_matrix[1][0])
                # WARN: need to copy the p_matrix, otherwise will modify it by mistake
                p_matrix_dump = np.copy(p_matrix)
                self.pmatrix.append(p_matrix_dump)
                self.lambda_tt.append(lambda_t0*dt)
                self.mu_tt.append(mu_t0*dt)
                #print(self.pmatrix[0])
        return p_matrix
    
    def cal_lambda(self, t, score_x, score_y, alpha_h, beta_a, gamma, lambda_params, rho, xi, is_home=True):
        
        def lambda_xy(x,y,lambda_params):
            '''parameter definition for given home goal(x) and away goal(y).
            Parameters
            ----------
            x: np.array([int])
                home current goal
            y: np.array([int])
                away current goal
            lambda_params: dict (length=6)
                6 parameters for lambda_{xy}. [lambda_{10}, lambda_{01}, 
                lambda_{11}, lambda_{22}, lambda_{21}, lambda_{12}]
                
            Returns
            -------
            lambda_: np.array()
                lambda_{xy} which depends on the current score. 
                (1) 1,            for x=0, y=0
                (2) lambda_{10},  for x=1, y=0
                (3) lambda_{01},  for x=0, y=1
                (4) lambda_{11},  for x=1, y=1
                (5) lambda_{22},  for x-y=0, x>=2, y>=2
                (6) lambda_{21},  for x-y>=1, x>=2
                (7) lambda_{12},  for x-y<=-1, y>=2
            '''
            num_params = len(lambda_params)
            if num_params==6:
                lambda_ = (((x==0) & (y==0))*1.0   
                         + ((x==1) & (y==0))*lambda_params[0] 
                         + ((x==0) & (y==1))*lambda_params[1] 
                         + ((x==1) & (y==1))*lambda_params[2] 
                         + ((x>=2) & (y>=2) & (x-y==0))*lambda_params[3]  
                         + ((x>=2) & (x-y>=1))*lambda_params[4]  
                         + ((y>=2) & (x-y<=-1))*lambda_params[5]) 
                return lambda_
            elif num_params==4:
                lambda_ = (((x==0) & (y==0))*1.0   
                         + ((x==1) & (y==0))*lambda_params[0] 
                         + ((x==0) & (y==1))*lambda_params[1] 
                         + ((x+y>1) & (x-y>=1))*lambda_params[2]
                         + ((x+y>1) & (x-y<=-1))*lambda_params[3])
                return lambda_
            elif num_params==2:
                lambda_ = (((x-y==0))*1.0   
                         + ((x-y>=1))*lambda_params[0]
                         + ((x-y<=-1))*lambda_params[1])
                return lambda_
            elif num_params==0:
                lambda_ = np.ones_like(x)
                return lambda_
            
        def lambda_t(t, lambda_, xi):
            return (lambda_ + xi*t)
        
        lambda_t_matrix = np.zeros((10,10))
        # WARN: score_x, score_y must not exceed 10 here.
        for x in range(score_x,10):
            for y in range(score_y,10):
                lambda_xy_ = lambda_xy(x, y,lambda_params)
                lambda_k_ = alpha_h * beta_a * gamma
                lambda_ = lambda_xy_*lambda_k_  # lambda_xy_ and lambda_k_ have been taken exponential to assure positiveness
                
                if len(rho)>0:
                    injury_time_home_effect = (
                                               ((t>(44.0/90.0)) & (t<=(45.0/90.0)))*rho[0]
                                               + ((t>(89.0/90.0)) & (t<=(90.0/90.0)))*rho[1] 
                                               + ((t<=(44.0/90.0)) | ((t>(45.0/90.0)) 
                                                                      & (t<=(89.0/90.0))))*1.0 
                                              )
                else:
                    injury_time_home_effect = 1.
                    
                if len(xi)>0 and is_home:
                    xi_1 = xi[0]
                elif len(xi)>0:
                    xi_1 = xi[1]
                else:
                    xi_1 = 0.
                       
                lambda_ = lambda_*injury_time_home_effect
                
    #            if is_home:
    #                self.lambda_k.append(lambda_k_)
    #                self.lambda_xy.append(lambda_xy_)
    #                self.lambda_t.append(lambda_)
    #                self.lambda_tt.append( lambda_t(t,lambda_,xi_1) )
    #            else:
    #                self.mu_k.append(lambda_k_)
    #                self.mu_xy.append(lambda_xy_)
    #                self.mu_t.append(lambda_)
    #                self.mu_tt.append( lambda_t(t,lambda_,xi_1) )
                    
                lambda_t_matrix[x][y] = lambda_t(t,lambda_,xi_1)
        
        return lambda_t_matrix
    

if __name__=="__main__":
    virtualSports = VirtualSports()
    #virtualSports.get_params(36,348,24)
    pmatrix = virtualSports.get_pmatrix(36,24,58,0,0,0)
    virtualSports.close()
    for n in range(3):
        np.savetxt("pmatrix_t"+str(n)+"_samples.csv",virtualSports.pmatrix[n],delimiter=",")
        np.savetxt("lambda_t"+str(n)+"_samples.csv",virtualSports.lambda_tt[n],delimiter=",")
        np.savetxt("mu_t"+str(n)+"_samples.csv",virtualSports.mu_tt[n],delimiter=",")
        
    np.savetxt("pmatrix_sample.csv", pmatrix, delimiter=",")
    
#    with open("inplay_params_samples.csv","w") as f:
#        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
#        wr.writerow(["lambda_k"]+virtualSports.lambda_k)
#        wr.writerow(["lambda_xy"]+virtualSports.lambda_xy)
#        wr.writerow(["lambda_t"]+virtualSports.lambda_t)
#        wr.writerow(["lambda_t*"]+virtualSports.lambda_tt)
#        wr.writerow("\n")
#        wr.writerow(["mu_k"]+virtualSports.mu_k)
#        wr.writerow(["mu_xy"]+virtualSports.mu_xy)
#        wr.writerow(["mu_t"]+virtualSports.mu_t)
#        wr.writerow(["mu_t*"]+virtualSports.mu_tt)