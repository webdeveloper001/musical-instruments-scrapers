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


# csv.register_dialect('myDialect1',
# 	  quoting=csv.QUOTE_ALL,
# 	  skipinitialspace=True)

# write_file = open('armorall/products.csv', 'a')
# csv_writer = csv.writer(write_file, dialect='myDialect1')

# csv_writer.writerow(["Date Added", "File Name", "File Type"])

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
url = 'https://www.ghmusic.com.au/drums/?pgnum={}'
pgcount = 1
while pgcount > 0:

	r = session.get(url.format(pgcount))
	soup = BeautifulSoup(r.text, features="html.parser")
	print(r.text)
	products = soup.findAll('article', class_='wrapper-thumbnail')
	print(len(products))
	pgcount = pgcount + 1
# categories = soup.findAll('div', class_='col-md-4')
# for category in categories:
# 	print(category.find('a').attrs['href'])
# 	r = session.get(baseurl + category.find('a').attrs['href'])
# 	soup = BeautifulSoup(r.text, features="html.parser")
# 	products = soup.findAll('div', class_='col-xs-6')
# 	for product in products:
# 		print(product.find('a').attrs['href'])
# 		name = product.find('div', class_='caption').text.replace('/', '-').strip()
# 		r = session.get(baseurl + product.find('a').attrs['href'])
# 		soup = BeautifulSoup(r.text, features="html.parser")
# 		date_added = datetime.strftime(datetime.now(),'%d-%m-%Y')

# 		if len(soup.findAll('div', class_='product-img')) > 0:
# 			image = soup.findAll('div',class_='product-img')[0].find('img').attrs['src']
# 			urllib.urlretrieve(image, 'armorall/images/Armorall ' + name + ' - Bottle Image Front.png')
# 			image = 'Armorall ' + name + ' - Bottle Image Front.png'
# 			print(date_added, image, 'Front')
# 			csv_writer.writerow([date_added, image, 'Front'])

# 		if len(soup.findAll('a', class_='products_link_footer')) > 0:
# 			sds = soup.findAll('a', class_='products_link_footer')[0].attrs['href']
# 			urllib.urlretrieve(sds, 'armorall/images/Armorall ' + name + ' - SDS Sheet.pdf')
# 			sds = 'Armorall ' + name + ' - SDS Sheet.pdf'
# 			print(date_added, sds, 'SDS')
# 			csv_writer.writerow([date_added, sds, 'SDS'])
		
