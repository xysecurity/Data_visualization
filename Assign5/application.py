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
import json

matplotlib.use('Agg')

application = Flask(__name__)
app=application

# print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))
print(port)
db=sqlite3.connect('1.db')
cu=db.cursor()
data=cu.execute('select * from titanic3')
data2=[]
for row in data:
	data2.append(row)
db.commit()
db.close()


def kmeans(list,kn):
	# X = np.array([[15, 17], [12,18], [14,15], [13,16], [12,15], [16,12],
	# 	[4,6], [5,8], [5,3], [7,4], [7,2], [6,5]])
	X=np.array(list)
	print(X)
	y_pred = KMeans(n_clusters=kn, random_state=0).fit_predict(X)
	k=KMeans(n_clusters=kn, random_state=0,n_init=20).fit(X)
	print(y_pred)
	print(k)
	print(k.cluster_centers_)
	# plt.figure(figsize=(8, 8))
	# plt.grid(linestyle='--',linewidth='0.5')
	# plt.xlabel('Age')
	# plt.ylabel('Fare')
	# # color = ("red", "green",'blue','yellow','black','magenta')
	# # colors=np.array(color)[y_pred]
	# plt.scatter(X[:, 0], X[:, 1],cmap=plt.cm.coolwarm,alpha='0.5',label='$quake$')
	# plt.scatter(k.cluster_centers_[:,0],k.cluster_centers_[:,1],c='r',marker='+',label='$center$',alpha='0.8')
	# plt.legend()
	# # plt.show()
	# sio=BytesIO()
	# plt.savefig(sio,format='png')
	# data=base64.encodebytes(sio.getvalue()).decode()
	# # print(data)
	# return data
	# plt.close()
	return y_pred



# @app.route('/')
# def hello_world():
# 	return"Pengyun Wang ID:1710"
	# return 'Hello World! I am running on port ' + str(port)
	
@app.route('/kmean')
def kmean():
	datalist=[]
	i=-80
	j=-200

	while i != 80:
		j=-200
		while j !=200:
			datalist.append([i,i+20,j,j+50,0])
			j+=50
		i+=20
	kn=int(request.args.get('kn'))
	list=[]
	for row in data2:
		if row[4] and row[8]:

			list.append((float(row[4]),float(row[8])))
		# find_scope(float(row[1]),float(row[2]),datalist)
	print(datalist)
	datalist_sort=sorted(datalist,key=lambda x:x[4],reverse=True)
	# kmeans(list,6)
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

	return render_template('form.html')



@app.route('/database2')
def database2():
	bn=int(request.args.get('bn'))
	list=[]
	for row in data2:

		if row[4] and row[8]:

			list.append([float(row[4]),float(row[8])])
	X=np.array(list)

	k=KMeans(n_clusters=bn, random_state=0,n_init=20).fit(X)
	print(k)
	print(k.cluster_centers_)
	div=k.labels_
	i=bn
	lists=[[] for i in range(i)]
	for i in range(len(div)):
		lists[div[i]].append(list[i])
	center=k.cluster_centers_.tolist()
	lists.append(center)
	print(lists)



	return render_template('scatter.html',data=lists)


@app.route('/database')
def database():
	bn=int(request.args.get('bn'))
	list=[]
	for row in data2:

		if row[4] and row[8]:

			list.append([float(row[4]),float(row[8])])
	X=np.array(list)

	k=KMeans(n_clusters=bn, random_state=0,n_init=20).fit(X)
	print(k)
	print(k.cluster_centers_)
	div=k.labels_
	i=bn
	lists=[[] for i in range(i)]
	for i in range(len(div)):
		lists[div[i]].append(list[i])
	print(lists)

	return render_template('k.html',total=len(list),center=k.cluster_centers_.tolist(),distance=k.inertia_)






if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port,debug=True)
