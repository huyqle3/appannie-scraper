from bs4 import BeautifulSoup
import urllib2
import json
import argparse

response = urllib2.urlopen("http://www.appannie.com/apps/ios/top/?device=iphone").read()
print(response)

data = {1: "a", 2: "b", 3: "c"}

with open("iphone-data.json", "w") as output:
	json.dump(data, output)
