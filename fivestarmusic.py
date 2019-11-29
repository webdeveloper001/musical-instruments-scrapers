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

write_file = open('fivestarmusic.csv', 'a')
csv_writer = csv.writer(write_file, dialect='myDialect1')

csv_writer.writerow(["Product Name", "Sku", "Price", "Detail URL", "Image URL"])

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'cookie': '__cfduid=d6553e5bdd686e1d76aadc0dd0f34c90d1572040543; __cfruid=f41f912989b9ae2af46131961299c634d31bcb89-1572040543; ninfo_geoloc=%7B%22ship_pobox%22%3A%22n%22%2C%22ship_state%22%3Anull%2C%22ship_country%22%3A%22AU%22%2C%22ship_zip%22%3Anull%2C%22ship_city%22%3Anull%7D; ninfo_view=NSD1%3B%231%7C%245%7Cnview%240%7C; N064179_main_sess=2092a34b4c6e9b9061263ad8d0e27175; _ga=GA1.3.1584428312.1572040572; _gid=GA1.3.537956367.1572040572; _fbp=fb.2.1572040573911.657829587; studio19-cart-count=0; __zlcmid=uwidfGWtTfFE4K; __cf_bm=db094977cc9eb25dca18d02b393629ef735567d6-1572041507-1800-Aa2alPQMRz3iyQXGffDFeYUNkxmDpJzTiIZwg6/F9dtM+bxEq4w8ateidxvXuTOwVDlYs2IJZDgYWp6h+wEVs2Y=',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'sec-fetch-mode': 'navigate',
	'sec-fetch-site': 'none',
	'sec-fetch-user': '?1',
	'upgrade-insecure-requests': '1'
})
category_pages = [
	'https://fivestarmusic.com.au/product-category/guitars/',
	'https://fivestarmusic.com.au/product-category/amps/',
	'https://fivestarmusic.com.au/product-category/bluegrass/',
	'https://fivestarmusic.com.au/product-category/effects/',
	'https://fivestarmusic.com.au/product-category/drums-percussion/',
	'https://fivestarmusic.com.au/product-category/keys-synths/'
]

for category in category_pages:
	r = session.get(category)
	soup = BeautifulSoup(r.text, features="html.parser")
	for product_page in soup.findAll('li', class_='product-category'):
		url = product_page.find('a').attrs['href']
		print(url)
		baseurl = '{}/page/{}/'
		pgcount = 1
		while pgcount > 0:
			print(pgcount)
			r = session.get(baseurl.format(url, pgcount))
			soup = BeautifulSoup(r.text, features="html.parser")
			# print(r.text)
			products = soup.findAll('li', class_='product')
			for product in products:
				link = product.findAll('a')
				# print(link)
				detail = link[0].attrs['href']
				sku = ''
				if len(link) > 1:
					sku = link[1].attrs['data-product_sku'];
				price = ''
				if product.find('span', class_='woocommerce-Price-amount amount'):
					price = product.find('span', class_='woocommerce-Price-amount amount').text
				name = ''
				if product.find('h2', class_='woocommerce-loop-product__title'):
					name = product.find('h2', class_='woocommerce-loop-product__title').text;
				image = ''
				if product.find('img', class_='size-shop_catalog'):
					image = product.find('img', class_='size-shop_catalog').attrs['src']
				print(name, image, detail, price, sku)
				csv_writer.writerow([name, sku, price, image, detail])
			print(len(products))
			if len(products) == 0:
				break
			pgcount = pgcount + 1
