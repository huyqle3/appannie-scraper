#!/usr/local/bin/python3
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
import statistics

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
def findGoodBadUpdates(data, threshold):
	good_updates = []
	bad_updates = []
	for app in data:
		if "Previous Versions" in data[app] and data[app]["Previous Average"] != 0:
			if data[app]["Current Average"] - data[app]["Previous Average"] > threshold:
				good_updates.append(app)
			elif data[app]["Current Average"] - data[app]["Previous Average"] < (threshold * -1):
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

def ratingChangeStats(data):
	rating_change = []
	for app in data:
		if "Previous Average" in data[app] and data[app]["Previous Average"] != 0:
			rating_change.append(abs(data[app]["Current Average"] - data[app]["Previous Average"]))
	mean = sum(rating_change) / len(rating_change)
	std_dev = statistics.stdev(rating_change)
	return mean, std_dev

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
	fig = plt.figure()
	ret = {i: 0 for i in range(-1*days, days+1)}
	counts = {i: 0 for i in range(-1*days, days+1)}
	ranking_change = {}
	ranking_change_total = {i: 0 for i in range(0, days+1)}
	ranking_change_ct = {i: 0 for i in range(0, days+1)}
	for app in data:
		if "Last Updated" in data[app]:
			last_updated = data[app]["Last Updated"]
			prev_total = 0
			prev_count = 0
			for i in range(-1*days, 0):
				if last_updated + timedelta(days=i) in data[app]["Ranking"]:
					prev_total += data[app]["Ranking"][last_updated + timedelta(days=i)]
					prev_count += 1

			if prev_count > 0:
				prev_avg = prev_total / prev_count
			else:
				continue
			
			
			for j in range(1, days+1):
				ranking_change[0] = 0
				
				if last_updated + timedelta(days=j) in data[app]["Ranking"]:
					ranking_change[j] = data[app]["Ranking"][last_updated + timedelta(days=j)] - prev_avg
					ranking_change_total[j] += ranking_change[j]
					ranking_change_ct[j] += 1


			if len(ranking_change) > 5:
				keys = sorted(list(ranking_change.keys()))
				values = [ranking_change[key] for key in keys]
				plt.plot(keys, values)

	ranking_change_total = {x:y/ranking_change_ct[x] for x, y in ranking_change_total.items() if ranking_change_ct[x] > 0}
	ranking_change_total[0] = 0
	keys = sorted(list(ranking_change_total.keys()))
	values = [ranking_change_total[key] for key in keys]
	plt.plot(keys, values, linewidth=5)
	fig.suptitle('Good Updates', fontweight="bold")
	plt.xlabel('Days since most recent update')
	plt.ylabel('Rating change since most recent update')
	fig.savefig('good_updates.jpeg')
	plt.show()
	



	return ret

def main(infile):

	data = json.loads(open(infile).read())
	data = strToDateTime(data)
	# data, mean = avgRankingChangeOverTime(data, 10)
	# print(len(data))
	data = calcPrevAvg(data)
	data = calcDTDChange(data)
	rating_chg_mean, rating_chg_std_dev = ratingChangeStats(data)
	print(rating_chg_mean, rating_chg_std_dev)
	# print(rating_chg_mean, rating_chg_std_dev)
	# print(len(data))
	good_updates, bad_updates = findGoodBadUpdates(data, rating_chg_std_dev)
	print(len(good_updates), len(bad_updates))
	good_data = {app: data[app] for app in good_updates}
	bad_data = {app: data[app] for app in bad_updates}
	good = beforeAndAfter(good_data, 20)
	print




	

	return 0

main("data.json")