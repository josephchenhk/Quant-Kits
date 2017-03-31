# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 14:57:44 2016

@author: joseph.chen
"""

import codecs
import pandas as pd
import requests
import datetime
import time
import random
from bs4 import BeautifulSoup
import sys
import warnings


class SoccerAssociation(object):
    
    def __init__(self, year=2014):
        start = str((year - 1) - 2000)
        end = str(year - 2000)
        self.base_url = ('http://www.soccerassociation.com/int/' + start + end +
                         '/WC,f/')
        self.WEEK = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        self.MONTH = ({"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
                       "July":7,"August":8,"September":9,"October":10,"November":11,
                       "December":12})
        self.group_stage = ["u0gA","u0gB","u0gC","u0gD","u0gE","u0gF","u0gG","u0gH"]
        self.round_2 = ["u0r2"]
        self.quarter_final = ["u0s0"]
        self.semi_final = ["u0t0"]
        self.third_fourth = ["u0tp"]
        self.final = ["u0u0"]
        
        
    def get_results(self):
        
#        for stage in self.group_stage:
#            url = self.base_url + stage + ".htm"
#            page = self.download_page(url)
#            soup = BeautifulSoup(page, "lxml")
#            table = soup.find("table",{"cellspacing":"1", "cellpadding":"1", 
#                                       "border":"0", "bgcolor":"#cccccc"})
#            trs = table.find_all("tr")
#            data_ready = False
#            for tr in trs:
#                text = tr.text.strip()
#                if text.split(",")[0] in self.WEEK:
#                    day, month, year = (text.split(",")[1].strip().split("\xa0"))
#                    date = year + "-" + str(self.MONTH[month]) + "-" + day
#                    data_ready = False
#                else:
#                    tds = tr.find_all("td")
#                    home_team = tds[0].text.strip()
#                    hg,ag = tds[1].text.strip().split("-")
#                    away_team = tds[2].text.strip()
#                    data_ready = True
#                if data_ready:
#                    print(date, home_team, hg, "-", ag, away_team)
          
        knockout = (self.round_2 + self.quarter_final + self.semi_final  
                    + self.third_fourth + self.final)
        for stage in knockout:
            print("---------------------\nStage {}".format(stage))
            url = self.base_url + stage + ".htm"
            page = self.download_page(url)
            soup = BeautifulSoup(page, "lxml")
            table = soup.find("table",{"cellspacing":"1", "cellpadding":"1", 
                                       "border":"0", "bgcolor":"#cccccc"})
            trs = table.find_all("tr")
            
            data_ready = False
            for n in range(len(trs)):
                tr = trs[n]
                text = tr.text.strip()
                try:
                    next_text = trs[n+1].find_all("td")[0].text.strip()
                except:
                    next_text = None
                if text.split(",")[0] in self.WEEK:
                    day, month, year = (text.split(",")[1].strip().split("\xa0"))
                    date = year + "-" + str(self.MONTH[month]) + "-" + day
                    data_ready = False
                else:
                    tds = tr.find_all("td")
                    td0_text = tds[0].text.strip()
                    if not self.is_goal_times(td0_text):                     
                        home_team = tds[0].text.strip()
                        hg,ag = tds[1].text.strip().split("-")
                        away_team = tds[2].text.strip()
                        goal_times = {'home':[],"away":[]}
                        data_ready = False
                        if not self.is_goal_times(next_text):
                            #print("next_text:{}".format(next_text))
                            #print(self.is_goal_times(next_text),">???\n")
                            data_ready = True
                    else:
                        if len(tds)==4:
                            if tds[0].text.strip()!="":                                
                                goal_time = tds[0].text.strip()
                                goal_player = tds[1].text.strip()
                                goal_times["home"].append((goal_time,goal_player))
                            else:
                                goal_time = tds[2].text.strip()
                                goal_player = tds[3].text.strip()
                                goal_times["away"].append((goal_time,goal_player))
                        elif len(tds)==5:
                            goal_time = tds[0].text.strip()
                            goal_player = tds[1].text.strip()
                            goal_times["home"].append((goal_time,goal_player))
                            goal_time = tds[3].text.strip()
                            goal_player = tds[4].text.strip()
                            goal_times["away"].append((goal_time,goal_player))
                        else:
                            warnings.warn("Format incorrect!")
                        if not self.is_goal_times(next_text):
                            data_ready = True
                if data_ready:
                    print(date, home_team, hg, "-", ag, away_team, goal_times, "\n")
            
        
    def is_int(self, text_str):
        try:
            int(text_str)
            return True
        except (ValueError,TypeError):
            return False
        
    def is_goal_times(self, td_text):
        
        if td_text==None:
            return False
        elif type(td_text)==str:
            td_text = td_text.split("(")[0]
            if self.is_int(td_text) or td_text=="":
                return True
            else:
                return False
        else:
            print("td_text is neither None nor str type: {}".format(td_text))
            return False
    
    def download_page(self, url):
        print(url)
        return requests.get(url, headers={
            "Host": "www.soccerassociation.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "http://www.soccerassociation.com/int/1314/WC,f/u0r2.htm",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Cookie": "jt=1490838664110",
        }).content
    

    


if __name__ == '__main__':
    sa = SoccerAssociation(year=2014)
    sa.get_results()
    


