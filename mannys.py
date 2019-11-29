# -*- coding: utf-8 -*-
import csv     
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup 
import sys
import urllib

reload(sys)
sys.setdefaultencoding('utf8')
class AppURLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"


csv.register_dialect('myDialect1',
	  quoting=csv.QUOTE_ALL,
	  skipinitialspace=True)

write_file = open('mannys.csv', 'a')
csv_writer = csv.writer(write_file, dialect='myDialect1')

csv_writer.writerow(["Product Name", "Sku", "Price", "Detail URL", "Image URL"])

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
   	'Content-Type': 'application/json; charset=UTF-8',
   	'Cookie': 'ASP.NET_SessionId=m0tkyrefjpay0ifomoejx3um; dynamicServiceSessionId=guestuser25da63b1-9eb2-42f5-85d6-f3b0a8fee4df; PersonalisationEmail=guestuser25da63b1-9eb2-42f5-85d6-f3b0a8fee4df; cto_lwid=86b861f8-6d35-4079-b64d-102eb964066d; _ga=GA1.3.994528128.1572081686; _gid=GA1.3.1242551442.1572081686; __zlcmid=uxidjklOp4JYI5; _gat_UA-30111-5=1; _gali=widget-infinite-Scrolling-253db766-9070-4301-8286-e624ad8e9451',
   	'X-Requested-CV': '_token',
	'X-Requested-With': 'XMLHttpRequest'

})
baseurl = 'https://www.mannys.com.au'
url = 'https://www.mannys.com.au/service/storeLocator/setUserCurrentStore?rand=1572081767195'
r = session.post(url, json={"storeName":"Mannys Fitzroy","_sessionId":"guestuser25da63b1-9eb2-42f5-85d6-f3b0a8fee4df","_applicationType":"cssnet"})

r = session.get(baseurl)
soup = BeautifulSoup(r.text, features="html.parser")
categories = soup.findAll('div', class_='dropdown-column')
flag = False
for category in categories:
	for product_page in category.findAll('li'):
		rurl = baseurl + product_page.find('a').attrs['href']
		print(rurl)
		# f = open('1.html', 'a')
		# f.write(r.text)
		# f.close()
		# r = session.get(rurl)
		# soup = BeautifulSoup(r.text, features="html.parser")
		# subcategories = soup.find('div', class_='subcategory-tiles').findAll('a')
		# for subcategory in subcategories:
		# 	rawUrl = baseurl + subcategory.attrs['href']
		# 	print(rawUrl)
		# 	pagecount = 1
		# 	# r = session.get(rawUrl)
		# 	# soup = BeautifulSoup(r.text, features="html.parser")
		# 	# count = int(soup.find('span', class_='widget-product-list-totals').attrs['data-record-count']) - 1
		# 	# pg = count / 24 + 1
			
		# 	# print(pg)
		broken_url = 'https://www.mannys.com.au/keyboards/workstation-keyboards'
		if rurl == broken_url:
			flag = True
		if rurl != broken_url and flag == False:
			continue
		pagecount = 1
		while pagecount > 0:
			url = 'https://www.mannys.com.au/service/products/GetInfiniteScrollingProducts?rand=1572081838281'
			r = session.post(url, json={
				'pageNumber': pagecount,
				'pageSizeArg': 24,
				'rawUrl': rurl,
				'templateName': "Product List Item Zoned",
				'_applicationType': "cssnet",
				'_sessionId': "guestuser25da63b1-9eb2-42f5-85d6-f3b0a8fee4df"
				})
			# soup = BeautifulSoup(r.text, features="html.parser")
			# print(json.loads(json.loads(r.text)['data']['productImpressions']))
			print(len(json.loads(r.text)['data']['result']))
			if len(json.loads(r.text)['data']['result']) == 0:
				break
			for product in json.loads(r.text)['data']['result']:
				soup = BeautifulSoup(product, features="html.parser")
				link = soup.findAll('a')[1]
				name = link.text
				detail = baseurl + link.attrs['href']
				sku = link.attrs['data-product-link']
				image = baseurl + soup.find('img', class_='product-img').attrs['data-image-src']
				price = soup.find('span', class_='item-price').text
				print(detail, sku, image, name, price)
				csv_writer.writerow([name, sku, price, detail, image])
			pagecount = pagecount + 1