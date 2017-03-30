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

#DOWNLOAD_URL = 'http://www.soccerassociation.com/int/1314/WC,f/u0gA.htm'
DOWNLOAD_URL = 'http://www.soccerassociation.com'
WEEK = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
MONTH = ({"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
          "July":7,"August":8,"September":9,"October":10,"November":11,
          "December":12})

class SoccerAssociation(object):
    
    def __init__(self, year=2014):
        start = str((year - 1) - 2000)
        end = str(year - 2000)
        self.base_url = ('http://www.soccerassociation.com/int/' + start + end +
                         '/WC,f/')
        
    def get_results(self):
        url = self.base_url + 'u0gA.htm'
        page = self.download_page(url)
        soup = BeautifulSoup(page, "lxml")
        table = soup.find("table",{"cellspacing":"0", "cellpadding":"1", 
                                   "border":"0", "bgcolor":"#000099"})
        tbody = table.find("tbody")
        print(tbody)
    
    def download_page(self, url):
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
    


