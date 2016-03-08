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
parser.add_argument("--input_file", nargs='?', default="iphone-data-2015-12-05.json", help="Enter file")

args = parser.parse_args()

print(args.input_file)
json_file = open(args.input_file)
json_str = json_file.read()
json_data = json.loads(json_str.encode('ascii', 'ignore'))

apps = json_data

app_ranking = {}
app_name = "Facebook"
app_ranking.update({current_date: 5})
if(app_name in apps):
	print(app_name + " matched.")
	app_name_contents = apps[app_name]
	if("Ranking" in app_name_contents):
		app_name_contents["Ranking"].update(app_ranking)
	else:
		app_metadata.update({"Ranking": app_ranking})
else:
	app_metadata.update({"Ranking": app_ranking})

with open('test.json', 'w') as output:
	json.dump(apps, output)