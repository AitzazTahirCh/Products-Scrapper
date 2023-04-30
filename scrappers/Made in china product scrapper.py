#!/usr/bin/env python
# coding: utf-8

# In[2]:


import bs4 as bs
import re
import json
from math import ceil
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


# In[3]:


site= "https://yzecoway.en.made-in-china.com/product/TFtaGVhbHDko/China-500ml-Cleaning-Nourishing-Hair-Shampoo-in-Custom-Design-Pump-Bottle.html"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
data = BeautifulSoup(page, 'html.parser')
print(data)


# # Product name

# In[4]:


details = {}


# In[5]:


name = data.find('h1', attrs={'class', 'sr-proMainInfo-baseInfoH1 J-baseInfo-name'})
details["Product Name"] = name.text[17:-13]
print(name.text[17:-13])
price = data.find('div', attrs={'class', 'sr-proMainInfo-baseInfo-propertyPrice'})
details["Product Price"] = price.td.span.text
print(price.td.span.text)


# # Prodcuct Image

# In[9]:


img = data.find('a', attrs={'class', 'enlargeHref'})
details["Product Image"] = img.img["src"]
print(img.img["src"])


# # Main info

# In[22]:


x = data.find('div', attrs={'class', 'sr-proMainInfo-baseInfo-propertyAttr'})
y = x.table.tbody
y = list(y)
y = y[1:-1]
print(y)


# In[23]:


for i in y:
    try:
        print(i.th.text)
        print(i.td.text)
        details[i.th.text] = i.td.text
    except:
        continue
    print("--")


# # Basic info

# In[24]:


d = data.find_all('div', attrs={'div', 'bsc-item cf'})
print(len(d))


# In[25]:


for de in d:
    print(de.select_one(":nth-child(1)").text)
    print(de.select_one(":nth-child(2)").text)
    details[de.select_one(":nth-child(1)").text] = de.select_one(":nth-child(2)").text 
    print("=-----=")


# # Product specification

# In[26]:


s = data.find('div', attrs={'div', 'rich-text-table'})
s = s.table.tbody
print(s)
print(len(s))


# In[27]:


for se in s:
    print(se.select_one(":nth-child(1)").text)
    print(se.select_one(":nth-child(2)").text)
    details[se.select_one(":nth-child(1)").text] = se.select_one(":nth-child(2)").text 
    print("=-----=")


# In[28]:


l = []
l.append(details)
pdata = pd.DataFrame.from_dict(l)
pdata.to_csv('pdata.csv', index=False)

