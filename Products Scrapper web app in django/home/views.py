from django.shortcuts import render
from selenium import webdriver
import requests, re, json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
# Create your views here.

# for aliexpress
target = ["title", "itemDetailUrl", "imagePath"]
def main(url):
    details = {}
    html_paged = webdriver.Chrome('chromedriver')
    html_paged.get(url)
    name = html_paged.find_element("xpath",'//*[@class="product-title-text"]')
    details["Product Name"] = name.text
    r = requests.get(url)
    match = re.search(r'data: ({.+})', r.text).group(1)
    data = json.loads(match)
    goal = [data['pageModule'][x] for x in target] + \
        [data['priceModule']['formatedActivityPrice']]
    a = ["Common SEO Search Titles/Tags of product", "Product Link", "Product Image", "Product Price"]
    details.update(dict(zip(a,goal)))
    try:
        d = html_paged.find_element("xpath",'//*[@id="product-description"]')
        details["Product Description/Specification"] = d.text
        # if d.text == '':
        #     d = html_paged.find_element("xpath",'//*[@class="product-detail-tab"]/div/div/div[2]')
        #     details["Product Description/Sprcification"] = d.text
        #     html_paged.quit()
        html_paged.quit()
        return details
    except:
        try:
            d = html_paged.find_element("xpath",'//*[@class="product-detail-tab"]/div/div/div[2]')
            details["Product Description/Sprcification"] = d.text
            html_paged.quit()
            return details
        except:
            pass
 
#     r = requests.get(url)
#     match = re.search(r'data: ({.+})', r.text).group(1)
#     data = json.loads(match)
#     goal = [data['pageModule'][x] for x in target] + \
#         [data['priceModule']['formatedActivityPrice']]
#     return goal

# def main2(url):
#     html_paged = webdriver.Chrome('chromedriver')
#     html_paged.get(url)
#     try:
#         d = html_paged.find_element("xpath",'//*[@class="product-detail-tab"]/div/div/div[2]')
#         x = d.text
#         if d.text == '':
#             x = html_paged.find_element("xpath",'//*[@id="product-description"]')
#             x = x.text
#             html_paged.quit()
#         html_paged.quit()
#     except:
#         try:
#             x = html_paged.find_element("xpath",'//*[@id="product-description"]')
#             x = x.text
#             html_paged.quit()
#         except:
#             pass
#     return x

# for daraz
def fetchInfo(product_url):
    html_doc = requests.get(product_url).text
    data = re.search(r'pdpTrackingData = ("{.*}")', html_doc)

    if data is None:
        return {"status": False, "error": "Failed to retrieve product information"}

    data = json.loads(data.group(1))
    data = data.replace('\"', '"')
    data = json.loads(data)

    result = {}
    result['Product Name'] = data['pdt_name']
    result['Seller'] = data['seller_name']
    result['Product Price'] = data['pdt_price']
    result['Product Image'] = data['pdt_photo']
    result['Category'] = data['pdt_category']
    result['Discount'] = data['pdt_discount']
    result['Brand Name'] = data['brand_name']
    result['Product SKU'] = data['pdt_sku']
    result['Product Simple SKU'] = data['pdt_simplesku']
    result['Country'] = data['core']['country']
    return result

# for made in china
def madeinchina(url):
    site = url
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    data = BeautifulSoup(page, 'html.parser')
    
    details = {}
    
    name = data.find('h1', attrs={'class', 'sr-proMainInfo-baseInfoH1 J-baseInfo-name'})
    details["Product Name"] = name.text[17:-13]
    price = data.find('div', attrs={'class', 'sr-proMainInfo-baseInfo-propertyPrice'})
    details["Product Price"] = price.td.span.text
    img = data.find('a', attrs={'class', 'enlargeHref'})
    details["Product Image"] = img.img["src"]
    x = data.find('div', attrs={'class', 'sr-proMainInfo-baseInfo-propertyAttr'})
    y = x.table.tbody
    y = list(y)
    y = y[1:-1]
    for i in y:
        try:
            details[i.th.text] = i.td.text
        except:
            continue
    
    d = data.find_all('div', attrs={'div', 'bsc-item cf'})
    for de in d:
        details[de.select_one(":nth-child(1)").text] = de.select_one(":nth-child(2)").text 
    
    s = data.find('div', attrs={'div', 'rich-text-table'})
    s = s.table.tbody
    for se in s:
        details[se.select_one(":nth-child(1)").text] = se.select_one(":nth-child(2)").text 
    return details

def index(request):
    if request.GET.get('url'):
        url = request.GET.get('url')
        if "aliexpress" in url:
        # if (request.GET.get('select') == "1"):
            data = main(url)
            return render(request, 'index.html',{  'data': data , 'image': data["Product Image"]})
        elif "daraz" in url: 
        # elif (request.GET.get('select') == "2"):
            data = fetchInfo(url)
            return render(request, 'index.html', { "data": data , 'image': data["Product Image"]})
        elif "made-in-china" in url:
        # elif (request.GET.get('select') == "3"):
            data = madeinchina(url)
            return render(request, 'index.html', { "data": data , 'image': data["Product Image"]})
    else:
        return render(request, 'index.html')