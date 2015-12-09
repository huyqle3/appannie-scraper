"""
iphone-ranking-scraper.py
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
parser.add_argument("--input_file", nargs='?', default="iphone-one-day-12-08.json", help="Enter file")

args = parser.parse_args()

print(args.input_file)
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
"""
example = client.get("https://www.appannie.com/apps/ios/app/1052231801/", headers=headers3)
print((example.text).encode('ascii', 'ignore'))
"""
apps = json_data

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
	category = ["Free", "Paid", "Grossing"]
	app_or_publisher = ["App", "Publisher", "Test"]
	ap_position = 0

	rank_counter = [1, 1, 1]
	position = 0

	switch = 1
	test = 1

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

					if(ap_position == 0):
						app_name = (row4.text).encode('ascii', 'ignore')
						app_metadata.update({"App Link": (row4.get('href')).encode('ascii', 'ignore')})

						if(switch == 1):
							# print(category[position])
							app_metadata.update({"Type": category[position]})
							# print(rank_counter[position])
							app_ranking.update({check_date.strftime('%Y-%m-%d'): rank_counter[position]})
							if(app_name in apps):
								print(app_name + " matched.")
								app_name_contents = apps[app_name]
								if("Ranking" in app_name_contents):
									app_name_contents["Ranking"].update(app_ranking)
								else:
									app_metadata.update({"Ranking": app_ranking})
							switch = 0
						else:
							switch = 1
						# print(apps)
						# apps.update({app_name: app_metadata})
						ap_position += 1
					else:
						app_metadata.update({"Publisher": (row4.text).encode('ascii', 'ignore')})
						app_metadata.update({"Publisher Link": (row4.get('href')).encode('ascii', 'ignore')})
						ap_position = 0

					if(switch == 1):
						rank_counter[position] += 1
						position += 1
						if (position == 3):
							position = 0
			apps.update({app_name: app_metadata})
			# print(app_metadata)

	# print(apps)
	check_date -= timedelta(days=1)

with open('iphone-ranking-from' + args.date + '-to-' + args.end_date + '.json', 'w') as output:
	json.dump(apps, output)