from bs4 import BeautifulSoup
import urllib2
import json

response = urllib2.urlopen("http://huyle.me").read()
print(response)

data = {1: "a", 2: "b", 3: "c"}

with open("iphone-data.json", "w") as output:
	json.dump(data, output)

print("Hello")
