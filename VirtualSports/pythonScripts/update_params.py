# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:33:40 2017

@author: joseph.chen
"""
import json
import statsmodels.api as sm
import numpy as np

from mle import BirthProcess
from sql_connector import SQLConnector

class UpdateParams(object):
    
    def __init__(self):
        try:
            self.params = sm.load("estimates/estimated_params_36.pickle")
        except TypeError:
            raise TypeError("The estimated_params.pickle file is NOT in current directory.")
            
        try:
            with open("estimates/estimated_teams_36.json","r") as f:
                self.teams = json.load(f)
        except TypeError:
            raise TypeError("The estimated_teams.pkl file is NOT in current directory.")
        
        self.sql = SQLConnector()
        
        self.num_xi = 2
        self.num_rho = 2
        self.num_mu = 6
        self.num_lambda = 6
        self.num_gamma = 1
        self.num_team = len(self.teams)
        self.alpha,self.beta,self.gamma,self.lambda_,self.mu,self.rho,self.xi = self.parse_params()
    
    def close(self):
        self.sql.close()
        
    def parse_params(self):
        results = self.params
        alpha_indept = results.params[0:self.num_team-1]
        alpha_last = self.num_team - sum(alpha_indept)
        alpha = list(alpha_indept) + [alpha_last]
        alpha_indept_sd = results.bse[0:self.num_team-1]
        alpha_last_sd = 0
        alpha_sd = alpha_indept_sd + [alpha_last_sd]
        
        beta = results.params[self.num_team-1:2*self.num_team-1]
        beta_sd = results.bse[self.num_team-1:2*self.num_team-1]
        
        gamma = results.params[2*self.num_team-1:2*self.num_team][0]
        gamma_sd = results.bse[2*self.num_team-1:2*self.num_team][0]
        
        if (self.num_lambda>0) & (self.num_mu>0):
            lambda_ = results.params[2*self.num_team:2*self.num_team+self.num_lambda]
            lambda_sd = results.bse[2*self.num_team:2*self.num_team+self.num_lambda]
            mu = results.params[2*self.num_team+self.num_lambda:2*self.num_team+self.num_lambda+self.num_mu]
            mu_sd = results.bse[2*self.num_team+self.num_lambda:2*self.num_team+self.num_lambda+self.num_mu]
            if (self.num_rho>0):
                rho = results.params[2*self.num_team+self.num_lambda+self.num_mu:2*self.num_team+self.num_lambda+self.num_mu+self.num_rho]
                rho_sd = results.bse[2*self.num_team+self.num_lambda+self.num_mu:2*self.num_team+self.num_lambda+self.num_mu+self.num_rho]
                if (self.num_xi>0):
                    xi = (results.params[2*self.num_team+self.num_lambda+self.num_mu+self.num_rho:
                                         2*self.num_team+self.num_lambda+self.num_mu+self.num_rho+self.num_xi])
                    xi_sd = (results.bse[2*self.num_team+self.num_lambda+self.num_mu+self.num_rho:
                                         2*self.num_team+self.num_lambda+self.num_mu+self.num_rho+self.num_xi])
        elif (self.num_rho>0):
            rho = results.params[2*self.num_team:2*self.num_team+self.num_rho]
            rho_sd = results.bse[2*self.num_team:2*self.num_team+self.num_rho]
            if (self.num_xi>0):
                xi = results.params[2*self.num_team+self.num_rho:2*self.num_team+self.num_rho+self.num_xi]
                xi_sd = results.bse[2*self.num_team+self.num_rho:2*self.num_team+self.num_rho+self.num_xi]
        elif (self.num_xi>0):
            xi = results.params[2*self.num_team:2*self.num_team+self.num_xi]
            xi_sd = results.bse[2*self.num_team:2*self.num_team+self.num_xi]
        
        try:
#            alpha = [float(a) for a in alpha]
#            beta = [float(b) for b in beta]
#            lambda_ = [float(l) for l in lambda_]
#            mu = [float(m) for m in mu]
#            rho = [float(r) for r in rho]
#            xi = [float(x) for x in xi]

            ## ALERT: Exponentiate all parameters
            alpha = [np.exp(float(a)) for a in alpha]
            beta = [np.exp(float(b)) for b in beta]
            gamma = np.exp(gamma)
            lambda_ = [np.exp(float(l)) for l in lambda_]
            mu = [np.exp(float(m)) for m in mu]
            rho = [np.exp(float(r)) for r in rho]
            xi = [np.exp(float(x)) for x in xi]
            return (alpha,beta,gamma,lambda_,mu,rho,xi)
        except Exception as e:
            raise
     
    def get_team_ids(self, league_id):
        query = ("SELECT DISTINCT `home_team_name`, `home_team_id` " +
                 "FROM `goal_times` " +
                 "WHERE `league_id` = %s")
        #print(query)
        params = (league_id,)
        team_id = self.sql.execute(query,params)
        return team_id
        
        
    def upload_params(self, league_id):
        query = ("INSERT INTO `inplay_league_params` " +
                 "(league_id, gamma, lambda, mu, rho, xi) " +
                 "VALUES (%s, %s, %s, %s, %s, %s) ")
        lambda_str = json.dumps(self.lambda_)
        mu_str = json.dumps(self.mu)
        rho_str = json.dumps(self.rho)
        xi_str = json.dumps(self.xi)
        params = (int(league_id), float(self.gamma), lambda_str, mu_str, 
                  rho_str, xi_str)
        self.sql.execute(query,params)        
        team_ids = self.get_team_ids(league_id)
        for n, team_name in enumerate(self.teams):
            alpha = self.alpha[n]
            beta = self.beta[n]
            team_id = [t[1] for t in team_ids if t[0]==team_name][0]
            query = ("INSERT INTO `inplay_team_params` " +
                     "(league_id, team_id, team_name, alpha, beta) " +
                     "VALUES (%s, %s, %s, %s, %s) ")
            params = (int(league_id), int(team_id), str(team_name), 
                      float(alpha), float(beta))
            self.sql.execute(query,params)
            
        self.sql.commit()
            

if __name__=="__main__":
    updateParams = UpdateParams()
    #print(updateParams.params.summary())
    #updateParams.get_team_ids(36)
    updateParams.upload_params(36)
    updateParams.close()