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

write_file = open('bettermusic.csv', 'a')
csv_writer = csv.writer(write_file, dialect='myDialect1')

csv_writer.writerow(["Product Name", "Sku", "Code", "Price", "Detail URL", "Image URL"])

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
})
start_url = 'https://www.bettermusic.com.au'
url = 'https://www.bettermusic.com.au/'
r = session.get(url)
soup = BeautifulSoup(r.text, features="html.parser")
categories = soup.findAll('div', class_='sublevel-menu')
urllist = [
	# 'https://www.bettermusic.com.au/electric-guitars/solid-body-electric',
	# 'https://www.bettermusic.com.au/electric-guitars/7-8-string-electric',
	# 'https://www.bettermusic.com.au/electric-guitars/packages-bundles',
	# 'https://www.bettermusic.com.au/electric-guitars/left-handed-electric',
	# 'https://www.bettermusic.com.au/electric-guitars/pickups',
	# 'https://www.bettermusic.com.au/pre-owned'
	# 'https://www.bettermusic.com.au/sheet-music'
]
flag = False
for category in categories:

	cat_url = category.parent()[0].attrs['href']
	# if cat_url == 'https://www.bettermusic.com.au/electric-guitars':
	# 	continue
	r = session.get(cat_url)
	soup = BeautifulSoup(r.text, features="html.parser")
	for product_page in soup.findAll('div', class_='category-promotion-col'):
		# for url in urllist:
		url = start_url + product_page.findAll('a')[0].attrs['href']
		print(url)
		# broken_url = 'https://www.bettermusic.com.au/bass-guitars/packages-bundles'
		# if url == broken_url:
		# 	flag = True
		# if url != broken_url and flag == False:
		# 	continue
		r = session.get(url)
		soup = BeautifulSoup(r.text, features="html.parser")
		pages = int(soup.find('span', class_='items-results').find('strong').text) / 12 + 1
		base_url = "{}?p={}"
		print(base_url.format(url, pages))
		r = session.get(base_url.format(url, pages))
		soup = BeautifulSoup(r.text, features="html.parser")
		products = soup.find('div', class_='product-list').findAll('li')
		for product in products:
			detail = product.find('a').attrs['href']
			sku = product.find('a').attrs['data-id']
			image = product.find('div', class_='product-img').find('img').attrs['src']
			name = product.find('div', class_='product-details').find('p').text
			r = session.get(detail.format(url, pages))
			soup = BeautifulSoup(r.text, features="html.parser")
			price = soup.find('span', class_='butt-normal').text
			print(soup.find('span', class_='butt-normal').text, soup.find('div', class_='product-info').findAll('span')[0].text.replace('Code', '').strip())
			# price = product.find('div', class_='price').text
			code = soup.find('div', class_='product-info').findAll('span')[0].text.replace('Code', '').strip()
			print(detail, sku, code, image, name, price)
			csv_writer.writerow([name, sku, code, price, detail, image])

