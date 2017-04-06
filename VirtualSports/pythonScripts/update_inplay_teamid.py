# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:06:02 2017

@author: joseph.chen
"""

from sql_connector import SQLConnector

class UpdateInplayTeamID(object):
    def __init__(self, league_id=36):
        self.league_id = league_id
        self.sql = SQLConnector()
        self.team_names_in_goal_times = self.get_names_from_goal_times()
        self.team_pool = self.get_names_from_team()
        self.league_id = []
        self.team_id = []
        self.team_name = []
        for team in self.team_pool:
            self.team_id.append(team[0])
            self.league_id.append(team[1])
            self.team_name.append(team[2])      
        self.mapping()
        self.map_exception()
        
    def close(self):
        self.sql.close()
        
    def get_names_from_goal_times(self):
        query = ("SELECT DISTINCT `home_team_name` FROM `goal_times` " +
                "WHERE league_id IS NULL") 
        team_names = [d[0] for d in self.sql.execute(query)]
        return team_names
    
    def get_names_from_team(self):
        query = "SELECT `team_id`,`league_id`,`en` FROM `team`"
        team_names = self.sql.execute(query)
        return team_names
    
    def mapping(self):
        self.exception = []
        self.mapp = {}
        for tn in self.team_names_in_goal_times:
            #print(tn)
            if tn in self.team_name:
                idx = self.team_name.index(tn)
                self.mapp[tn] = (self.league_id[idx], self.team_id[idx])
            else:
                self.exception.append(tn)
                self.mapp[tn] = ()
        print("Teams that do NOT find match names: \n{}".format(self.exception))
        #return self.mapp
    
    def map_exception(self, default=False):
        for name in self.exception:
            query = ("SELECT `team_id`, `league_id`, `en` " +
                     "FROM `team` " +
                     "WHERE `en` LIKE \"%{}%\"".format(name))
            print("\n------------------\nResults that match team *{}*:".format(name))
            print(self.sql.execute(query))
            if default:
                select = " ".join([str(d) for d in self.sql.execute(query)[0][:2]]) 
                print("*Default* You choose first matching result: {}".format(select))
            else:
                select = input("*User Input* Please input the correct team_id & "
                               "league_id for team '{}':\n".format(name))
            try:
                team_id, league_id = select.split(" ")
                league_id = int(league_id)
                team_id = int(team_id)
                self.mapp[name] = (league_id, team_id)
            except:
                print("league_id & team_id should be integers with space split.")
                raise
        print("\n Team id map:\n{}".format(self.mapp))
        
    def update(self):
        query = ("SELECT `goal_times_id`,`home_team_name`,`away_team_name` " +
                 "FROM `goal_times` " +
                 "WHERE league_id IS NULL " +
                 "OR home_team_id IS NULL " +
                 "OR away_team_id IS NULL")  
        goal_times = self.sql.execute(query)
        
        print(goal_times)

#        for g in goal_times[:]:
#            #print(g)
#            g_id = g[0]
#            home_name = g[1]
#            away_name = g[2]
#            league_id_h, home_id = self.mapp[home_name]
#            league_id_a, away_id = self.mapp[away_name]
#            if league_id_h==league_id_a:
#                # TODO: Here we choose to update all records to league_id=36.
#                # Still not a perfect solution. (Should be league_id_h ???)
#                query = ("UPDATE `goal_times` " +
#                         "SET league_id={}, ".format(75) +
#                         "home_team_id={}, ".format(home_id) +
#                         "away_team_id={} ".format(away_id) +
#                         "WHERE goal_times_id={}".format(g_id)
#                        )
#                #print("1. >> {}".format(query))
#                self.sql.execute(query)
#                self.sql.commit()
#            else:
#                # TODO: How to deal with the special cases where tournament
#                # had been downgraded ?
#                # Temperally set all special case to league_id=36.
#                # Need to find a better solution in the future.
#                query = ("UPDATE `goal_times` " +
#                         "SET league_id={}, ".format(75) +
#                         "home_team_id={}, ".format(home_id) +
#                         "away_team_id={} ".format(away_id) +
#                         "WHERE goal_times_id={}".format(g_id)
#                        )
#                #print("2. >> {}".format(query))
#                self.sql.execute(query)
#                self.sql.commit()
                
            
            
        
if __name__=="__main__":
    updateTeamID = UpdateInplayTeamID()
    updateTeamID.update()
    updateTeamID.close()
    