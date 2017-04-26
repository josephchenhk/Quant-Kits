# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 12:33:25 2017

@author: joseph.chen
"""

from selenium import webdriver
import urllib.parse
import time
import random

if __name__=="__main__":
    base_url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd="
    #driver = webdriver.Chrome()
    keywords = open("baidukeywords",encoding="utf-8") 
    keyword = keywords.readline()
    while keyword:
        print(keyword)
        query = urllib.parse.quote(keyword, safe='')
        url = base_url + query
        print(url)
        print("-----------------------------\n")
        driver = webdriver.Chrome()

        driver.get(url)
        #sleeptime =  random.randint(5, 10) + random.random()
        #time.sleep(sleeptime)
        input("Press Enter to continue...")
        driver.quit()
        
        keyword = keywords.readline()
    keywords.close()
    