# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 12:23:04 2016

@author: joseph.chen
"""

import pandas as pd
import sys
import mysql.connector
from sqlalchemy import create_engine

if __name__=="__main__":

    DB_USER = 'football2'
    DB_PASS = 'f00tba11' 
    DB_HOST = '172.20.2.177' 
    DB_PORT = '3306'
    DATABASE = 'virtual_sport_football'
    
    cnx = mysql.connector.connect(user=DB_USER, 
                                  password=DB_PASS, 
                                  host=DB_HOST, 
                                  port=DB_PORT,
                                  database=DATABASE)
    
    connect_info = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8'.format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE)  #1
    engine = create_engine(connect_info)
    
    for year in [2014]:
        
        data_file = "../../Crawler/SoccerAssociation/data/worldcup/goal_times_worldcup_year_%s.xlsx"%year   
        df = pd.read_excel(data_file)
        
        try:
            df.to_sql(name="goal_times", con=engine, if_exists="append",index=False)
        except Exception as e:
            sys.exit("Fail to upload to MySQL database.\nError: {}".format(e))
    