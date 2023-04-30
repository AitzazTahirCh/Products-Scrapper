#!/usr/bin/env python
# coding: utf-8

# In[30]:


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


# # Aliexpress product scrapper

# In[133]:


details = {}
url = "https://www.aliexpress.com/item/1005004990769251.html?spm=a2g0o.detail.1000014.7.666d6338vgShOI&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.40050.281175.0&scm_id=1007.40050.281175.0&scm-url=1007.40050.281175.0&pvid=3871b0b6-4237-4e46-9c6c-39bea4d17fd1&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.40050.281175.0,pvid:3871b0b6-4237-4e46-9c6c-39bea4d17fd1,tpp_buckets:668%232846%238113%231998&pdp_ext_f=%7B%22sku_id%22%3A%2212000031262007959%22%2C%22sceneId%22%3A%2230050%22%7D&pdp_npi=3%40dis%21PKR%2111813.37%215082.24%21%21%21%21%21%40210312ea16774898613835356e9bfe%2112000031262007959%21rec%21PK%21"

target = ["title", "itemDetailUrl", "imagePath"]

r = requests.get(url)
match = re.search(r'data: ({.+})', r.text).group(1)
data = json.loads(match)
goal = [data['pageModule'][x] for x in target] +     [data['priceModule']['formatedActivityPrice']]
a = ["Common search titles for this product", "Product Link", "Product Image", "Price"]
details = dict(zip(a,goal))

html_paged = webdriver.Chrome('chromedriver')
html_paged.get(url)
name = html_paged.find_element("xpath",'//*[@class="product-title-text"]')
details["Product Name"] = name.text
print(name.text)
try:
    d = html_paged.find_element("xpath",'//*[@class="product-detail-tab"]/div/div/div[2]')
    details["Product Description/Sprcification"] = d.text
    print(d.text)
    if d.text == '':
        x = html_paged.find_element("xpath",'//*[@id="product-description"]')
        details["Product Description/Sprcification"] = x.text
        print(x.text)
        html_paged.quit()
    html_paged.quit()
except:
    try:
        x = html_paged.find_element("xpath",'//*[@id="product-description"]')
        details["Product Description/Sprcification"] = x.text
        print(x.text)
        html_paged.quit()
    except:
        pass

print()
print("-------")
print(details)


# In[ ]:





# In[99]:


html_paged = webdriver.Chrome('chromedriver')
html_paged.get("https://www.aliexpress.com/item/1005004990769251.html?spm=a2g0o.detail.1000014.7.666d6338vgShOI&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.40050.281175.0&scm_id=1007.40050.281175.0&scm-url=1007.40050.281175.0&pvid=3871b0b6-4237-4e46-9c6c-39bea4d17fd1&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.40050.281175.0,pvid:3871b0b6-4237-4e46-9c6c-39bea4d17fd1,tpp_buckets:668%232846%238113%231998&pdp_ext_f=%7B%22sku_id%22%3A%2212000031262007959%22%2C%22sceneId%22%3A%2230050%22%7D&pdp_npi=3%40dis%21PKR%2111813.37%215082.24%21%21%21%21%21%40210312ea16774898613835356e9bfe%2112000031262007959%21rec%21PK%21")
d = html_paged.find_element("xpath",'//*[@class="product-detail-tab"]/div/div/div[2]')
print(d.text)

html_paged.quit()


# In[136]:


url = "https://www.aliexpress.com/item/1005005192929134.html?spm=a2g0o.productlist.main.1.6cd914f10mmFke&algo_pvid=431e8e86-19ce-40f7-a2d3-6f88e4087602&algo_exp_id=431e8e86-19ce-40f7-a2d3-6f88e4087602-0&pdp_ext_f=%7B%22sku_id%22%3A%2212000032067301130%22%7D&pdp_npi=3%40dis%21PKR%213490.4%211557.67%21%21%21%21%21%4021021d7b16774855370001285d074c%2112000032067301130%21sea%21PK%210&curPageLogUid=qEKm6WvlDTHu"
html_paged = webdriver.Chrome('chromedriver')
html_paged.get(url)
x = html_paged.find_element("xpath",'//*[@id="product-description"]')
print(x.text)
html_paged.quit()


# In[ ]:





# In[129]:


def main(url):
    r = requests.get(url)
    match = re.search(r'data: ({.+})', r.text).group(1)
    data = json.loads(match)
    goal = [data['pageModule'][x] for x in target] +         [data['priceModule']['formatedActivityPrice']]
    a = ["Common search titles for this product", "Product Link", "Product Image", "Price"]
    result = dict(zip(a,goal))
    return result
print()
main("https://www.aliexpress.com/item/1005004990769251.html?spm=a2g0o.detail.1000014.7.666d6338vgShOI&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.40050.281175.0&scm_id=1007.40050.281175.0&scm-url=1007.40050.281175.0&pvid=3871b0b6-4237-4e46-9c6c-39bea4d17fd1&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.40050.281175.0,pvid:3871b0b6-4237-4e46-9c6c-39bea4d17fd1,tpp_buckets:668%232846%238113%231998&pdp_ext_f=%7B%22sku_id%22%3A%2212000031262007959%22%2C%22sceneId%22%3A%2230050%22%7D&pdp_npi=3%40dis%21PKR%2111813.37%215082.24%21%21%21%21%21%40210312ea16774898613835356e9bfe%2112000031262007959%21rec%21PK%21")

