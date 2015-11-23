# App Annie iPhone analysis
# Huy Le and Scott Woods

import urllib

link = "https://www.appannie.com/apps/ios/top/?device=iphone" 
link_open = urllib.urlopen(link)
my_file = link_open.read()
print(my_file)
