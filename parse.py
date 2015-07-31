######################################################
# converts json data to text files for easy parsing  #
# 332 still has problems 							 #
######################################################

import json
from collections import OrderedDict
import time
import datetime
import pytz
import os

#str(time.strfttime("%a"))

def addtofile(day, campus, bldg, room, start, end, pm):
	if campus is None or bldg is None or room is None or start is None or end is None:
		return

	if campus == 'COOK':
		campus = 'COOKDOUGLAS'

	if campus == 'DOUGLASS/COOK':
		campus = 'COOKDOUGLAS'

	if campus == 'DOUGLAS/COOK':
		campus = 'COOKDOUGLAS'

	path = "days/"+day+"/"+campus+"_"+bldg+"_"+room+".txt"

	times = start + " " + end + " " + pm
		
	# ex. days/M/LIVINGSTON_BRR.txt
	#if os.path.isfile(path): 
	#	with open(path) as dayfile:
	#		if times in dayfile:
	#			return
	#		else:
	#			dayfile.close()
	#else:
	dayfile = open(path, "a")
	dayfile.write(times+"|")

def parse():
	#no 332
	path = 'data/data_988.json'

	with open(path) as json_Data:
		data = json.load(json_Data)

	numClasses = len(data)

	i = 0
	while i in range(0, numClasses):
		numSections = len(data[i]['sections'])

		j = 0
		while j in range(0, numSections):
			numTimes = len(data[i]['sections'][j]['meetingTimes'])

			k = 0
			while k in range(0, numTimes):
				s = data[i]['sections'][j]['meetingTimes'][k]['startTime']
				e = data[i]['sections'][j]['meetingTimes'][k]['endTime']
				pm = data[i]['sections'][j]['meetingTimes'][k]['pmCode']
				building = data[i]['sections'][j]['meetingTimes'][k]['buildingCode']
				room = data[i]['sections'][j]['meetingTimes'][k]['roomNumber']
				campus = data[i]['sections'][j]['meetingTimes'][k]['campusName']
				day = data[i]['sections'][j]['meetingTimes'][k]['meetingDay']

				if s is not None and e is not None or building is not None or room is not None:
					#print path, campus, building, room, s, e, pm
					addtofile(day, campus, building, room, s, e, pm)
				k += 1

			j += 1

		i += 1

	json_Data.close()	




def main():
	#parse()
	#print checktime()	

if __name__ == "__main__":
    main()
