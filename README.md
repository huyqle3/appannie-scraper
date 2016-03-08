# appannie-scraper for iPhone data only

[AppAnnie](https://appannie.com) is an analytics site that contains ratings, reviews, and the top ranking apps for Apple, Android, etc. Our scripts scrape AppAnnie for their iPhone app data. Check the data folder for our results.

### Dependencies

1. Beautifulsoup 4
2. requests

```
curl https://bootstrap.pypa.io/get-pip.py | python
pip install beautifulsoup4
pip install requests
```

### Steps

1. Create creds.txt inside data folder
2. Running the scripts

### Create creds.txt inside data folder
Put the AppAnnie username and password line by line.

```
username@email.com
password
```

### Running the data collection scripts
All the data mining scripts are in the data folder. The three main scripts are iphone-full-scraper.py, iphone-ranking-scraper.py, and iphone-partial-scraper.py.

#### 2 ways of scraping

+ Using iphone-full-scraper.py 
+ Using iphone-partial-scraper.py and then using iphone-ranking-scraper.py 

First, you can use iphone-full-scraper.py to grab all the data that we can collect from AppAnnie.

```
iphone-full-scraper.py
--date (date is the most recent day to respect to today that you want to start collecting)
--end_date (end_date is the earliest day that you want to reach)
--input_file (you can add more data to an existing file that was created from our scripts)
```

Example: The script takes the data already existing in iphone-ranking-from-2015-12-09-to-2015-06-08. It creates a JSON file with data from 2015-12-11 (inclusive) to 2015-11-11 (non-inclusive).
```
python iphone-full-scraper.py --date 2015-12-11 --end_date 2015-11-11 --input_file iphone-ranking-from-2015-12-09-to-2015-06-08.json
```

Second, you can choose to get ranking and metadata separately with the iphone-partial-scraper.py and iphone-ranking-scraper.py.

iphone-partial-scraper.py creates a partial set of metadata.
iphone-ranking-scraper.py creates a day's app iphone ranking only.
Both of these scripts have the same arguments as iphone-full-scraper.py.

Example:
Creates today's app iphone ranking data into a JSON file. Without any arguments, the 3 scripts collect data from the current day.
```
python iphone-ranking-scraper.py
```
