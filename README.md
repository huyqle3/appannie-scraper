# appannie-scraper

Scripts to scrape AppAnnie for their mobile app data.

### Dependencies

1. Beautifulsoup 4
2. requests

```
curl https://bootstrap.pypa.io/get-pip.py | python
pip install beautifulsoup4
pip install requests
```

### Steps

1. Create creds.txt inside huy folder
2. Running the scripts

### Create creds.txt inside huy folder
Put the AppAnnie username and password line by line.

```
username@email.com
password
```

### Running the data collection scripts (inside huy folder)
iphone-full-scraper.py grabs full detailed metadata from specified dates.
iphone-ranking-scraper.py grabs rankings from specified dates.

iphone-full-scraper.py

Example: The script takes the data already existing in iphone-ranking-from-2015-12-09-to-2015-06-08. It creates a JSON file with data from 2015-12-11 (inclusive) to 2015-11-11 (non-inclusive).
```
python iphone-full-scraper.py --date 2015-12-11 --end_date 2015-11-11 --input_file iphone-ranking-from-2015-12-09-to-2015-06-08.json
```

iphone-ranking-scraper.py

Example:
Creates today's app iphone ranking data into a JSON file.
```
python iphone-ranking-scraper.py
```