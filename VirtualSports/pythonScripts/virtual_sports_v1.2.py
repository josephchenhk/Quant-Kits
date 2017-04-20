# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 10:26:51 2017

@author: joseph.chen
"""
import time
import random
import json
import csv
import copy

#from mle import BirthProcess


class NumpyTools(object):
    
    def range(self, start, end, step):
        lst = [start]
        while True:
            element = lst[-1]+step
            if element>end:
                break
            else:
                lst.append(element)
        return lst
    
    def linspace(self, start, end, Nstep):
        step = (end-start)*1.0/(Nstep-1)
        lst = [start]
        while True:
            element = lst[-1]+step
            if element>end:
                break
            else:
                lst.append(element)
        return lst
    
    def zeros(self,dimension):
        if type(dimension)==int:
            return [0. for _ in range(dimension)]
        if type(dimension)==list or type(dimension)==tuple:
            N = len(dimension)
            if N==1:
                return [0. for _ in range(dimension[0])]
            else:
                inner_lst = [0. for _ in range(dimension[N-1])]
                for n in range(N-2,-1,-1):
                    lst = [inner_lst[:] for _ in range(dimension[n])]
                    inner_lst = lst[:]
                return lst
            
    def ones(self,dimension):
        if type(dimension)==int:
            return [1. for _ in range(dimension)]
        if type(dimension)==list or type(dimension)==tuple:
            N = len(dimension)
            if N==1:
                return [1. for _ in range(dimension[0])]
            else:
                inner_lst = [1. for _ in range(dimension[N-1])]
                for n in range(N-2,-1,-1):
                    lst = [inner_lst[:] for _ in range(dimension[n])]
                    inner_lst = lst[:]
                return lst
            
    def dimension(self, x):
        s = []
        while type(x)==list:
            N = len(x)
            s.append(N)
            x = x[0]
        return s
    
    def zeros_like(self, x):
        dimension = self.dimension(x)
        return self.zeros(dimension)
    
    def ones_like(self, x):
        dimension = self.dimension(x)
        return self.ones(dimension) 
    
    def multiply(self, a, arr):
        # TODO: can only handle 2D list now
        arr2 = arr[:]
        dimension = self.dimension(arr)
        if len(dimension)==1:
            for n in range(dimension[0]):
                arr2[n] = arr[n]*a
            return arr2
        elif len(dimension)==2:
            for n in range(dimension[0]):
                for m in range(dimension[1]):
                    arr2[n][m] = arr[n][m]*a
            return arr2
        
    def accumulate(self, lis):
        total = 0
        for x in lis:
            total += x
            yield total
        
        
        
            

            
        

class VirtualSports(object):
    
    def __init__(self, load_params="sql"):
        self.load_params = load_params
        if load_params=="sql":
            from sql_connector import SQLConnector
            self.sql = SQLConnector()
        self.np = NumpyTools()
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
        if self.load_params=="sql":
            self.sql.close()
        
    def get_params(self, league_id, home_team_id, away_team_id):
        if self.load_params=="sql":
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
            
            data = [alpha_h, beta_h, alpha_a, beta_a, gamma, lambda_, mu, rho, xi]
            with open("params.json","w") as f:
                json.dump(data,f)            
            return alpha_h, beta_h, alpha_a, beta_a, gamma, lambda_, mu, rho, xi
        elif self.load_params=="json":
            with open("params.json","r") as f:
                data = json.load(f)
            [alpha_h, beta_h, alpha_a, beta_a, gamma, lambda_, mu, rho, xi] = data
            return alpha_h, beta_h, alpha_a, beta_a, gamma, lambda_, mu, rho, xi
        
    def accumulate(self, lis):
        total = 0
        for x in lis:
            total += x
            yield total
     
#    def run_virtual_match(self,league_id, home_team_id, away_team_id, 
#                          kickoff_time=0, kickoff_hg=0, kickoff_ag=0,
#                          N_sim=1, NTimeStep = 540):
#        alpha_h, beta_h, alpha_a, beta_a, gamma, lambda_, mu, rho, xi = (
#                self.get_params(league_id, home_team_id, away_team_id)
#                )
#        
#        timestamps = self.np.linspace(kickoff_time,90*60,NTimeStep)
#        timestamps = [t*1.0/90./60. for t in timestamps] # normalized timestamps
#        
#        result_matrix = self.np.zeros((10,10))
#        for _ in range(N_sim):
#            if _%100==0:
#                print("Simulation {} finished.".format(_))
#            hg = kickoff_hg
#            ag = kickoff_ag
#            for n in range(len(timestamps)-1):
#                # TODO: Is it reasonable to accumulate exceptions to the last element?
##                hg = min(8,hg)
##                ag = min(8,ag)
#                
#                t0 = timestamps[n]
#                t1 = timestamps[n+1]
#                dt = t1-t0
#                lambda_t0 = self.cal_lambda(t0, hg, ag, alpha_h, beta_a, gamma, lambda_, rho, xi)
#                mu_t0 = self.cal_lambda(t0, hg, ag, alpha_a, beta_h, 1.0, mu, rho, xi, False)
#                p_homeScore = (lambda_t0[hg][ag]*dt) * (1-mu_t0[hg][ag]*dt)
#                p_awayScore = (1-lambda_t0[hg][ag]*dt) * (mu_t0[hg][ag]*dt)
#                p_noScore = (1-lambda_t0[hg][ag]*dt) * (1-mu_t0[hg][ag]*dt)
##                if n<1:
##                    print(lambda_t0[hg][ag], dt)
##                    print("Before normalization:", p_homeScore,",", p_awayScore,",", p_noScore)
#                p_sum = p_homeScore + p_awayScore + p_noScore
#                p_homeScore = p_homeScore/p_sum
#                p_awayScore = p_awayScore/p_sum
#                p_noScore = p_noScore/p_sum
#                #print(p_homeScore,p_awayScore,p_noScore,p_homeScore+p_awayScore+p_noScore)
##                if n<1:
##                    print("After normalization:", p_homeScore,",", p_awayScore,",", p_noScore)
##                    print("\n")
#
##                if n<2:
##                    print(self.np.multiply(dt,lambda_t0))
##                    print("\n")
#                cum_prob = list(self.np.accumulate([p_homeScore,p_awayScore,p_noScore]))
#                rand = random.random()
#                if rand<=cum_prob[0]:
#                    #print("Home Score!")
#                    hg += 1
#                elif rand<=cum_prob[1]:
#                    #print("Away Score!")
#                    ag += 1
#                    
#                if hg>9 or ag>9:
#                    break
#            
#            if hg<=9 and ag<=9:
#                result_matrix[hg][ag] += 1
#        
#        factor = 1.0/sum([e for inner_lst in result_matrix for e in inner_lst])
#        result_matrix = self.np.multiply(factor,result_matrix)
#        return result_matrix
        
    def run_virtual_match(self,league_id, home_team_id, away_team_id, 
                          kickoff_time=0, kickoff_hg=0, kickoff_ag=0,
                          N_sim=10000, NTimeStep = 540):
        alpha_h, beta_h, alpha_a, beta_a, gamma, lambda_, mu, rho, xi = (
                self.get_params(league_id, home_team_id, away_team_id)
                )
        
        timestamps = self.np.linspace(kickoff_time,90*60,NTimeStep)
        timestamps = [t*1.0/90./60. for t in timestamps] # normalized timestamps
        
        result_matrix = self.np.zeros((10,10))
        for _ in range(N_sim):
            if _%100==0:
                print("Simulation {} finished.".format(_))
            hg = kickoff_hg
            ag = kickoff_ag
            acc_dt = 0
            for n in range(len(timestamps)-1):
                
                t0 = timestamps[n]
                t1 = timestamps[n+1]
                dt = t1-t0
                
                #TODO: need to find a better way to describe the process.
                rand = random.random()
                if rand>0.5:
                    acc_dt += dt
                    danger_attack = True
                else:
                    acc_dt += dt
                    danger_attack = False
                    
                if danger_attack:
                    
                    dt = acc_dt*1.0
                    lambda_t0 = self.cal_lambda(t0, hg, ag, alpha_h, beta_a, gamma, lambda_, rho, xi)
                    mu_t0 = self.cal_lambda(t0, hg, ag, alpha_a, beta_h, 1.0, mu, rho, xi, False)
                    p_homeScore = (lambda_t0[hg][ag]*dt) * (1-mu_t0[hg][ag]*dt)
                    p_awayScore = (1-lambda_t0[hg][ag]*dt) * (mu_t0[hg][ag]*dt)
                    p_noScore = (1-lambda_t0[hg][ag]*dt) * (1-mu_t0[hg][ag]*dt)
    
                    p_sum = p_homeScore + p_awayScore + p_noScore
                    p_homeScore = p_homeScore/p_sum
                    p_awayScore = p_awayScore/p_sum
                    p_noScore = p_noScore/p_sum
    
                    cum_prob = list(self.np.accumulate([p_homeScore,p_awayScore,p_noScore]))
                    rand = random.random()
                    if rand<=cum_prob[0]:
                        hg += 1
                    elif rand<=cum_prob[1]:
                        ag += 1
                        
                    acc_dt = 0.0
                        
                    if hg>9 or ag>9:
                        break
            
            if hg<=9 and ag<=9:
                result_matrix[hg][ag] += 1
        
        factor = 1.0/sum([e for inner_lst in result_matrix for e in inner_lst])
        result_matrix = self.np.multiply(factor,result_matrix)
        return result_matrix        
            
            
                
    def get_pmatrix(self, league_id, home_team_id, away_team_id, t, hg, ag,
                    NTimeStep = 540):
        alpha_h, beta_h, alpha_a, beta_a, gamma, lambda_, mu, rho, xi = (
                self.get_params(league_id, home_team_id, away_team_id)
                )
        N = 10 # p-matrix dimension
        #NTimeStep = 541
        p_matrix = self.np.zeros((N,N))
        p_matrix[hg][ag] = 1
        timestamps = self.np.linspace(t,90*60,NTimeStep)
        timestamps = [t*1.0/90./60. for t in timestamps] # normalized timestamps
        p_matrix_T = self.cal_pmatrix(timestamps, p_matrix, alpha_h, alpha_a, beta_h, beta_a, gamma, lambda_, mu, rho, xi, hg, ag)
        #print(p_matrix_T)
        #print(p_matrix_T[0][0],p_matrix_T[1][0],p_matrix_T[2][0])
        return p_matrix_T
         

    def cal_pmatrix(self, timestamps, p_matrix, alpha_h, alpha_a, beta_h, beta_a, gamma, lambda_params, mu_params, rho, xi,
                 score_x, score_y, N=10):
        
        _upperScore_x = score_x + 1
        _upperScore_y = score_y + 1
        for n in range(len(timestamps)-1):
            t0 = timestamps[n]
            t1 = timestamps[n+1]
            dt = t1-t0
            lambda_t0 = self.cal_lambda(t0, score_x, score_y, alpha_h, beta_a, gamma, lambda_params, rho, xi)
            mu_t0 = self.cal_lambda(t0, score_x, score_y, alpha_a, beta_h, 1.0, mu_params, rho, xi, False)
            
            #p_matrix0 = np.copy(p_matrix)
            
            # WARN: shadow copy would cause p_matrix0 reference to p_matrix!
            p_matrix0 = copy.deepcopy(p_matrix)
   
            for x in range(0,10):
                for y in range(0,10):
                    p_matrix[x][y] = p_matrix0[x][y]*(1-lambda_t0[x][y]*dt)*(1-mu_t0[x][y]*dt)
                    if x>score_x and x<=_upperScore_x:
                        p_matrix[x][y] += p_matrix0[x-1][y]*lambda_t0[x-1][y]*dt*(1-mu_t0[x-1][y]*dt)                        
                    if y>score_y and y<=_upperScore_y:
                        p_matrix[x][y] += p_matrix0[x][y-1]*(1-lambda_t0[x][y-1]*dt)*mu_t0[x][y-1]*dt                       
            _upperScore_x += 1
            _upperScore_y += 1         
              
            adjust_factor = 1.0/sum([e for inner_lst in p_matrix for e in inner_lst])
            p_matrix = self.np.multiply(adjust_factor, p_matrix)
            
#            if n==0:
#                #print(lambda_t0)
#                print(p_matrix[0][0], p_matrix[0][1], p_matrix[1][0], p_matrix[1][1])

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
                lambda_ = self.np.ones_like(x)
                return lambda_
            
        def lambda_t(t, lambda_, xi):
            return (lambda_ + xi*t)
        
        lambda_t_matrix = self.np.zeros((10,10))
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
                    
                lambda_t_matrix[x][y] = lambda_t(t,lambda_,xi_1)
                
#                print(x,y,":",round(lambda_/injury_time_home_effect,4),"*",
#                      round(injury_time_home_effect,2),"+",round(xi_1,4),"*",
#                      round(t,4)," = ",round(lambda_t_matrix[x][y],4)
#                      )
        
        return lambda_t_matrix
    

if __name__=="__main__":
    virtualSports = VirtualSports(load_params="json")
    
    #test_cases = [(0,0,0),(10,0,0),(10,1,0),(10,0,2),(15,3,1),(55,2,2)]
    test_cases = [(65*60.,2,2)]
    for case in test_cases:
        kickoff_time = case[0]
        kickoff_hg = case[1]
        kickoff_ag = case[2]
        pmatrix = virtualSports.get_pmatrix(36,24,58,kickoff_time, kickoff_hg, kickoff_ag)
        tic = time.time()
        rmatrix = virtualSports.run_virtual_match(36,24,58,kickoff_time, kickoff_hg, kickoff_ag)
        print("time : {}".format(time.time()-tic))
        virtualSports.close()
        
#        with open("prob_matrix_sample("+str(kickoff_time)+","+str(kickoff_hg)+","+str(kickoff_ag)+")_v4.csv","w") as f:
#                writer = csv.writer(f)
#                writer.writerows(pmatrix)
#                
#        with open("result_matrix_sample("+str(kickoff_time)+","+str(kickoff_hg)+","+str(kickoff_ag)+")_v4.csv","w") as f:
#                writer = csv.writer(f)
#                writer.writerows(rmatrix)