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
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

# print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))
print(port)
db=sqlite3.connect('2.db')
cu=db.cursor()
data=cu.execute('select * from quakes')
data2=[]
for row in data:
	data2.append(row)
db.commit()
db.close()
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
 
    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # 地球平均半径，单位为公里
    return c * r 

@app.route('/choose')
def choose():
	# db=sqlite3.connect('1.db')
	# cu=db.cursor()
	# data=cu.execute('select * from all_month')
	list=[]
	list2=[]
	for row in data2:
		# print(row[4])
		if row[4]==None:
			pass
		else:
			if float(row[4])>2.0:
				list.append(row)
	list_sort=sorted(list,key=lambda x:x[4])
	list2.append(list_sort[0])




	return render_template('earchquake.html',data=list2)
	
	# return 'no picture available'
@app.route('/choose2')
def choose2():
	startid=float(request.args.get('start'))
	endid=float(request.args.get('end'))
	incre=float(request.args.get('increment'))
	interval_list=[]
	while startid<endid:
		interval_list.append([round(startid,2),round(startid+incre,2),0])
		startid+=incre
	print(interval_list)

	list=[]
	
	for row in data2:
		if row[3] and row[0]:
			for i in interval_list:
				if float(row[3])>=i[0] and float(row[3])<i[1]:
					i[2]+=1
	print(interval_list)
				

	# with open("./people.csv", "r") as fr:
	# 	rows = csv.reader(fr)
	# 	for row in rows:
	# 		if row[0]=='Name':
	# 			list.append(row)
	# 		else:
	# 			if row[1] == '':
	# 				pass
	# 			else:
	# 				if int(row[1])>int(startid) and int(row[1])<int(endid):
	# 					if favor in row[5]:
	# 						print(row[0])
	# 						list.append(row)
					# print(row[3]+'>'+endid)			
	return render_template('count.html',data=interval_list) 	
@app.route('/choose3')
def choose3():
	latitude1=float(request.args.get('latitude1'))
	longitude1=float(request.args.get('longitude1'))
	latitude2=float(request.args.get('latitude2'))
	longitude2=float(request.args.get('longitude2'))

	l_latitude=max(latitude1,latitude2)
	s_latitude=min(latitude1,latitude2)
	l_longitude=max(longitude1,longitude2)
	s_longitude=min(longitude1,longitude2)

	list=[]
	# print(data2[0])
	# print(haversine(float(longitude),float(latitude),data2[0][2],data2[0][1]))
	for row in data2:
		if float(row[1])>=s_latitude and float(row[1])<l_latitude and float(row[2])>=s_longitude and float(row[2])<l_longitude:

			list.append(row)





	# with open("./people.csv", "r") as fr:
	# 	rows = csv.reader(fr)
	# 	for row in rows:
	

	# 		if point ==row[1] and name==row[0]:
	# 			print(row[0])
	# 			row[0]=nname
	# 			row[1]=npoint
	# 			row[5]=favor
	# 		rows1.append(row)

	# 		list+=row[0]+','+row[1]+','+row[2]+','+row[3]+','+row[4]+','+row[5]+'\n'
	# with open("./people.csv", "w") as fr:
	# 	fr.write(list)
	return render_template('earchquake.html',data=list) 
@app.route('/choose4')	
def choose4():
	start_time=request.args.get('start_time')
	end_time=request.args.get('end_time')
	start_dep=float(request.args.get('start_dep'))
	end_dep=float(request.args.get('end_dep'))

	list=[]
	for row in data2:

		if row[0][:10]>=start_time and row[0][:10]<=end_time and float(row[3])>=start_dep and float(row[3]) <=end_dep:
			print(row)

			list.append(row)
	print(list)
	# edit
	db=sqlite3.connect('2.db')
	cu=db.cursor()
	for row in list:
		time1=row[0]
		exe=cu.execute("UPDATE quakes set depth='999' WHERE time='%s'"%time1)
	db.commit()

	return render_template('earchquake.html',data=list)

@app.route('/choose5')	
def choose5():
	latitude=request.args.get('latitude')
	longitude=request.args.get('longitude')
	distance=request.args.get('distance')
	location=request.args.get('location')
	list=[]
	for row in data2:
		if haversine(float(longitude),float(latitude),row[2],row[1])<int(distance) or row[6].find(location)>0:

			list.append(row)
	return render_template('earchquake.html',data=list)








@app.route('/kmean')
def kmean():
	datalist=[]
	i=-80
	j=-200
# for i in range(90):
# 	for j in range(180):
# 		datalist.append([i,i+1,j,j+1,0])
	while i != 80:
		j=-200
		while j !=200:
			datalist.append([i,i+20,j,j+50,0])
			j+=50
		i+=20
	kn=int(request.args.get('kn'))
	list=[]
	for row in data2:
		list.append((row[1],row[2]))
		find_scope(float(row[1]),float(row[2]),datalist)
	print(datalist)
	datalist_sort=sorted(datalist,key=lambda x:x[4],reverse=True)
	# kmeans(list,6)
	html= '''
       <html>
           <body>
           <div style='text-align:center;'>
<img src="data:image/png;base64,{}" />
           </div>
               
           </body>
        <html>
    '''



	# return html.format(kmeans(list,kn))
	return render_template('kmean.html',base64=kmeans(list,kn),data=datalist_sort)

@app.route('/predict')
def predict():
	mg=float(request.args.get('mg'))
	list=[]
	ct_l_day=ct_l_night=ct_s_day=ct_s_night=0
	for row in data2:
		if row[4] and row[0]:
			local_time=int(row[0][11:13])+calctime(float(row[2]))
			if local_time<=0:
				local_time=24+local_time

			# print(local_time)
			if float(row[4])>=mg:
				if (local_time >= 0 and local_time <= 6) or ( local_time >18 and local_time<=24):
					print('18:00<='+str(local_time)+'<=24:00'+'or'+'00:00<='+str(local_time)+'<=06:00')
					ct_l_night+=1
				else:
					ct_l_day+=1
			# if 
			else:
				if (local_time >= 0 and local_time <= 6) or ( local_time >18 and local_time<=24):
					ct_s_night+=1
				else:
					ct_s_day+=1
	list.append((ct_l_day,ct_l_night,ct_s_day,ct_s_night))
	return render_template('count.html',data=list)





@app.route('/',methods=['POST','GET'])
def input():
	if request.method=='POST':
		f=request.files['file']
		basepash=os.path.dirname(__file__)
		uploadpath=os.path.join(basepash,'static/',f.filename)
		f.save(uploadpath)
	number=len(data2)

	return render_template('form.html',number=number)
@app.route('/database')
def database():
	db=sqlite3.connect('1.db')
	cu=db.cursor()
	data=cu.execute('select * from all_month')

	return render_template('earchquake.html',data=data)
	db.close()






if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port,debug=False)
