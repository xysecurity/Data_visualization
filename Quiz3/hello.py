#!/usr/bin/env python3
from flask import Flask
from io import BytesIO
import base64
import os
import csv
from flask import render_template
from flask import request
import sqlite3
import random
import time
import redis

app = Flask(__name__)

# print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))
print(port)
db=sqlite3.connect('2.db')
cu=db.cursor()
data=cu.execute('select * from quake6')
r=redis.Redis(host='anakin.redis.cache.windows.net',port=6379,password='QuhFzLTrVd+LNdWaF1fAxikpgc6bdfiaimiqk2PJB44=',decode_responses=True)
data2=[]
for row in data:
	data2.append(row)
db.commit()
db.close()

@app.route('/choose')
def choose():
	start_dep=float(request.args.get('start_dep'))
	end_dep=float(request.args.get('end_dep'))
	lon=float(request.args.get('longitude'))
	# query_number=float(request.args.get('query_num'))
	db=sqlite3.connect('2.db')
	cu=db.cursor()
	data=cu.execute('select * from quake6 where depthError between %.1f and %.1f and longitude > %.1f' %(start_dep,end_dep,lon))
	list2=[]
	for row in data:
		# print(row[4])
		list2.append(row)


	return render_template('earchquake.html',data=list2)
	db.commit()
	db.close()
	
	# return 'no picture available'
@app.route('/choose2')
def choose2():
	start_lat=float(request.args.get('start_dep'))
	end_lat=float(request.args.get('end_dep'))
	query_number=int(request.args.get('query_num'))
	db=sqlite3.connect('2.db')
	cu=db.cursor()
	list2=[]
	for i in range(1,query_number):
		a=0
		b=0
		while a==b:
			a=round(random.uniform(start_lat,end_lat),1)
			b=round(random.uniform(start_lat,end_lat),1)		
		if a>b:
			big=a
			small=b
		else:
			big=b
			small=a
		start=time.time()
		data=cu.execute('select count(time) from quake6 where depthError between %.1f and %.1f' %(small,big))
		end=time.time()
		cost_time=end-start
		for cot in data:
			count=cot[0]
		list2.append([count,small,big,cost_time])


	return render_template('querytime.html',data=list2) 	


@app.route('/choose3')
def choose3():
	start_lat=float(request.args.get('start_dep'))
	end_lat=float(request.args.get('end_dep'))
	query_number=int(request.args.get('query_num'))
	db=sqlite3.connect('2.db')
	cu=db.cursor()
	
	list2=[]
	for i in range(1,query_number):
		a=0
		b=0
		count=0
		while a==b:
			a=round(random.uniform(start_lat,end_lat),1)
			b=round(random.uniform(start_lat,end_lat),1)		
		if a>b:
			big=a
			small=b
		else:
			big=b
			small=a
		start=time.time()
		redis_num=r.get('%.1f-%.1f'%(small,big))
		# print(r.get('%.1f-%.1f'%(small,big)),small,big)

		if redis_num and redis_num!=0:
			count=redis_num
		else:
			data=cu.execute('select count(time) from quake6 where depthError between %.1f and %.1f' %(small,big))
			for cot in data:
				count=cot[0]
			r.set('%.1f-%.1f'%(small,big),count)
			print(r.get('%.1f-%.1f'%(small,big)))

		end=time.time()
		cost_time=end-start

		list2.append([count,small,big,cost_time])


	return render_template('querytime.html',data=list2) 	



@app.route('/',methods=['POST','GET'])
def input():
	if request.args.get('start_dep') and request.args.get('end_dep') and request.args.get('query_num') and request.args.get('choice'):
		start_lat=float(request.args.get('start_dep'))
		end_lat=float(request.args.get('end_dep'))
		query_number=int(request.args.get('query_num'))
		choice=int(request.args.get('choice'))
		db=sqlite3.connect('2.db')
		cu=db.cursor()
		list2=[]
		if choice==1:
			start=time.time()
			for i in range(1,query_number):
				a=0
				b=0
				while a==b:
					a=round(random.uniform(start_lat,end_lat),1)
					b=round(random.uniform(start_lat,end_lat),1)		
				if a>b:
					big=a
					small=b
				else:
					big=b
					small=a
				data=cu.execute('select count(time) from quake6 where latitude between %.1f and %.1f' %(small,big))
				for cot in data:
					count=cot[0]

			end=time.time()
			cost_time=end-start
		else:
			start=time.time()
			for i in range(1,query_number):
				a=0
				b=0
				count=0
				while a==b:
					a=round(random.uniform(start_lat,end_lat),1)
					b=round(random.uniform(start_lat,end_lat),1)		
				if a>b:
					big=a
					small=b
				else:
					big=b
					small=a	
				redis_num=r.get('%.1f-%.1f'%(small,big))

				# print(redis_num)
				# print(small,big)

				if redis_num and redis_num!=0:
					count=redis_num
					# print(count,'get')
				else:
					data=cu.execute('select count(time) from quake6 where depthError between %.1f and %.1f' %(small,big))
					for cot in data:
						count=cot[0]
					r.set('%.1f-%.1f'%(small,big),count)
					# print(r.get('%.1f-%.1f'%(small,big)))
			end=time.time()
			cost_time=end-start
		return render_template('form.html',cost_time=cost_time)
	return render_template('form.html')





if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port,debug=True)
