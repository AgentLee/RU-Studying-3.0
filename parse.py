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

def parsepath(path):
	count = 0
	room = ""
	for c in path:
		if c == '_':
			count += 1
		if c == '.':
			return room
		if count == 2:
			if c == '_':
				continue
			room += c


#	garbage, good = path.split("days/TH/LIVINGSTON_BRR_", 1)
#	room, txt = good.split(".txt", 1)
#	return room

def checktime(campus, bldg):
	today = datetime.datetime.now()
	today = today.strftime("%A")

	if today == 'Monday':
		today = 'M'
	elif today == 'Tuesday':
		today = 'T'
	elif today == 'Wednesday':
		today = 'W'
	elif today == 'Thursday':
		today = 'TH'
	elif today == 'Friday':
		today = 'F'

	
	init_path = "days/"+today+"/"
	paths = []
	rooms = []
	room = ""
	for dir_entry in os.listdir(init_path):
		if bldg in dir_entry:
			paths.append(init_path+dir_entry)
	
	#campus = 'LIVINGSTON'
	#bldg = 'LSH'
	#room = 'B105'
	#path = 'days/'+today+'/'+campus+'_'+bldg+'_'+room+'.txt'
	rooms = []
	insession = []
	empty = []

	for path in paths:
		start1 = ""
		start2 = ""
		end1 = ""
		end2 = ""
		buff = ""
		pm = ""
		i = 0
		spaces = 0

		with open(path) as times:
			while True:
				c = times.read(1)
				
				i += 1
				
				if c == ' ':
					continue

				if c != '|':
					buff += c
				else:
					i = 0

				if i == 2:
					start1 = buff
					buff = ""
				elif i == 4:
					start2 = buff
					buff = ""
				elif i == 7:
					end1 = buff
					buff = ""
				elif i == 9:
					end2 = buff
					buff = ""
				elif i == 11:
					pm = buff
					buff = ""

					if pm == 'P':
						if start1 != "12":
							start1 = str(int(start1) + 12)
						if end1 != "12":
							end1 = str(int(end1) + 12)

					#print start1, start2, end1, end2, pm
						
					start = datetime.time(int(start1), int(start2), 0)
					end = datetime.time(int(end1), int(end2), 0)
					rn = datetime.datetime.now().time()

					room = parsepath(path)
					#print room, str(start), str(end), str(rn)
	
					if room not in rooms:
						rooms.append(room)

					if (start <= rn <= end) is True:
						if room not in insession:
							insession.append(room)
					elif (start <= rn <= end) is False:
						if room not in empty:
							empty.append(room)
					
				if not c:
					break

	insession.sort()
	empty.sort()	

	return insession, empty
	
	'''
	if start <= end:
		print 'empty'
		return start <= x <= end
	else:
		print 'class'
		return start <= x or x <= end
	'''

def main():
	insession, empty = checktime('LIVINGSTON', 'LSH')
	for full in insession:
		print full, " in session"

	for clear in empty:
		print clear, " empty"

	#for room in checktime('LIVINGSTON', 'LSH'):
	#	print room
		
	#parse()
	#print checktime()	

if __name__ == "__main__":
    main()
