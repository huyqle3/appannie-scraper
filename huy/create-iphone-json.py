from bs4 import BeautifulSoup
import requests
from requests import session
import cookielib

import urllib2
import json
import argparse

# response = urllib2.urlopen('http://www.appannie.com/apps/ios/top/?device=iphone').read()
# print(response)

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, sdch',
			'Accept-Language': 'en-US,en;q=0.8',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Cookie': '_gat_UA-2339266-6=1; _ga=GA1.2.2005558127.1448218987; __atuvc=1%7C47; __atuvs=5652116ad4ee2cdc000; _bizo_bzid=a8a8831e-2acb-4ec6-983e-8443f0d31fbe; _bizo_cksm=1C616CA57234E187; _bizo_np_stats=6256%3D13%2C14%3D116%2C; kvcd=1448218988017; km_ai=xBlsQFF8sWsDyn0nW70d7JkxCuA%3D; km_vs=1; km_lv=1448218988; km_uq=; csrftoken=RcD2mWqu6paVHVULOGIFPxwQGEBDwsXp; sessionId=".eJxrYKotZNQI5S9OLS7OzM-LT81LTMpJTfFmChVIzEktKolPzkhNzo4vycxNLWRKTkksSQUxueCMQuZQLvb73GLCzNz8Iv3JBZUlVVzxoSHOXIUsmkGFrG1BhWyh3CX5xfGlBSA9KYXsnaV6ABAVJoA:1a0Zuq:LhvRm7iqf-4FV5Whb7pSi5jnEXk"',
			'Host': 'www.appannie.com',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}

headers2={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, sdch',
			'Accept-Language': 'en-US,en;q=0.8',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Cookie': 'km_ai=xBlsQFF8sWsDyn0nW70d7JkxCuA%3D; __atuvc=2%7C47; optimizelyEndUserId=oeu1448231620985r0.5221775402314961; aa_language=en; km_lv=x; optimizelySegments=%7B%222069170486%22%3A%22false%22%2C%222083860069%22%3A%22gc%22%2C%222083940003%22%3A%22direct%22%2C%223519320656%22%3A%22none%22%7D; optimizelyBuckets=%7B%7D; _gat_UA-2339266-6=1; sessionId=".eJxrYKotZNQI5S9OLS7OzM-LT81LTMpJTfFmChVIzEktKolPzkhNzo4vycxNTU5JLEkFMbjgjEKmUC72-9ziDAyMbFe4kgsqS6q44kNDnLkKmTWDClnaggpZQ7lL8ovjSwtAelIK2TpL9QDSriYb:1a0eY5:2FJP8LcGus3Jex6zsS0Ak28YeRE"; csrftoken=RcD2mWqu6paVHVULOGIFPxwQGEBDwsXp; _bizo_bzid=a8a8831e-2acb-4ec6-983e-8443f0d31fbe; _bizo_cksm=1D39B6DA9F55EE10; _bizo_np_stats=6256%3D98%2C6256%3D97%2C14%3D97%2C; kvcd=1448236822484; km_vs=1; km_uq=; _ga=GA1.2.2005558127.1448218987',
			'Host': 'www.appannie.com',
			'Origin': 'https://www.appannie.com',
			'Referer': 'https://www.appannie.com/account/login/',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}

URL = 'https://www.appannie.com/account/login/'

client = requests.session()
login = client.get(URL, headers=headers)
og_soup = BeautifulSoup(login.text, "html.parser")
csrftoken = og_soup.find("input", value=True)["value"]

with open('creds.txt') as f:
	credentials = [x.strip('\n') for x in f.readlines()]

username = credentials[0]
password = credentials[1]

payload = {
	'csrfmiddlewaretoken': csrftoken,
	'next': '/',
	'username': username,
	'password': password
}

r = requests.get("https://www.appannie.com/apps/ios/top/?device=iphone", headers=headers)

client.post(URL, data=payload, headers={'Referer': "https://www.appannie.com/account/login/", 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'})

r5 = client.get("https://www.appannie.com/apps/ios/app/1052231801/", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'})
print((r5.text).encode('ascii', 'ignore'))

soup = BeautifulSoup(r.text, "html.parser")

category = ["Free", "Paid", "Grossing"]
rank_counter = [1, 1, 1]
position = 0

switch = 1
test = 1

apps = {}

for row in soup.find_all('tr', class_=["odd", "even"]):
	for row2 in row.find_all('div', class_="main-info"):
		for row3 in row2.find_all('span', class_="oneline-info"):
			for row4 in row3.find_all('a'):
				if(switch == 1):
					print(category[position])
					print(rank_counter[position])
					switch = 0
				else:
					switch = 1
				print((row4.text).encode('ascii', 'ignore'))
				print(row4.get('href'))

				if(row4.get('href').startswith("/apps/ios/app/") and test == 1):
					r2 = requests.get("https://www.appannie.com" + row4.get('href'), headers=headers)
					soup2 = BeautifulSoup(r2.text, "html.parser")

					"""
					for row in soup2.find_all('div'):
						print(row)
					"""

					# print((r2.text).encode('ascii', 'ignore'))
					test = 0

				if(switch == 1):
					rank_counter[position] += 1
					position += 1
					if (position == 3):
						position = 0

# print(soup.prettify())

data = {1: 'a', 2: 'b', 3: 'c'}

with open('iphone-data.json', 'w') as output:
	json.dump(data, output)
