#!/usr/bin/env python3
from flask import Flask

import os
import csv
from flask import render_template
from flask import request
import sqlite3
from timeit import timeit
import redis
import json
app = Flask(__name__)

# print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))
print(port)
# r=redis.Redis(host='localhost',port=6379,decode_responses=True)
db=sqlite3.connect('1.db')
cu=db.cursor()
data=cu.execute('select * from all_month')
data2=[]
i=0
for row in data:
	data2.append(row)
	# r.set(i,str(row))
db.commit()
db.close()



@app.route('/pie')
def pie():
	# db=sqlite3.connect('1.db')
	# cu=db.cursor()
	# data=cu.execute('select * from all_month')
	list=[]
	list2=[]
	count=[[1,5,0],[5,10,0],[10,20,0],[20,100,0],[100,1000,0]]
	for row in data2:
		# print(row[4])
		list2.append([row[1],row[2]])
		if row[3]==None or row[4]==None:
			pass
		else:
			for i in range(len(count)):
				if float(row[3])>=count[i][0] and float(row[3])<count[i][1]:
					# print(float(row[4]))
					count[i][2]+=1
					# list.append(row)
			if float(row[4])>=4:
				list.append({"zoomLevel":5,
  "scale": 0.5,
  "title": "EarchQuake",
  "latitude": row[1],
  "longitude": row[2]})
	count1=[]
	count2=[]
	for i in count:
		count1.append(i[2])
	# print(count1)
	for i in range(len(count)):
		count2.append({'name':str(count[i][0])+'-'+str(count[i][1]),'value':count[i][2]})
	# print(list)




	return render_template('chart.html',locationdata=json.dumps(list),count=json.dumps(count1),count2=json.dumps(count2),scatter=json.dumps(list2))





@app.route('/histogram')
def createtable():
	tablename=request.args.get('tabelname')
	if tablename:
		time2=timeit("cu.execute('CREATE Table %s(Id NOT NULL)');"%tablename,"import sqlite3;db=sqlite3.connect('1.db');cu=db.cursor();",number=1)
		return render_template('tabletime.html',time1=time2)
	else:
		return render_template('tabletime.html')

@app.route('/scatter')
def searchtable():
	number=request.args.get('number')
	depth=request.args.get('depth')
	redis_num=request.args.get('redis_num')
	if number and depth and redis_num:
		number=int(number)
		depth=float(depth)
		time2=timeit("cu.execute('SELECT * FROM all_month WHERE depth>=%d');"%depth,"import sqlite3;db=sqlite3.connect('1.db');cu=db.cursor();",number=number)
		number2=int(redis_num)
		time3=timeit("r.get(1)","import redis;r=redis.Redis(host='localhost',port=6379,decode_responses=True);",number=number2)
		return render_template('tabletime.html',time2=time2,number=number,time3=time3,number2=number2)
	else:
		return render_template('tabletime.html')


@app.route('/',methods=['POST','GET'])
def input():
	return render_template('form.html')
	






if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port,debug=True)
