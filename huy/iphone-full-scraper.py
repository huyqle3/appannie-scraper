"""
iphone-full-scraper.py
Python script that collects AppAnnie iOS iPhone data from website.
"""

from bs4 import BeautifulSoup
import requests
from requests import session
import cookielib

from datetime import datetime
import urllib2
import json
import sys
import argparse

"""
Arguments
"""
current_date = datetime.now().strftime('%Y-%m-%d')

parser = argparse.ArgumentParser(description='Scrape AppAnnie rankings at a certain date.')
parser.add_argument("--date", nargs='?', default=current_date, help="Enter date")

args = parser.parse_args()

def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format. Should be YYYY-MM-DD")

validate(args.date)
print(args.date)

"""
login_url is required to be able to access AppAnnie app store information
"""
login_url = 'https://www.appannie.com/account/login/'

"""
Sample headers to send with get and post requests.
"""
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

headers3={'Referer': 'https://www.appannie.com/account/login/',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}

"""
client is to visit login url and collect the csrftoken.
"""
client = requests.session()
login = client.get(login_url, headers=headers)
og_soup = BeautifulSoup(login.text, "html.parser")
if "captcha" in (login.text).encode('ascii', 'ignore'):
	print("Captcha required. Log-in failed.")
	sys.exit(0)
# print((login.text).encode('ascii', 'ignore'))

csrf_token = og_soup.find("input", value=True)["value"]

"""
Create a creds.txt file in the directory.
Put username on the first line.
And put password on the second line.
"""
with open('creds.txt') as f:
	credentials = [x.strip('\n') for x in f.readlines()]
username = credentials[0]
password = credentials[1]

"""
Testing example iphone page, parsing for information that requires username and password.
"""

# app_name = {}

# Example structure
"""
app_metadata = {"Ranking": 
{"2015-12-02": 72},
"Current Version Ratings": {
	"4.0": {
		"total ratings": "2730",
		"average": "4.2",
		"five_star": "1920",
		"four_star": "500",
		"three_star": "250",
		"two_star": "50",
		"one_star": "10"
	}
},
"Overall Ratings": {
	"total ratings": "5620",
	"average": "4.5",
	"five_star": "4000",
	"four_star": "1000",
	"three_star": "500",
	"two_star": "100",
	"one_star": "20"
},
"Featured in iPhone Market": {
	"iTunes Home Page": "10",
	"iTunes": "33"
},
"Category": "Games",
"Last Updated": "2015-11-12",
"Publisher": "Zynga Inc.",
"Type": "Grossing",
"Publisher Link":
"/apps/ios/publisher/zynga-inc./",
"App Link": "/apps/ios/app/empires-allies/"}
"""
"""
app_ranking = {"Ranking": 
{"2015-12-02": 72}}

app_metadata = {"Publisher": "Zynga Inc.",
"Type": "Grossing",
"Publisher Link":
"/apps/ios/publisher/zynga-inc./",
"App Link": "/apps/ios/app/empires-allies/"}

app_metadata.update(app_ranking)

with open ("example.txt", "r") as iphone_example:
    example_html = iphone_example.read().replace('\n', '')
soup2 = BeautifulSoup(example_html, "html.parser")

app_name.update({"Empires & Allies": app_metadata})
deep_metadata_count = 0

if "Empires & Allies" in app_name:
	for row5 in soup2.find_all('div', class_=["app_slide_content", "app_slide_header"]):
		# print((row.text).encode('ascii', 'ignore'))
		metadata = (row5.text).encode('ascii', 'ignore')
		parsed_metadata = (metadata.replace('\r', '')).split()
		if deep_metadata_count == 1:
			app_metadata.update({"Featured in iPhone Market": {"iTunes Home Page": parsed_metadata[0], "iTunes": parsed_metadata[7]}})
		if deep_metadata_count == 3:
			app_metadata.update({"Featured in iPad Market": {"iTunes Home Page": parsed_metadata[0], "iTunes": parsed_metadata[7]}})
		if deep_metadata_count == 4:
			current_version = parsed_metadata[3]
			app_metadata.update({"Current Version": {current_version: {"average": parsed_metadata[3], "total_ratings": parsed_metadata[5]}}})
		if deep_metadata_count == 5:
			app_metadata.update({"Current Version": {current_version: {"five_star": parsed_metadata[0], "four_star": parsed_metadata[1],
				"three_star": parsed_metadata[2], "two_star": parsed_metadata[3], "one_star": parsed_metadata[4]}}})
		if deep_metadata_count == 6:
			app_metadata.update({"Overall Ratings": {"average": parsed_metadata[3], "total_ratings": parsed_metadata[5]}})
		if deep_metadata_count == 7:
			app_metadata.update({"Overall Ratings": {"five_star": parsed_metadata[0], "four_star": parsed_metadata[1],
				"three_star": parsed_metadata[2], "two_star": parsed_metadata[3], "one_star": parsed_metadata[4]}})	
		deep_metadata_count += 1

	deep_metadata_count = 0

	for row5 in soup2.find_all('div', class_="app-box-content"):
		for row6 in row5.find_all('p'):
			if((row6.text).startswith("Category")):
				divided = ((row6.text).encode('ascii', 'ignore')).split(': ')
				# print((row6.text).encode('ascii', 'ignore'))
				app_metadata.update({"Category": divided[1]})
				# print(divided)
			if((row6.text).startswith("Updated")):
				divided = (row6.text).split(': ')
				# print((row6.text).encode('ascii', 'ignore'))
				app_metadata.update({"Last Updated": divided[1]})
				# print(divided)

app_name.update({"Empires & Allies": app_metadata})
print(app_name)
"""

"""
We log in with this payload dictionary.
"""
payload = {
	'csrfmiddlewaretoken': csrf_token,
	'next': '/dashboard/home/',
	'username': username,
	'password': password
}

"""
We send a post request to login.
"""
client.post(login_url, data=payload, headers=headers3)

"""
Example link to print and see if loaded
"""
"""
example = client.get("https://www.appannie.com/apps/ios/app/1052231801/", headers=headers3)
print((example.text).encode('ascii', 'ignore'))
"""

"""
Check iPhone top 100 page for free, paid, and grossing. Exit if 404.
"""
r = requests.get("https://www.appannie.com/apps/ios/top/?_ref=header&device=iphone&date=" + args.date, headers=headers3)
if (r.status_code == 403):
	print(r.status_code)
	sys.exit(0)
soup = BeautifulSoup(r.text, "html.parser")
# print((soup.text).encode('ascii', 'ignore'))

"""
Load the order of Free, Paid, Grossing, and order of ranks.
"""
category = ["Free", "Paid", "Grossing"]
app_or_publisher = ["App", "Publisher", "Test"]
ap_position = 0

rank_counter = [1, 1, 1]
position = 0

switch = 1
test = 1

apps = {}

"""
Parse the ranking list of iPhone page for top 100.
"""
for row in soup.find_all('tr', class_=["odd", "even"]):
	for row2 in row.find_all('div', class_="main-info"):
		app_ranking = {}
		app_metadata = {}
		# print(row2)
		for row3 in row2.find_all('span', class_="oneline-info"):
			for row4 in row3.find_all('a'):
				# print(row4)
				if(switch == 1):
					# print(category[position])
					app_metadata.update({"Type": category[position]})
					# print(rank_counter[position])
					app_ranking.update({args.date: rank_counter[position]})
					app_metadata.update({"Ranking": app_ranking})
					switch = 0
				else:
					switch = 1

				if(ap_position == 0):
					app_name = (row4.text).encode('ascii', 'ignore')
					app_metadata.update({"App Link": (row4.get('href')).encode('ascii', 'ignore')})
					# print(apps)
					apps.update({app_name: app_metadata})
					ap_position += 1
				else:
					app_metadata.update({"Publisher": (row4.text).encode('ascii', 'ignore')})
					app_metadata.update({"Publisher Link": (row4.get('href')).encode('ascii', 'ignore')})
					ap_position = 0

				if(app_name in apps):
					deep_metadata_count = 0
					if(row4.get('href').startswith("/apps/ios/app/") and test == 1):
						r2 = client.get("https://www.appannie.com" + row4.get('href'), headers=headers3)
						soup2 = BeautifulSoup(r2.text, "html.parser")
						print(r2.text).encode('ascii', 'ignore')

						for row5 in soup2.find_all('div', class_=["app_slide_content", "app_slide_header"]):
							# print((row5.text).encode('ascii', 'ignore'))
							metadata = (row5.text).encode('ascii', 'ignore')
							parsed_metadata = (metadata.replace('\r', '')).split()
							if deep_metadata_count == 1:
								app_metadata.update({"Featured in iPhone Market": {"iTunes Home Page": parsed_metadata[0], "iTunes": parsed_metadata[7]}})
							if deep_metadata_count == 3:
								app_metadata.update({"Featured in iPad Market": {"iTunes Home Page": parsed_metadata[0], "iTunes": parsed_metadata[7]}})
							if deep_metadata_count == 4:
								current_version = parsed_metadata[3]
								app_metadata.update({"Current Version": {current_version: {"average": parsed_metadata[3], "total_ratings": parsed_metadata[5]}}})
							if deep_metadata_count == 5:
								app_metadata.update({"Current Version": {current_version: {"five_star": parsed_metadata[0], "four_star": parsed_metadata[1],
									"three_star": parsed_metadata[2], "two_star": parsed_metadata[3], "one_star": parsed_metadata[4]}}})
							if deep_metadata_count == 6:
								app_metadata.update({"Overall Ratings": {"average": parsed_metadata[3], "total_ratings": parsed_metadata[5]}})
							if deep_metadata_count == 7:
								app_metadata.update({"Overall Ratings": {"five_star": parsed_metadata[0], "four_star": parsed_metadata[1],
									"three_star": parsed_metadata[2], "two_star": parsed_metadata[3], "one_star": parsed_metadata[4]}})	
							deep_metadata_count += 1

						for row5 in soup2.find_all('div', class_="app-box-content"):
							for row6 in row5.find_all('p'):
								if((row6.text).startswith("Category")):
									divided = ((row6.text).encode('ascii', 'ignore')).split(': ')
									# print((row6.text).encode('ascii', 'ignore'))
									app_metadata.update({"Category": divided[1]})
									# print(divided)
								if((row6.text).startswith("Updated")):
									divided = (row6.text).split(': ')
									# print((row6.text).encode('ascii', 'ignore'))
									app_metadata.update({"Last Updated": divided[1]})
									# print(divided)

						apps.update({app_name: app_metadata})
						test = 0

				if(switch == 1):
					rank_counter[position] += 1
					position += 1
					if (position == 3):
						position = 0
		# apps.update({app_name: app_metadata})
		# print(app_metadata)

print(apps)

"""
with open('iphone-data-' + args.date + '.json', 'w') as output:
	json.dump(apps, output)
"""
