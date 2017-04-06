# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 16:50:56 2017

@author: joseph.chen
"""
import requests
from bs4 import BeautifulSoup

class SoccerAssociation(object):
    
    def __init__(self):
        self.base_url = ('http://www.soccerassociation.com/sqp/int/index.htm' )
        
    def download_page(self, url):
        print(url)
        return requests.get(url, headers={
            "Connection":"keep-alive",
            "Cookie":"jt=1490950148177",
            "Host":"www.soccerassociation.com",
            "Referer":"http://www.soccerassociation.com/int/index.htm",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":("Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) " + 
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" + 
                          "56.0.2924.87 Mobile Safari/537.36")
        }).content
            
    def get_results(self):
        page = self.download_page(self.base_url)
        soup = BeautifulSoup(page,"lxml")
        table = soup.find("table",{"border":"0","cellspacing":"1",
                                   "cellpadding":"1","width":"90%"})
        brTags = table.find_all("br")
        countries = []
        for br in brTags:
            nextTag = br.nextSibling
            try:
                nextTag = nextTag.text.strip()
            except:
                nextTag = str(nextTag)
            print(nextTag, type(nextTag))
            countries.append(nextTag)
        return countries
            
            

if __name__=="__main__":
    sa = SoccerAssociation()
    countries = sa.get_results()