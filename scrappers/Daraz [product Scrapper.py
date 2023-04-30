#!/usr/bin/env python
# coding: utf-8

# In[18]:


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


# # Extracting categories and their links 

# In[19]:


site= "https://www.daraz.pk/"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
data = BeautifulSoup(page, 'html.parser')
print(data)


# In[ ]:


x = data.find('ul', attrs={'class', 'lzd-site-menu-root'})
x = x.find_all("a")
x = x[12:]
category_list = []
for y in x:
    categories = {}
    categories["category name"] = y.text[1:-1]
    test = y.get('href')
    url = 'https:'+str(test)
    categories["category link"] = url
    
    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    total_products_category_element = driver.find_element(By.XPATH, "//div[@class='result-tips--Knf5Y']/div/div/span")
    total_products_category = [int(i) for i in total_products_category_element.text.split() if i.isdigit()]
    driver.quit()
    categories["total products"] = total_products_category[0]
    
    
    category_list.append(categories)
print(category_list)


# In[252]:


dataFrame = pd.DataFrame.from_dict(category_list)
print(dataFrame)

dataFrame.to_csv('categories data.csv', index=False)


# # Extracting all pages links of all categories

# In[16]:


def get_pages_list(category_url, total_number_of_products):
    '''
    params: category_url : url of the category
            total_number_of_products : total number of products for that category 

    returns:    1. method computes the possible number of pages according to the number of products
                2. Creates a new list of url for all the page and then returns the list
    '''

    total_pages_category = ceil(total_number_of_products / 40)

    if total_pages_category > 1:
        category_pages_list = []

        for page in range(1, total_pages_category+1):
            if page == 1:
                category_pages_list.append(category_url)
            elif page >= 105:
                break
            else:
                category_pages_list.append(category_url+'?page='+str(page))
        return category_pages_list
    else:
        return []


# In[17]:


import csv
 
# opening the CSV file
with open('categories data.csv', mode ='r')as file:
    
  # reading the CSV file
    csvFile = csv.reader(file)
 
  # displaying the contents of the CSV file
    counter = 0
    links_data = []
    for lines in csvFile:
        counter +=1
        if counter == 1:
            continue
        else:
            pages_list = get_pages_list(lines[1],int(lines[2]))
            for p in pages_list:
                details = {}
                details["category name"] = lines[0]
                details["page link"] = p
#                 print(details["category name"])
#                 print(details["page link"])
                links_data.append(details)
# print(links_data)
pageslink_data = pd.DataFrame.from_dict(links_data)
# print(pageslink_data)
pageslink_data.to_csv('pageslink_data.csv', index=False)


# # Extracting Products links

# In[6]:


import csv
page_links = []
with open('pageslink_data.csv', mode ='r')as f:
    myFile = csv.reader(f)
    counter = 0
    for rows in myFile:
        counter +=1
        if counter == 1:
            continue
        else:
#             print(rows[1])
            page_links.append(rows[1])
    
#     print(page_links)   


# In[7]:


products_list = []
for page in page_links:

    html_paged = webdriver.Chrome('chromedriver')
    html_paged.get(page)

    if html_paged:
        for i in range(1, 40):
            '''
            Reason for iterating 40 elements is that Daraz Only Displays 40 items on its page, Hence we will fetch the product url for 40 items and then restart the counter for the next page.
            '''
            try:
                target_name = html_paged.find_element("xpath",'//*[@class="ant-col-20 ant-col-push-4 side-right--Tyehf"]/div[2]/div['+str(i)+']/div/div/div[2]/div[2]/a')
                if target_name:
                    pr_link = target_name.get_attribute("href")
                    products_list.append(pr_link)
                    print (pr_link)
                    # These product links would be written to an excel file and then next script will take care to cal the fetchInfo() method
                else:
                    break
            except:
                break
    else:
        continue
    html_paged.quit()


# In[8]:


print(products_list)


# In[12]:


products_links = pd.DataFrame.from_dict(products_list)
products_links.to_csv('products_links.csv', index=False)


# # Fetching product details

# In[2]:


import csv
product_links = []
with open('products_links.csv', mode ='r')as t:
    li = csv.reader(t)
    counter = 0
    for rows in li:
        counter +=1
        if counter == 1:
            continue
        else:
#             print(rows[0])
            product_links.append(rows[0])

print(product_links)


# In[3]:


def fetchInfo(product_url):
    '''
    params: product_url : link of the product

    returns: basic information of product 
    '''

    html_doc = requests.get(product_url).text
    data = re.search(r'pdpTrackingData = ("{.*}")', html_doc)

    if data is None:
        return {"status": False, "error": "Failed to retrieve product information"}

    data = json.loads(data.group(1))
    data = data.replace('\"', '"')
    data = json.loads(data)

    result = {}
    result['name'] = data['pdt_name']
    result['seller'] = data['seller_name']
    result['price'] = data['pdt_price']
    result['image'] = data['pdt_photo']
    result['category'] = data['pdt_category']
    result['discount'] = data['pdt_discount']
    result['brand_name'] = data['brand_name']
    result['pdt_sku'] = data['pdt_sku']
    result['pdt_simplesku'] = data['pdt_simplesku']
    result['country'] = data['core']['country']
    return result


# In[4]:


product_detail = []
for link in product_links:
    product_detail.append(fetchInfo(link))
    print(fetchInfo(link))


# In[5]:


products_details = pd.DataFrame.from_dict(product_detail)
products_details.to_csv('products_details.csv', index=False)

