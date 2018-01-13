# -*- coding:utf-8 -*- 
#	检查天梯赛季间隔
import time
import xl2lua2

def check(sheet, parses):
	print "Checking starttime(赛季间隔必须>=21天) for " + sheet.name
	row = 2
	time1 = ""
	time2 = ""
	while row < sheet.nrows:
		#print row
		for index, parse in enumerate(parses):
			key = parse["name"]
			if key == "starttime":
				value = xl2lua2.GetValue(sheet, row, 1)
				if time1 == "":
					time1 = value
				else:
					time2 = time1
					time1 = value

				timeisavailable(time1, time2)
				#print value
		
		row = xl2lua2.GetNextRow(sheet, row + 1, sheet.nrows, 1)			

def timeisavailable(time1, time2):
	if time2 == "":
		return

	timestamp1 = time.mktime(time.strptime(time1,'%Y-%m-%d %H:%M:%S'))
	timestamp2 = time.mktime(time.strptime(time2,'%Y-%m-%d %H:%M:%S'))
	deltatime = timestamp1 - timestamp2
	#print deltatime
	assert deltatime >= 21 * 24 * 3600, "赛季间隔必须>=21天"
	#print timestamp1
	#print timestamp2




