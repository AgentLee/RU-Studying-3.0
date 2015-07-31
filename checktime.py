#######################################
# gets rooms that match user criteria #
#######################################

import json
from collections import OrderedDict
import time
import datetime
import pytz
import os

tz = pytz.timezone('America/New_York')

# splits path to get room number
def getroom(path):
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

# get day of the week
def getday():
	today = datetime.datetime.now()
	today = today.strftime("%A")

	if today == 'Monday':
		return 'M'
	elif today == 'Tuesday':
		return 'T'
	elif today == 'Wednesday':
		return 'W'
	elif today == 'Thursday':
		return 'TH'
	elif today == 'Friday':
		return 'F'

def gettimes(paths, rooms):
	for i in range(len(rooms)):
		start1 = ""
		start2 = ""
		end1 = ""
		end2 = ""
		buff = ""
		pm = ""
		count = 0
		spaces = 0

		path = paths[i]
		with open(path) as times:
			while True:
				c = times.read(1)

				count += 1

				if c == ' ':
					continue

				if c != '|':
					buff += c
				else:
					count = 0

				if count == 2:
					start1 = buff
					buff = ""
				elif count == 4:
					start2 = buff
					buff = ""
				elif count == 7:
					end1 = buff
					buff = ""
				elif count == 9:
					end2 = buff
					buff = ""
				elif count == 11:
					pm = buff
					buff = ""

					if pm == 'P':
						if start1 != "12":
							start1 = str(int(start1) + 12)
						if end1 != "12":
							end1 = str(int(end1) + 12)
					elif pm == 'A':
						if int(start1) < 12 and int(end1) < 10:
							end1 = str(int(end1) + 12)

					start = datetime.time(int(start1), int(start2), 0)
					end = datetime.time(int(end1), int(end2), 0)
					rn = datetime.datetime.now(tz).time()

					if (start <= rn <= end) is True:
						if rooms[i][1] is True:
							rooms[i][1] = False
					elif (start <= rn <= end) is False:
						if rooms[i][1] is False:
							continue

					#print rooms[i], start1, start2, end1, end2, pm

				if not c:
					break

	return rooms

def getrooms(campus, bldg):
	today = getday()

	init_path = "days/"+today+"/"
	paths = []
	rooms = []
	room = ""

	# gets all the paths in days/today/
	# that match user criteria
	# sample path = 'days/'+today+'/'+campus+'_'+bldg+'_'+room+'.txt'
	for dir_entry in os.listdir(init_path):
		if bldg in dir_entry and campus in dir_entry:
			paths.append(init_path+dir_entry)

	paths.sort()

	rooms = []
	roomz = []
	insession = []
	empty = []

	for i in range(len(paths)):
		path = paths[i]
		room = getroom(path)

		if room not in rooms:
			rooms.append([])
			for j in range(2):
				if j == 0:
					rooms[i].append(room)
				else:
					rooms[i].append(True)


	rooms = gettimes(paths, rooms)

	return rooms

def main():
	rooms = getrooms('LIVINGSTON', 'BRR')
	for room in rooms:
		print room

if __name__ == "__main__":
    main()