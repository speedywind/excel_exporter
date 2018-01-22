# -*- coding:utf-8 -*- 

#	excel 导出 lua 表
#	支持类型: int,bool,float,string,struct<int>,struct<bool>,list<struct>
#	特别说明default(仅用于struct): list<struct<int:itemid,default:count=1>>:reward
#	特别说明: IsMyInt0 IsMyInt IsMyString中的字段可以不配类型
#	特别说明<(<数相同表示同级元素): list<struct<int:hpbar>>:enemy	<list<struct<int:enemyid>>:enemy	string:enemyname	int:count=1	int:lv=0
	# 导出结构示例: ld_enemy:id=key  name  struct<int:itemid>:cost  struct<int:hpbar=1>:enemygroup  <list<struct<int:itemid>>:lootlist  count  <list<struct<int:id>>:enemy  <<list<struct<int:enemylv=0>>:enemylv
	# ld_ENEMY    (源自ld_enemy:id=key  name)
	# ├──[1]={id = 1, name = "enemy1",
	# │   ├──cost={itemid = 1001, count = 1},     (源自struct<int:itemid,default:count=1>:cost)
	# │   └──enemygroup={hpbar = 2,    (源自struct<int:hpbar=1>:enemygroup)
	# │          ├──lootlist={         (源自<list<struct<int:itemid>>:lootlist  count)
	# │          │      ├──{itemid = 1001, count = 10},
	# │          │      └──{itemid = 1002, count = 100}},
	# │          │
	# │          └──enemy={            (源自<list<struct<int:id>>:enemy  <<list<struct<int:enemylv=0>>:enemylv)
	# │               ├──{id = 40012,
	# │               │  └──enemylv={{enemylv = -1}}},
	# │               ├──{id = 40013,
	# │               │  └──enemylv={{enemylv = 0}}},
	# │               └──{id = 40014,
	# │                  └──enemylv={{enemylv = 1}}}}}},
	# └──[2]={id = 2, name = "enemy2",
	#     ├──cost={itemid = 1001, count = 1},
	#     └──enemygroup={hpbar = 2,
	#            ├──lootlist={
	#            │      ├──{itemid = 1001, count = 10},
	#            │      └──{itemid = 1002, count = 100}},
	#            │
	#            └──enemy={
	#                 ├──{id = 40012,
	#                 │  └──enemylv={{enemylv = -1}}},
	#                 ├──{id = 40013,
	#                 │  └──enemylv={{enemylv = 0}}},
	#                 └──{id = 40014,
	#                    └──enemylv={{enemylv = 1}}}}}},

import codecs
import copy
import time
import xlrd
import sys
import os
import shutil
# import ckladderseason
# import ckevent1
# import ckevent
sheetfields = {}
imglacks = {}
isdebug = False
TFileTag = "ld_"
TDefault = "default"
TInt = "int"
TBool = "bool"
TFloat = "float"
TString = "string"
TStruct = "struct"
TList = "list"
TNextLevel = "<"
TReward = "Reward"
myrow = 1
mycol = 0
filename = "ld_"
sheetname = "ld_"

def IsMyInt0(name):
	return name == "team_ad" \
	or name == "team_ap" \
	or name == "sp" \
	or name == "ad" \
	or name == "ap" \
	or name == "adi" \
	or name == "api" \
	or name == "arm" \
	or name == "mr" \
	or name == "str" \
	or name == "spi" \
	or name == "def" \
	or name == "vit" \
	or name == "power" \
	or name == "rating" \
	or name == "ratingdamage" \
	or name == "fireup" \
	or name == "iceup" \
	or name == "lightup" \
	or name == "darkup" \
	or name == "speed" \
	or name == "heal" \
	or name == "skill" \
	or name == "skilllevel" \
	or name == "steal" \
	or name == "duochong" \
	or name == "health" \
	or name == "enemylv" \
	or name == "limit" \
	or name == "reelement"

def IsMyInt(name):
	return name[-2:] == "id" \
	or name[-4:] == "type" \
	or name[-5:] == "level" \
	or name == "rare" \
	or name == "handbook" \
	or name == "counta" \
	or name == "countb" \
	or name == "count" \
	or name == "weight" \
	or name == "weightb" \
	or name == "weightall" \
	or name == "star" \
	or name == "interval" \
	or name == "exp" \
	or name == "gold" \
	or name == "daguan" \
	or name == "lv" \
	or name == "targetcount" \
	or name == "targetcount1" \
	or name == "rank" \
	or name == "rank1" \
	or name == "order" \
	or name == "zhanli" \
	or name == "merlevel" \
	or name == "score" \
	or name == "grade" \
	or name == "position" \
	or name == "skip" \
	or name == "rate"

def IsMyString(name):
	return name == "name" \
	or name[-3:] == "des" \
	or name == "starttime" \
	or name == "endtime" \
	or name == "ccbi" \
	or name == "img"

def IsMyStruct(name):
	return name[:len("Reward")] == "Reward" \
	or name[:len("Enemy")] == "Enemy" \
	or name[:len("struct")] == "struct"

def CheckMyStruct(fieldtype, fields):
	if fieldtype[:len("Reward")] == "Reward":
		nextfields = fieldtype[len("Reward")+1:-1].split(",")
		for index, parse in enumerate(nextfields + fields):
			if TList == parse[:len(TList)] or TStruct == parse[:len(TStruct)] or IsMyStruct(parse) or TNextLevel == parse[:len(TNextLevel)]:
				break;
			assert parse.find("itemid") in [0, len("int:"), len("default:")]\
				or parse.find("count") in [0, len("int:"), len("float:"), len("default:")]\
				or parse.find("weight") in [0, len("int:"), len("float:"), len("default:")]\
				or parse.find("startloot") in [0, len("int:"), len("float:"), len("default:")]\
				or parse.find("lootshow") in [0, len("int:"), len("default:")] or not parse,\
				"Error[非法的数据结构]: near " + fieldtype +"\n"+ str(nextfields+fields)
	elif fieldtype[:len("EnemyGroup")] == "EnemyGroup":
		nextfields = fieldtype[len("EnemyGroup")+1:-1].split(",")
		for index, parse in enumerate(nextfields + fields):
			assert parse == "<list<Enemy<int:enemyid>>:enemy"\
				or  parse.find("hpbar") in [0, len("int:"), len("default:")] or not parse,\
				"Error[非法的数据结构]: near " + fieldtype +"\n"+ str(nextfields+fields)
			if TList == parse[:len(TList)] or TStruct == parse[:len(TStruct)] or IsMyStruct(parse) or TNextLevel == parse[:len(TNextLevel)]:
				break;
	elif fieldtype[:len("Enemy")] == "Enemy":
		nextfields = fieldtype[len("Enemy")+1:-1].split(",")
		for index, parse in enumerate(nextfields + fields):
			if TList == parse[:len(TList)] or TStruct == parse[:len(TStruct)] or IsMyStruct(parse) or TNextLevel == parse[:len(TNextLevel)]:
				break;
			assert parse.find("enemyid") in [0, len("int:"), len("default:")]\
				or parse.find("count") in [0, len("int:"), len("default:")]\
				or parse.find("enemylv") in [0, len("int:"), len("default:")] or not parse,\
				"Error[非法的数据结构]: near " + fieldtype +"\n"+ str(nextfields+fields)
	else:
		assert not fieldtype, "Error[未识别的数据结构]: near " + fieldtype
	return nextfields

def CheckParses(fields):
	result = []
	while len(fields) > 0:
		# print fields
		field = fields.pop(0)
		if not field:
			parse = { 'name': "", "func": None, "args": None }
			result.append(parse)
			continue
		if TNextLevel == field[:len(TNextLevel)]: #父子
			field = field[len(TNextLevel):]
			for index, val in enumerate(fields):
				if TNextLevel == val[:len(TNextLevel)]:
					fields[index] = val[len(TNextLevel):]
		if TFileTag == field[:len(TFileTag)]:
			field = field[field.find(":")+1:]
		parse = { "default": None, "args": None }
		typepos = field.rfind(":")
		fieldtype = field[:typepos]
		name = field[typepos+1:]
		valuepos = name.rfind("=")
		if valuepos != -1: #设置默认值
			parse["default"] = name[valuepos+1:]
			name = name[:valuepos]
		parse["name"] = ValToKey(name)
		# print fieldtype, name, parse
		if TDefault == fieldtype[:len(TDefault)]: #默认字段,只出现在list和struct中
			parse["func"] = TDefault
		elif TInt == fieldtype[:len(TInt)]:
			parse["func"] = TInt
		elif TBool == fieldtype[:len(TBool)]:
			parse["func"] = TBool
		elif TFloat == fieldtype[:len(TFloat)]:
			parse["func"] = TFloat
		elif TString == fieldtype[:len(TString)]:
			parse["func"] = TString
			if parse["default"] and parse["default"][:1] != "\"" and parse["default"][-1:] != "\"":
				parse["default"] = CheckString(parse["default"])
		elif typepos == -1 and IsMyInt0(name):
			fieldtype = TInt
			parse["func"] = TInt
			if not parse["default"]:
				parse["default"] = "0"
		elif typepos == -1 and IsMyInt(name):
			fieldtype = TInt
			parse["func"] = TInt
		elif typepos == -1 and IsMyString(name):
			fieldtype = TString
			parse["func"] = TString
		else:
			if TList == fieldtype[:len(TList)]:
				parse["func"] = TList
				nextfield = fieldtype[len(TList)+1:-1]
				nextfields = IsMyStruct(nextfield) and [nextfield+":"] or ["struct<" + nextfield+">:"]
				# print nextfields
			elif TStruct == fieldtype[:len(TStruct)]:
				parse["func"] = TStruct
				nextfields = fieldtype[len(TStruct)+1:-1].split(",")
			# elif TReward == fieldtype[:len(TReward)]:
			# 	parse["func"] = TStruct
			# 	nextfields = fieldtype[len(TReward)+1:-1].split(",")
			elif IsMyStruct(fieldtype):
				parse["func"] = TStruct
				nextfields = CheckMyStruct(fieldtype, fields)
			else:
				print fieldtype, name, parse
				assert not field, "Error[非法的字段名]: near " + field +"\n"+ str(result)
			endpos = len(fields)
			for m in xrange(0, endpos):
				if len(fields[m]) != 0 and  TInt != fields[m][:len(TInt)] and TBool != fields[m][:len(TBool)] \
				and TFloat != fields[m][:len(TFloat)] and TString != fields[m][:len(TString)] and TNextLevel != fields[m][:len(TNextLevel)] \
				and not IsMyInt0(fields[m].split('=')[0]) and not IsMyInt(fields[m].split('=')[0]) and not IsMyString(fields[m].split('=')[0]):
					endpos = m
					# print endpos, fields[endpos]
					break
			# print endpos, nextfields + fields[0:endpos]
			assert TList != fieldtype[:len(TList)] or endpos == 0 or not fields[endpos-1] or IsMyStruct(nextfields[0]), "Error[list后请不要配一级字段]: near " + field +"\n"+ str(result)
			parse["args"] = CheckParses(nextfields + fields[:endpos])
			parse1 = parse["args"].pop()
			if parse1["func"] == TStruct:
				parse["args"].append(parse1)
				parse2 = parse1["args"].pop()
				if parse2["func"] == TList and parse["name"] == parse2["name"]: #父子合并
					# if parse["args"] != parse2["args"]:
					# 	debug("Warning "+)
					parse["args"] += parse2["args"]
				else:
					parse1["args"].append(parse2)
			elif parse1["func"] == TList and parse["name"] == parse1["name"]:
			 # and parse["args"] == parse1["args"]: #父子合并
				parse["args"] += parse1["args"]
			else:
				parse["args"].append(parse1)
			# print parse
			fields = fields[endpos:]
		# if len(result) > 0:
		# 	print parse," += ",result[len(result)-1]
		if len(result) > 0 and parse["func"] == TList and parse["name"] == result[len(result)-1]["name"]:
		# and (parse["args"] == result[len(result)-1]["args"] or (type(result[len(result)-1]["args"]) is list \
		# and parse["args"] == result[len(result)-1]["args"][:1])): #同级合并
			parse["args"] += result[len(result)-1]["args"]
			result.pop()
		for index, parse1 in enumerate(result):
			assert parse["name"] != parse1["name"], "Error[重复的字段]: near " + field +"\n"+ str(result)
		result.append(parse)
	# print result
	return result

def ValToKey(val):
	return val.isdecimal() and "[" + val + "]" or val

def CheckInt(data, args = None):
	if len(data) == 0:
		assert args != "key", "Error[主键不能为空]: near " + sheetname + filename + "("+GetColNum(mycol)+str(myrow+1)+")"
		assert args != None, "Error[字段不能为空]: near " + sheetname + filename + "("+GetColNum(mycol)+str(myrow+1)+")"
		return args
	vals = data.split('.')
	assert len(vals) == 2 and vals[1] == "0", "Error[非法的整型]: found " + data + " near " + sheetname + filename + "("+GetColNum(mycol)+str(myrow+1)+")"
	return vals[0]

def CheckBool(data, args = None):
	if len(data) == 0:
		assert args, "Error[字段不能为空]: near " + sheetname + filename + "("+GetColNum(mycol)+str(myrow+1)+")"
		return args
	return "0.0" == data and "false" or "true"

def CheckFloat(data, args = None):
	if len(data) == 0:
		assert args, "Error[字段不能为空]: near " + sheetname + filename + "("+GetColNum(mycol)+str(myrow+1)+")"
		return args
	return data

def CheckString(data, args = None):
	if not data:
		if not args:
			return "\"\""
		else:
			return args
	elif data[-2:] == ".0":
		data = data[:-2]
	return "\"" + data.replace("\n", "\\n") + "\""

def GetValue(sheet, row, col):
	return unicode(sheet.cell(row,col).value).strip()
	# return unicode(sheet.cell(row,col).value or "")

def GetLine(sheet, row):
	return [GetValue(sheet, row, col) for col in xrange(0, sheet.ncols)]

def GetType(name):
	if name[0] == 'i':
		return "int"
	elif name[0] == 'b':
		return "bool"
	elif name[0] == 'f':
		return "float"
	elif name[0] == 's':
		return "string"

def getColByName(parses, name):
	col1 = 0
	result = False
	for index, parse in enumerate(parses):
		if parse["name"] == name:
			return col1, True
		elif parse["func"] == TDefault:
			continue
		elif parse["func"] == TStruct:
			col, result = getColByName(parse["args"], name)
			col1 += col
		elif parse["func"] == TList:
			col, result = getColByName(parse["args"], name)
			col1 += col
		else: #跳过空字段或基础字段
			col1 += 1
		if result:
			return col1, True
	return col1, result

def GetColNum(col):
	if col >= 26:
		return "A" + unichr(col + 65 - 26)
	return unichr(col + 65)

def GetCols(parse):
	return str(parse).count('func')-str(parse).count('func\': \''+TDefault)-str(parse).count('func\': \''+TList)-str(parse).count('func\': \''+TStruct)

def CheckChunk(parses, sheet, row1, row2, col, indent, nodename):
	global myrow
	global mycol
	global imglacks
	luachunks = []
	jschunks = []
	xmlchunks = []
	while row1 < row2:
		myrow = row1
		col1 = col
		luachunk = []
		jschunk = []
		xmlchunk = []
		majorkey = None
		newrow2 = GetNextRow(sheet, row1 + 1, row2, col)
		# print "parse row", row1, newrow2
		for index, parse in enumerate(parses):
			mycol = col1
			field = parse["func"] == TDefault and parse["default"] or GetValue(sheet, row1, col1)
			key = parse["name"]
			# print myrow, mycol, parse["func"], key, field
			if parse["func"] == TDefault:
				assert parse["default"], "Error[无效的默认值]: near " + sheetname + filename + "("+GetColNum(mycol)+str(myrow+1)+")"
				if key.find("weight") == -1:
					luachunk.append(key + " = " + parse["default"])
					jschunk.append(key + ":" + parse["default"])
				xmlchunk.append(key + " = " + Quotes(parse["default"]))
				continue
			elif parse["func"] == TInt:
				val = CheckInt(field, parse["default"])
				if key.find("weight") == -1 and (field or not key in ["fordiamond", "skill", "skill1", "skill2"]):
					luachunk.append(key and key + " = " + val or val)
					jschunk.append(key and key + ":" + val or val)
				# else:
				# 	print "ignoring "+key+" = "+val
				if  filename != "ld_armor" or not key in ["equiplevel", "zhanli", "skill", "skilllevel"]:
					xmlchunk.append(key and key + " = " + Quotes(val) or Quotes(val))
				if parse["default"] == "key":
					assert not majorkey, "Error[重复的主键]: near " + sheetname + filename + "("+GetColNum(mycol)+str(myrow+1)+")"
					majorkey = "" + str(val) + ""
				col1 += 1
			elif parse["func"] == TBool:
				luachunk.append(key and key + " = " + CheckBool(field, parse["default"]) or CheckBool(field, parse["default"]))
				jschunk.append(key and key + ":" + CheckBool(field, parse["default"]) or CheckBool(field, parse["default"]))
				xmlchunk.append(key and key + " = " + Quotes(CheckBool(field, parse["default"])) or Quotes(CheckBool(field, parse["default"])))
				col1 += 1
			elif parse["func"] == TFloat:
				luachunk.append(key and key + " = " + CheckFloat(field, parse["default"]) or CheckFloat(field, parse["default"]))
				jschunk.append(key and key + ":" + CheckFloat(field, parse["default"]) or CheckFloat(field, parse["default"]))
				xmlchunk.append(key and key + " = " + Quotes(CheckFloat(field, parse["default"])) or Quotes(CheckFloat(field, parse["default"])))
				col1 += 1
			elif parse["func"] == TString:
				val = CheckString(field, parse["default"])
				if val != "\"\"" and key in ["img", "icon"]:
					rval = val[1:-1]
					# if filename == "ld_state":
					# 	path = "../美术/【乱斗】图片分类/state/"+rval+".png"
					# 	if not os.path.exists(path):
					# 		imglacks[rval] = "Warn["+filename+"找不到文件]: "+path
					# 		print imglacks[rval]
					# 	else:
					# 		shutil.copy(path, "../res/state/"+rval+".png")
					# elif filename in ["ld_touxiang", "ld_touxiangkuang", "ld_taskrichang", "ld_taskkaifu1", "ld_taskkaifu2"]:
					# 	path = "../美术/【乱斗】图片分类/res/"+rval+".png"
					# 	if not os.path.exists(path):
					# 		imglacks[rval] = "Warn["+filename+"找不到文件]: "+path
					# 		print imglacks[rval]
					# 	else:
					# 		shutil.copy(path, "../res/"+rval+".png")
					# elif not filename in ["ld_pvpfield", "ld_enemy", "ld_hero", "ld_talent"]:
					# 	for subpath in ["res/", "skill/", "state/", "材料/", "防具/", "技能/", "武器/"]:
					# 		path = "../美术/【乱斗】图片分类/"+subpath+rval+".png"
					# 		if os.path.exists(path):
					# 			shutil.copy(path, "../res/skill/"+rval+".png")
					# 			break
					# 	if not os.path.exists(path):
					# 		imglacks[rval] = "Warn["+filename+"找不到文件]: "+"../美术/【乱斗】图片分类/*/"+rval+".png"
					# 		print imglacks[rval]
				if val != "\"\"" or not key in ["img", "ccbi", "starttime", "endtime"]:
					luachunk.append(key and key + " = " + val or val)
					jschunk.append(key and key + ":" + val or val)
				if  not filename in ["ld_armor", "ld_event", "ld_package"] or not key in ["img", "des", "answer"]:
					xmlchunk.append(key and key + " = " + Quotes(CheckString(field, parse["default"])) or Quotes(CheckString(field, parse["default"])))
				col1 += 1
			elif parse["func"] == TStruct:
				if not GetValue(sheet, row1, col1) and parse["args"][0]["default"] == None:
					col1 += GetCols(parse["args"])
				else:
					col1, lua, js, xml = CheckChunk(parse["args"], sheet, row1, newrow2, col1, indent, key and key or nodename)
					if lua.find("lootshow = ") >= 0:
						if lua.find("lootshow = 1") >= 0:
							lua = lua.replace(", lootshow = 1", "")
							js = js.replace(", lootshow:1", "")
						else:
							debug("Removing lootshow: "+lua)
							lua = ""
							js = ""
					if lua[len(indent)+1:len(indent)+2] == "[":
						luachunk.append(lua)
						jschunk.append(js)
					elif lua:
						luachunk.append(key and key + " = {" + lua + "}" or "{" + lua + "}")
						jschunk.append(key and key + ":{" + js + "}" or "{" + js + "}")
					if xml != "" and (filename == "ld_hero" or filename == "ld_talent" or not (key and key or nodename) in ["increase", "states", "skill"]):
						xmlchunk.append((len(xmlchunk) > 0 and xmlchunk[len(xmlchunk)-1][-1:] != ">") and ">" + xml or xml)
			elif parse["func"] == TList:
				col1, lua, js, xml = CheckChunk(parse["args"], sheet, row1, newrow2, col1, indent+"\t", key)
				if xml != "":
					xmlchunk.append((len(xmlchunk) > 0 and xmlchunk[len(xmlchunk)-1][-1:] != ">") and ">" + xml or xml)
				if parse["default"] == "key":
					key =  ValToKey(CheckInt(field))
				luachunk.append("\n"+indent+"\t" + key + " = {" + lua + "}")
				jschunk.append("\n"+indent+"\t" + key + ":{" + js + "}")
			else: #跳过空字段
				assert parse["func"] == None, "Error[非法的字段名]: near " + sheetname + filename + "("+GetColNum(mycol)+str(myrow+1)+")"
				col1 += 1
			# print luachunk[len(luachunk)-1]
		xml = " ".join(xmlchunk)
		assert xml[-1:] == '"' or xml[-1:] == '>' or xml[-1:] == '', "A"+xml+"A"
		if xml != "":
			xmlchunks.append((xml[:1] == ">" or xml[:1] == "\n") and xml or "\n" + indent + "<" + nodename + " " + xml + (xml[-1:] == '"' and ">" or "") + "</" + nodename + ">")
		if majorkey:
			luachunks.append("\n" + indent + "[" + majorkey + "]" + " = {" + ", ".join(luachunk) + "}")
			jschunks.append("\n" + indent + majorkey + ":{" + ", ".join(jschunk) + "}")
		elif len(luachunk) > 0: #列表比如{1,2,3}
			luachunks.append(", ".join(luachunk))
			jschunks.append(", ".join(jschunk))
		row1 = newrow2
	return col1, ", ".join(luachunks),", ".join(jschunks), " ".join(xmlchunks)

def Quotes(val):
	if val[:1] == '"':
		return val
	return '"' + val + '"'

def GetNextRow(sheet, row1, row2, col):
	for newrow1 in xrange(row1, row2):
		if len(GetValue(sheet, newrow1, col)) != 0:
			return newrow1
	return row2

def debug(vals):
	if isdebug:
		print vals

def ExportFile(xlsx):
	global filename
	global sheetname
	oldfilename = "ld_"
	for index, sheet in enumerate(xlsx.sheets()):
		if sheet.nrows < 3:
			continue
		#	第一行注释
		#	第二行类型
		debug(GetLine(sheet, 1))
		sheetname = sheet.name
		filename = GetValue(sheet, 1, 0)
		if TFileTag == filename[:len(TFileTag)]:
			pos = filename.find(":")
			filename = filename[:pos]
		else:
			continue
		print "Exporting " + sheetname + filename + "......"
		sheetfields[filename] = ""
		for field in GetLine(sheet, 1):
			sheetfields[filename] += field+"\\\n"
		parses = CheckParses(GetLine(sheet, 1))
		# {'args': parses, 'name': u'a', 'func': u'int'}
		debug(parses)
		#	第三行内容
		if filename == oldfilename:
			print "Same file:", filename
			newlua = lua
			newjs = js
			newxml = xml
			col, lua, js, xml = CheckChunk(parses, sheet, 2, sheet.nrows, 0, "", "data")
			lua = newlua + "," + lua
			js = newjs + "," + js
			xml = newxml + "," + xml
		else:
			col, lua, js, xml = CheckChunk(parses, sheet, 2, sheet.nrows, 0, "", "data")
		#在此进行文件内容的校验
		# if filename == "ld_ladderseason":
		# 	ckladderseason.check(sheet, parses);
		# elif filename == "ld_event1":
		# 	ckevent1.check(sheet, parses);
		# elif filename == "ld_event":
		# 	ckevent.check(sheet, parses);
		#save to file
		oldfilename = filename
		if not filename in ["ld_fenjie"]:
			with codecs.open("../luanew/" + filename + ".lua", "w", "utf-8") as f:
				f.write(filename.upper() + " = {" + lua + "}")
		if not filename in ["ld_fenjie"]:
			with codecs.open("../jsnew/" + filename + ".js", "w", "utf-8") as f:
				f.write("module.exports = {" + js + "}")
		if not filename in ["ld_lvattribute"]:
			with codecs.open("../xmlnew/" + filename + ".xml", "w", "utf-8") as f:
				f.write("<data>" + xml + "</data>")

def HasKey(obj, attr):
	try:
	    if obj[attr] != None:
	    	return True
	except Exception,e:
		return False

def Main(opath):
	print "Reading " + opath
	xlsx = xlrd.open_workbook(opath)
	ExportFile(xlsx)

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	# print sys.getdefaultencoding()
	os.chdir(sys.path[0])
	with codecs.open("sheet.log", "r", "utf-8") as f:
		# print f.read().replace("\\", "\\\\\\n\\")
		sheetfields = eval(f.read().replace("\\", "\\\\\\n\\"))
	sheetfieldsold = copy.deepcopy(sheetfields)
	for i in xrange(1, len(sys.argv)):
		if sys.argv[i] == "debug":
			isdebug = True
	for i in xrange(1, len(sys.argv)):
		if sys.argv[i] != "debug":
			Main(sys.argv[i])
	with codecs.open("change.log", "a", "utf-8") as f:
		change = time.strftime('%Y-%m-%d',time.localtime(time.time()))+"\r\n"
		for key in sorted(sheetfields.keys()):
			if not HasKey(sheetfieldsold, key):
				val = "新增配置"+", ".join(sheetfields[key].split("\\\n"))+"\r\n"
				change += val
				print val
			elif sheetfields[key] != sheetfieldsold[key]:
				val = key+"发生变化:"
				newfields = sheetfields[key].split("\\\n")
				oldfields = sheetfieldsold[key].split("\\\n")
				index = len(newfields) - 1
				while index >= 0:
					if newfields[index] in oldfields:
						oldfields.remove(newfields[index])
						newfields.remove(newfields[index])
					index -= 1
				if len(oldfields) > 0:
					val += "  删除"+", ".join(oldfields)
				if len(newfields) > 0:
					val += "  增加"+", ".join(newfields)
				change += val + "\r\n"
				print val
		if isdebug and change.count("\n") > 1:
			f.write(change)
	if isdebug:
		# with codecs.open("imglacks.log", "w", "utf-8") as f:
		# 	result = ""
		# 	for key in sorted(imglacks.keys()):
		# 		if(not key.isdigit()):
		# 			result += imglacks[key]+"\n"
		# 			del imglacks[key]
		# 	if result == "":
		# 		f.write("No image is lack.\n")
		# 	else:
		# 		f.write(result)
		# 	f.write("other:\n")
		# 	f.write('\n'.join(['%s' % (imglacks[key]) for key in sorted(imglacks.keys())]))
		with codecs.open("sheet.log", "w", "utf-8") as f:
			f.write("{" + ',\n'.join(['"%s":\n"%s"' % (key, sheetfields[key]) for key in sorted(sheetfields.keys())]) + "}")
