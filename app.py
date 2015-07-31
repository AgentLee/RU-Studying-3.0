#RU Studying

from flask import Flask, render_template, redirect, url_for, request, session, flash, g
#from timeproc import *
from showtimes import *
from parse import *
import json
import pytz 
from datetime import datetime as dt
import time

app = Flask(__name__)

tz = pytz.timezone('America/New_York')

@app.route('/')
def home():
	return render_template('index.html')

# reads file with all the buildings for each campus and returns a list
def getbldgs(campus):
	path = "buildings/" + campus + '.txt'
	bldgs = []
	bldg = ""

	with app.open_resource(path) as bldgList:
		while True:
			c = bldgList.read(1)
		
			if c == ' ':
				bldgs.append(bldg)
				bldg = ""
			else:
				bldg += c
		
			if not c:
				bldgs.append(bldg)
				bldg = ""
				break

	return bldgs

@app.route('/<campus>')
def showbldgs(campus):
	bldgs = getbldgs(campus)

	if campus == 'livingston':
		campus = 'LIVINGSTON'
	elif campus == 'busch':
		campus = 'BUSCH'
	elif campus == 'collegeavenue':
		campus = 'COLLEGE AVENUE'
	else:
		campus = 'DOUGLAS/COOK'

	return render_template('bldg.html', bldgs = bldgs, campus = campus)

def dayconverter(today):
	if today == 0:
		return 'Monday'
	elif today == 1:
		return 'Tuesday'
	elif today == 2:
		return 'Wednesday'
	elif today == 3:
		return 'Thursday'
	elif today == 4:
		return 'Friday'
	elif today == 5:
		return 'Saturday'
	else:
		return 'Sunday'

@app.route('/<campus>/<bldg>')
def showtimes(campus, bldg):
	today = dayconverter(datetime.datetime.now(tz).weekday())
	currenttime = datetime.datetime.now(tz).time()

	if currenttime.hour > 12:
		hour = currenttime.hour - 12
		hour = str(hour)

	if currenttime.minute < 10:
		minute = '0'
		minute += str(currenttime.minute)
	else:
		minute = str(currenttime.minute)
	#today = tz.time.strftime("%a")
	#currenttime = tz.time.strftime("%I:%M")
	
	insession, empty = checktime(campus, bldg)
	#processtime(campus, bldg, today, currenttime)	

	return render_template('showtimes.html', insession = insession, empty = empty, hour = hour, minute = minute, today = str(today), bldg = bldg, campus = campus)

if __name__ == '__main__':
	app.run(debug = True)
