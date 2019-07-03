#!/usr/bin/env python3
from flask import Flask
from io import BytesIO
import base64
import os
import csv
from flask import render_template
from flask import request
import sqlite3
from math import radians, cos, sin, asin, sqrt
from sklearn.cluster import KMeans
import numpy as np
import json
import time
import math



application = Flask(__name__)
app=application

# print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))
print(port)
db=sqlite3.connect('1.db')
cu=db.cursor()
data=cu.execute('select * from minnow')
data2=[]
for row in data:
	data2.append(row)
db.commit()
db.close()

def cal_distance(d1,d2):
	p1=np.array(d1)
	p2=np.array(d2)
	p3=p2-p1
	p4=math.hypot(p3[0],p3[1])
	return p4





# @app.route('/')
# def hello_world():
# 	return"Pengyun Wang ID:1710"
	# return 'Hello World! I am running on port ' + str(port)
	


@app.route('/',methods=['POST','GET'])
def input():
	if request.method=='POST':
		f=request.files['file']
		basepash=os.path.dirname(__file__)
		uploadpath=os.path.join(basepash,'static/',f.filename)
		f.save(uploadpath)

	return render_template('form.html')






@app.route('/chart')
def chart():
	bn=int(request.args.get('bn'))
	v1=int(request.args.get('choice1'))
	v2=int(request.args.get('choice2'))
	v1_start=float(request.args.get('v1_start'))
	v1_end=float(request.args.get('v1_end'))
	v2_start=float(request.args.get('v2_start'))
	v2_end=float(request.args.get('v2_end'))


	list=[]
	list2=[]
	for row in data2:

		if row[v1] and row[v2]:
			if float(row[v1])>=v1_start and float(row[v1])<v1_end and float(row[v2])>=v2_start and float(row[v2])<v2_end:
				list.append([float(row[v1]),float(row[v2])])

	X=np.array(list)

	k=KMeans(n_clusters=bn, random_state=0,n_init=20).fit(X)
	# print(k)
	# print(k.cluster_centers_)
	center=[]
	for i in k.cluster_centers_.tolist():
		center.append([int(i[0]),int(i[1])])

	div=k.labels_
	i=bn
	list_len=[]
	distance_list=[]
	tmp=[]

	lists=[[] for i in range(i)]
	for i in range(len(div)):
		lists[div[i]].append(list[i])
	print(lists)
	for i in range(len(lists)):
		for j in lists[i]:
			tmp.append(cal_distance(j,center[i]))
		print(tmp)
		distance_list.append(max(tmp))
		tmp=[]

	for i in lists:
		list_len.append(len(i))


	print(lists)



	return render_template('bar.html',c=bn,list_len=list_len,center=center,distance=distance_list)





@app.route('/database2')
def database2():
	bn=int(request.args.get('bn'))
	v1=int(request.args.get('choice1'))
	v2=int(request.args.get('choice2'))
	v1_start=float(request.args.get('v1_start'))
	v1_end=float(request.args.get('v1_end'))
	v2_start=float(request.args.get('v2_start'))
	v2_end=float(request.args.get('v2_end'))
	x=0
	y=0
	if request.args.get('x') and request.args.get('y'):

		x=float(request.args.get('x'))
		y=float(request.args.get('y'))

	list=[]
	list2=[]
	for row in data2:

		if row[v1] and row[v2]:
			if float(row[v1])>=v1_start and float(row[v1])<v1_end and float(row[v2])>=v2_start and float(row[v2])<v2_end:
				list2.append(row)

				list.append([float(row[v1]),float(row[v2])])

	X=np.array(list)

	k=KMeans(n_clusters=bn, random_state=0,n_init=20).fit(X)
	# print(k)
	# print(k.cluster_centers_)
	center=k.cluster_centers_.tolist()
	div=k.labels_
	i=bn
	list_len=[]
	distance_list=[]
	tmp=[]

	lists=[[] for i in range(i)]
	for i in range(len(div)):
		lists[div[i]].append(list[i])
	# print(lists)
	for i in range(len(lists)):
		for j in lists[i]:
			tmp.append(cal_distance(j,center[i]))
		# print(tmp)
		distance_list.append(max(tmp))
		tmp=[]

	for i in lists:
		list_len.append(len(i))


	print(lists)

	user_data=[]
	for i in range(len(center)):
		if x and y:
			if float(center[i][0])==x and float(center[i][1])==y:
				data=lists[i]
				print(data)
				for i in data:
					for j in list2:												
						if float(i[0])==float(j[v1]) and float(i[1])==float(j[v2]):
							print(i)
							user_data.append(j)

	user_data={}.fromkeys(user_data).keys()




	return render_template('k2.html',c=bn,list_len=list_len,center=k.cluster_centers_.tolist(),distance=distance_list,user_data=user_data)

@app.route('/database')
def database():
	# bn=int(request.args.get('bn'))
	list=[]
	list2=[]
	for row in data2:

		if row[6] and row[4]:

			list.append([float(row[6]),float(row[4])])
		if row[10] and row[3]:
			list2.append([float(row[10]),float(row[3])])
	start=time.time()
	X=np.array(list)

	k=KMeans(n_clusters=4, random_state=0,n_init=20).fit(X)
	end=time.time()
	time1=end-start
	start=time.time()
	X1=np.array(list2)


	
	k2=KMeans(n_clusters=3, random_state=0,n_init=20).fit(X1)
	end=time.time()
	time2=end-start

	div=k.labels_
	div2=k2.labels_
	b=4
	j=3
	lists=[[] for i in range(b)]
	lists2=[[] for i in range(j)]
	list_len=[]
	list_len2=[]

	for i in range(len(div)):
		lists[div[i]].append(list[i])
	for i in range(len(div2)):
		lists2[div2[i]].append(list2[i])
	for i in lists:
		list_len.append(len(i))
	for i in lists2:
		list_len2.append(len(i))




	return render_template('k.html',c1=b,c2=j,time1=time1,time2=time2,list_len=list_len,list_len2=list_len2,center=k.cluster_centers_.tolist(),center2=k2.cluster_centers_.tolist())






if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port,debug=True)
