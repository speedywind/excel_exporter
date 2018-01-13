# -*- coding:utf-8 -*- 
#	检查关卡坐标
import xl2lua2

def check(sheet, parses):
	print "事件hpbar和question:" + sheet.name
	typecol,result = xl2lua2.getColByName(parses, "type")
	hpbarcol,result = xl2lua2.getColByName(parses, "hpbar")
	answercol,result = xl2lua2.getColByName(parses, "answer")
	# print typecol,hpbarcol,answercol, sheet.ncols
	row = 2
	if typecol >= sheet.ncols:
		return
	while row < sheet.nrows:
		mytype = xl2lua2.GetValue(sheet, row, typecol)
		if hpbarcol >= sheet.ncols:
			hpbar = False
		else:
			hpbar = xl2lua2.GetValue(sheet, row, hpbarcol)
		if answercol >= sheet.ncols:
			answer = False
		else:
			answer = xl2lua2.GetValue(sheet, row, answercol)
		# if mytype == "2.0":
		# 	print mytype, hpbar, answer
		if mytype == "0.0" and not hpbar:
			print "Error[战斗事件没有配置怪物]: near " + sheet.name + "("+xl2lua2.GetColNum(hpbarcol)+str(row+1)+")"
		elif mytype == "2.0" and not answer:
			print "Error[对话事件没有配置选项]: near " + sheet.name + "("+xl2lua2.GetColNum(answercol)+str(row+1)+")"
		row += 1
