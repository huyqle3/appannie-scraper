#!/usr/local/bin/python3
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta

# Takes in a dictionary of apps, adds the attribute Previous
# Ratings by subtracting Current Version from Overall Ratings
# Returns the modified data
def calcPrevAvg(data):
	delete = []
	for app in data:
		if "Current Version" in data[app]:
			data[app]["Current Version"] = next(iter(data[app]["Current Version"].values()))
			for star in data[app]["Current Version"]:
				if type(data[app]["Current Version"][star]) == str:
					rating = data[app]["Current Version"][star]
					rating = rating.replace(',', '')
					data[app]["Current Version"][star] = int(rating.strip('()'))
			avg = 0
			avg += (data[app]["Current Version"]["one_star"] * 1)
			avg += (data[app]["Current Version"]["two_star"] * 2)
			avg += (data[app]["Current Version"]["three_star"] * 3)
			avg += (data[app]["Current Version"]["four_star"] * 4)
			avg += (data[app]["Current Version"]["five_star"] * 5)
			avg /= sum(data[app]["Current Version"].values())
			data[app]["Current Average"] = avg

			

		if "Overall Ratings" in data[app]:
			for star in data[app]["Overall Ratings"]:
				if type(data[app]["Overall Ratings"][star]) == str:
					rating = data[app]["Overall Ratings"][star]
					rating = rating.replace(',', '')
					data[app]["Overall Ratings"][star] = int(rating.strip('()'))
			avg = 0
			count = 0
			avg += (data[app]["Overall Ratings"]["one_star"] * 1)
			avg += (data[app]["Overall Ratings"]["two_star"] * 2)
			avg += (data[app]["Overall Ratings"]["three_star"] * 3)
			avg += (data[app]["Overall Ratings"]["four_star"] * 4)
			avg += (data[app]["Overall Ratings"]["five_star"] * 5)
			avg /= sum(data[app]["Overall Ratings"].values())
			data[app]["Overall Average"] = avg

			data[app]["Previous Versions"] = {}
			data[app]["Previous Versions"]['one_star'] = data[app]["Overall Ratings"]["one_star"] - data[app]["Current Version"]["one_star"]
			data[app]["Previous Versions"]['two_star'] = data[app]["Overall Ratings"]["two_star"] - data[app]["Current Version"]["two_star"]
			data[app]["Previous Versions"]['three_star'] = data[app]["Overall Ratings"]["three_star"] - data[app]["Current Version"]["three_star"]
			data[app]["Previous Versions"]['four_star'] = data[app]["Overall Ratings"]["four_star"] - data[app]["Current Version"]["four_star"]
			data[app]["Previous Versions"]['five_star'] = data[app]["Overall Ratings"]["five_star"] - data[app]["Current Version"]["five_star"]
			avg = 0
			count = 0
			avg += (data[app]["Previous Versions"]["one_star"] * 1)
			avg += (data[app]["Previous Versions"]["two_star"] * 2)
			avg += (data[app]["Previous Versions"]["three_star"] * 3)
			avg += (data[app]["Previous Versions"]["four_star"] * 4)
			avg += (data[app]["Previous Versions"]["five_star"] * 5)
			total = sum(data[app]["Previous Versions"].values())
			if total > 0:
				avg /= total
			data[app]["Previous Average"] = avg
		else:
			delete.append(app)

	for app in delete:
		del data[app]
	return data

# Takes a dictionary of apps, returns two lists: a list of
# apps that had a star rating increase > good_thresh, and a
# list of apps that had a star rating change < bad_thresh
def findGoodBadUpdates(data, good_thresh, bad_thresh):
	good_updates = []
	bad_updates = []
	for app in data:
		if "Previous Versions" in data[app] and data[app]["Previous Average"] != 0:
			if data[app]["Current Average"] - data[app]["Previous Average"] > good_thresh:
				good_updates.append(app)
			elif data[app]["Current Average"] - data[app]["Previous Average"] < (bad_thresh * -1):
				bad_updates.append(app)
	return good_updates, bad_updates

# Calculates the ranking change from the day before, adds
# a new attribute dictionary called Ranking Chance, returns
# data dict
def calcDTDChange(data):
	delete = []
	for app in data:
		if "Ranking" in data[app]:
			data[app]["Ranking Change"] = {}
			for date in data[app]["Ranking"]:
				prev_day = date - timedelta(days=1)
				if prev_day in data[app]["Ranking"]:
					data[app]["Ranking Change"][date] = data[app]["Ranking"][date] - data[app]["Ranking"][prev_day]
		else:
			delete.append(app)
	for app in delete:
		del data[app]
	return data

# Dont worry about this one
def avgRankingChangeOverTime(data, days):
	delete = []
	total = 0
	count = 0
	for app in data:
		if "Ranking" in data[app]:
			for date in data[app]["Ranking"].keys():
				if date - timedelta(days=days) in data[app]["Ranking"]:
					total += data[app]["Ranking"][date] - data[app]["Ranking"][date-timedelta(days=days)]
					count += 1
		else:
			delete.append(app)
	mean = total / count

	for app in delete:
		del data[app]
	return data, mean

# Just reformats the dates in our data to datetime objects,
# returns the data dict
def strToDateTime(data):
	delete = []
	for app in data:
		if "Ranking" in data[app]:
			data[app]["Ranking"] = {datetime.strptime(x, "%Y-%m-%d"): y for x, y in data[app]["Ranking"].items() if type(x) == str}
		if "Last Updated" in data[app]:
			data[app]["Last Updated"] = datetime.strptime(data[app]["Last Updated"], "%b %d, %Y")

	return data

# This is the actual model. It returns a dictionary where the 
# keys are days relative to the update date, and the values are
# the average change on those days for every app in the dict.
# The days arguments specifies the number of days before and after
# the update date we are interested in
def beforeAndAfter(data, days):
	ret = {i: 0 for i in range(-1*days, days+1)}
	counts = {i: 0 for i in range(-1*days, days+1)}
	for app in data:
		if "Last Updated" in data[app]:
			last_updated = data[app]["Last Updated"]
			for i in range(-1*days, days+1):
				if last_updated + timedelta(days=i) in data[app]["Ranking Change"]:
					ret[i] += data[app]["Ranking Change"][last_updated + timedelta(days=i)]
					counts[i] += 1
	print(counts)
	print(ret)
	ret = {day: ct for day, ct in ret.items() if counts[day] > 3}
	ret = {day: ct/counts[day] for day, ct in ret.items()}
	print(ret)

	return ret

def main(infile):

	data = json.loads(open(infile).read())
	data = strToDateTime(data)
	# data, mean = avgRankingChangeOverTime(data, 10)

	data = calcPrevAvg(data)
	data = calcDTDChange(data)
	print(len(data))
	good_updates, bad_updates = findGoodBadUpdates(data, 0.3, 0.3)
	print(len(good_updates), len(bad_updates))
	good_data = {app: data[app] for app in good_updates}
	bad_data = {app: data[app] for app in bad_updates}
	day_split = beforeAndAfter(good_data, 10)
	keys = sorted(list(day_split.keys()))
	values = [day_split[key] for key in keys]
	plt.plot(keys, values)
	print(keys, values)
	plt.show()
	# print(day_split)

	
	# data = calcDTDChange(data)
	# data = calcPrevAvg(data)



	

	return 0

main("iphone-data-2015-08-01.json")