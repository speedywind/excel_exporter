# -*- coding:utf-8 -*- 
#	检查关卡坐标
import xl2lua2

def check(sheet, parses):
	print "检查关卡坐标(cox,coy):" + sheet.name
	col, result = xl2lua2.getColByName(parses, "cox")
	row = 2
	cox = 0
	coy = 0
	coxys = []
	while row < sheet.nrows:
		if xl2lua2.GetValue(sheet, row, 0):
			# print coxys
			coxys = []
			cox = 0
		x = int(float(xl2lua2.GetValue(sheet, row, col)))
		y = int(float(xl2lua2.GetValue(sheet, row, col+1)))
		val = 10*x+y
		if cox != 0 and (abs(cox-x) > 1 or abs(coy-y) > 1):
			print "Error[关卡坐标偏移过大]: near " + sheet.name + "("+xl2lua2.GetColNum(col)+str(row+1)+"):"+str(cox)+","+str(coy)+"-->"+str(x)+","+str(y)
		elif cox != 0 and val in coxys:
			print "Error[重复的关卡坐标]: near " + sheet.name + "("+xl2lua2.GetColNum(col)+str(row+1)+")"
		cox = x
		coy = y
		coxys.append(val)
		row += 1
