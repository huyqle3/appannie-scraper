"""
iphone-full-scraper.py
Python script that collects AppAnnie iOS iPhone data from website.
"""

from bs4 import BeautifulSoup
import requests
from requests import session
import cookielib

from datetime import datetime, timedelta
import random
import urllib2
import json
import sys
import argparse
import time

"""
Arguments
"""
current_date = datetime.now().strftime('%Y-%m-%d')
default_end_date = datetime.now() - timedelta(days=1)

parser = argparse.ArgumentParser(description='Scrape AppAnnie rankings at a certain date.')
parser.add_argument("--date", nargs='?', default=current_date, help="Enter date")
parser.add_argument("--end_date", nargs='?', default=default_end_date.strftime('%Y-%m-%d'), help="Enter date")
parser.add_argument("--input_file", nargs='?', default="", help="Enter file")

args = parser.parse_args()

if args.input_file:
	print("File ingested: " + args.input_file)
	json_file = open(args.input_file)
	json_str = json_file.read()
	json_data = json.loads(json_str.encode('ascii', 'ignore'))

def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format. Should be YYYY-MM-DD")

validate(args.date)
validate(args.end_date)

check_date = datetime.strptime(args.date, '%Y-%m-%d')

"""
login_url is required to be able to access AppAnnie app store information
"""
login_url = 'https://www.appannie.com/account/login/'

"""
Sample headers to send with get and post requests.
"""
headers3={'Referer': 'https://www.appannie.com/account/login/',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}

headers4={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}

"""
client is to visit login url and collect the csrftoken.
"""
client = requests.session()
login = client.get(login_url, headers=headers3)
og_soup = BeautifulSoup(login.text, "html.parser")
if "captcha" in (login.text).encode('ascii', 'ignore'):
	print("Captcha required. Log-in failed.")
	sys.exit(0)
else:
	print('Login should have succeeded. Proceeding.')
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
login_post = client.post(login_url, data=payload, headers=headers3)
print("Login response is: " + str(login_post.status_code))

"""
Example link to print and see if loaded
"""

if not args.input_file:
	apps = {}
else:
	apps = json_data

"""
example = client.get("https://www.appannie.com/apps/ios/app/1052231801/", headers=headers3)
print((example.text).encode('ascii', 'ignore'))
"""
def parse_detailed_metadata(row4, app_name):
	deep_metadata_count = 0
	if(row4.get('href').startswith("/apps/ios/app/")):
		random_float = random.uniform(8, 11)
		print("App page found. Waiting " + str(random_float) + " seconds before GET request to app page.")
		time.sleep(random_float)

		try:
			r2 = client.get("https://www.appannie.com" + row4.get('href'), headers=headers4)
		except requests.exceptions.ConnectionError as e:
			with open('iphone-data-' + args.date + '.json', 'w') as output:
				json.dump(apps, output)
			print("Connection errored out. Saved contents to JSON file.")

		soup2 = BeautifulSoup(r2.text, "html.parser")

		if (r2.status_code == 403):
			print("App page received a: " + str(r2.status_code) + " on date, " + check_date.strftime('%Y-%m-%d'))
			print((row4.get('href')).encode('ascii', 'ignore'))
			with open('iphone-data-' + args.date + '.json', 'w') as output:
				json.dump(apps, output)
			sys.exit(0)
		
		# print(r2.text).encode('ascii', 'ignore')
		if(((r2.text).encode('ascii', 'ignore')).startswith('<!DOCTYPE html>\n<html lang="en" xmlns:og="http://ogp.me/ns#">')):
			print("Incorrect app page without the right information on date, " + check_date.strftime('%Y-%m-%d') + ". Something must have gone wrong.")
			with open('iphone-data-' + args.date + '.json', 'w') as output:
				json.dump(apps, output)
			sys.exit(0)
		else:
			print("App page: " + (row4.get('href')).encode('ascii', 'ignore') + " hit correctly.")

		if(not soup2.find_all('div', class_=["app_slide_content", "app_slide_header"])):
			print("No featured info or ratings exist " + check_date.strftime('%Y-%m-%d') + ". Writing to JSON and continuing.")
			with open('iphone-data-' + args.date + '.json', 'w') as output:
				json.dump(apps, output)
			return

		for row5 in soup2.find_all('div', class_=["app_slide_content", "app_slide_header"]):
			# print((row5.text).encode('ascii', 'ignore'))
			metadata = (row5.text).encode('ascii', 'ignore')
			parsed_metadata = (metadata.replace('\r', '')).split()
			if not parsed_metadata:
				continue
			if deep_metadata_count == 1:
				if len(parsed_metadata) >= 8:
					apps[app_name].update({"Featured in iPhone Market": {"iTunes Home Page": parsed_metadata[0], "iTunes": parsed_metadata[7]}})
			if deep_metadata_count == 3:
				if len(parsed_metadata) >= 8:
					apps[app_name].update({"Featured in iPad Market": {"iTunes Home Page": parsed_metadata[0], "iTunes": parsed_metadata[7]}})
			if deep_metadata_count == 4:
				current_version = parsed_metadata[3]
				apps[app_name].update({"Current Version": {current_version: {"average": parsed_metadata[3], "total_ratings": parsed_metadata[5]}}})
			if deep_metadata_count == 5:
				apps[app_name].update({"Current Version": {current_version: {"five_star": parsed_metadata[0], "four_star": parsed_metadata[1],
					"three_star": parsed_metadata[2], "two_star": parsed_metadata[3], "one_star": parsed_metadata[4]}}})
			if deep_metadata_count == 6:
				apps[app_name].update({"Overall Ratings": {"average": parsed_metadata[3], "total_ratings": parsed_metadata[5]}})
			if deep_metadata_count == 7:
				apps[app_name].update({"Overall Ratings": {"five_star": parsed_metadata[0], "four_star": parsed_metadata[1],
					"three_star": parsed_metadata[2], "two_star": parsed_metadata[3], "one_star": parsed_metadata[4]}})	
			deep_metadata_count += 1

		for row5 in soup2.find_all('div', class_="app-box-content"):
			for row6 in row5.find_all('p'):
				if((row6.text).startswith("Category")):
					divided = ((row6.text).encode('ascii', 'ignore')).split(': ')
					# print((row6.text).encode('ascii', 'ignore'))
					apps[app_name].update({"Category": divided[1]})
					# print(divided)
				if((row6.text).startswith("Updated")):
					divided = (row6.text).split(': ')
					# print((row6.text).encode('ascii', 'ignore'))
					apps[app_name].update({"Last Updated": divided[1]})
					# print(divided)

"""
Check iPhone top 100 page for free, paid, and grossing. Exit if 404.
"""
while(check_date != datetime.strptime(args.end_date, '%Y-%m-%d')):
	print(check_date.strftime('%Y-%m-%d'))
	r = client.get("https://www.appannie.com/apps/ios/top/?_ref=header&device=iphone&date=" + check_date.strftime('%Y-%m-%d'), headers=headers4, allow_redirects=False)
	if (r.status_code == 403):
		print("Date page received a: " + str(r.status_code) + " on date, " + check_date.strftime('%Y-%m-%d'))
		with open('iphone-data-' + args.date + '.json', 'w') as output:
			json.dump(apps, output)
		sys.exit(0)
	else:
		print("GET request " + check_date.strftime('%Y-%m-%d') + " url proceeded correctly.")

	soup = BeautifulSoup(r.text, "html.parser")
	# print((soup.text).encode('ascii', 'ignore'))

	"""
	Load the order of Free, Paid, Grossing, and order of ranks.
	"""
	category = ["Free", "Paid"]
	app_or_publisher = ["App", "Publisher"]
	ap_position = 0

	rank_counter = [1, 1]
	position = 0

	if(not soup.find_all('tr', class_=["odd", "even"])):
		print("Captcha requested on date page. Date failed on " + check_date.strftime('%Y-%m-%d') + ". Writing to JSON and stopping.")
		with open('iphone-data-' + args.date + '.json', 'w') as output:
			json.dump(apps, output)
		sys.exit(0)

	"""
	Parse the ranking list of iPhone page for top 100.
	"""
	for row in soup.find_all('tr', class_=["odd", "even"]):
		for row2 in row.find_all('div', class_="main-info"):
			# print(row2)
			if(position == 2):
				print("About to break.")
				position = 0
				break

			for row3 in row2.find_all('span', class_="oneline-info"):
				row4 = row3.find_all('a')[0]
				# print(row4)

				if(ap_position == 0):
					app_name = (row4.text).encode('ascii', 'ignore')
					if(app_name in apps):
						print(app_name + " matched.")
						if("Current Version" not in apps[app_name]):
							parse_detailed_metadata(row4, app_name)
						# (apps[app_name])["Ranking"].update({check_date.strftime('%Y-%m-%d'): rank_counter[position]})
						rank_counter[position] += 1
						position += 1
						break

					else:
						apps[app_name] = {}
						parse_detailed_metadata(row4, app_name)
						apps[app_name].update({"App Link": (row4.get('href')).encode('ascii', 'ignore')})
						apps[app_name].update({"Type": category[position]})
						apps[app_name].update({"Ranking": {check_date.strftime('%Y-%m-%d'): rank_counter[position]}})
					ap_position += 1

				else:
					if(app_name not in apps):
						apps[app_name].update({"Publisher": (row4.text).encode('ascii', 'ignore')})
						apps[app_name].update({"Publisher Link": (row4.get('href')).encode('ascii', 'ignore')})
					ap_position = 0

				if(ap_position == 0):
					rank_counter[position] += 1
					position += 1

	check_date -= timedelta(days=1)

with open('iphone-data-' + args.date + '.json', 'w') as output:
	json.dump(apps, output)

