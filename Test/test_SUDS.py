# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 18:32:28 2017

@author: joseph.chen
"""

import logging
logging.basicConfig(level=logging.INFO)
 
from suds.client import Client
from suds.sax.element import Element
from suds.wsse import *
 
url = 'https://api.bettingpromotion.com/BPBookmakerAPI/BookmakerAPIService.asmx?WSDL'
client = Client(url)

security = Security()
username = "betdemo"
password = "demobet"
token = UsernameToken(username, password)
security.tokens.append(token)
client.set_options(wsse=security)
#client.set_options(soapheaders=(username,password))

#print(client)
#with open("client.txt","w") as f:
#    f.write(str(client))

result = client.service.GetAllOdds()
print(result)