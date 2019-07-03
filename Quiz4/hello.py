#!/usr/bin/env python3
from flask import Flask
from io import BytesIO
import os
import base64
import csv
from flask import render_template
from flask import request
import sqlite3
from timeit import timeit
import json

app = Flask(__name__)

# print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))
print(port)
# r=redis.Redis(host='localhost',port=6379,decode_responses=True)
db=sqlite3.connect('1.db')
cu=db.cursor()
data=cu.execute('select * from voting')
data2=[]
i=0
for row in data:
	row1=([row[0],row[1].replace(',',''),row[2].replace(',', ''),row[3].replace(',', ''),row[4].replace(',', '')])
	data2.append(row1)
	# r.set(i,str(row))
db.commit()
db.close()

# def kmeans(list,kn):
# 	# X = np.array([[15, 17], [12,18], [14,15], [13,16], [12,15], [16,12],
# 	# 	[4,6], [5,8], [5,3], [7,4], [7,2], [6,5]])
# 	X=np.array(list)
# 	# print(X)
# 	y_pred = KMeans(n_clusters=kn, random_state=0).fit_predict(X)
# 	k=KMeans(n_clusters=kn, random_state=0).fit(X)
# 	print(y_pred)
# 	print(k)
# 	print(k.cluster_centers_)

# 	color = ("red", "green",'blue','yellow','black','magenta')
# 	colors=np.array(color)[y_pred]
# 	print(colors)
# 	plt.scatter(X[:, 0], X[:, 1],c=colors,cmap=plt.cm.coolwarm,alpha='0.5',label='$quake$')
# 	plt.scatter(k.cluster_centers_[:,0],k.cluster_centers_[:,1],c='r',marker='+',label='$center$',alpha='0.8')
# 	plt.legend()
# 	# plt.show()
# 	sio=BytesIO()
# 	plt.savefig(sio,format='png')
# 	data=base64.encodebytes(sio.getvalue()).decode()
# 	# print(data)
# 	return data
# 	plt.close()

def cal(number):
	a=number*number*number
	str1=''
	str1=str(a)
	int1=0
	int1=int(str1[-1])
	return int1

@app.route('/bar')
def bar():
	# db=sqlite3.connect('1.db')
	# cu=db.cursor()
	# data=cu.execute('select * from all_month')
	num=int(request.args.get('for_num'))
	list=[]
	for i in range(1,num+1):
		list.append(cal(i))
	print(list)
	dict={}
	for i in list:
		dict[i]=dict.get(i,0)+1
	print(dict)
	names=[]
	values=[]
	for i in dict:
		names.append(i)
		values.append(dict.get(i,0))
	print(names)
	print(values)



	
	list2=[]

	return render_template('bar.html',names=names,values=values)





# @app.route('/kmean')
# def kmean():
# 	list=[]
# 	for row in data2:
# 		list.append((row[1],row[2]))

# 	# return html.format(kmeans(list,kn))
# 	return render_template('kmean.html',base64=kmeans(list,6))



@app.route('/pie')
def pie():
	incre=int(request.args.get('incre'))
	group=[]
	i=0
	while i<50:
		group.append([i,i+incre,0])
		i=i+incre
	for row in data2:
		for j in range(len(group)):

			if (float(row[1])/1000)>=group[j][0] and (float(row[1])/1000)<group[j][1]:
				group[j][2]+=1
	names=[]
	count=[]
	for j in group:
		names.append((str(j[0])+'-'+str(j[1])))
		count.append({'name':(str(j[0])+'-'+str(j[1])),'value':j[2]})
	return render_template('pie.html',names=names,count=count)



@app.route('/scatter')
def scatter():
	pop_start=float(request.args.get('pop_start'))
	pop_end=float(request.args.get('pop_end'))
	list=[]
	for row in data2:
		if (float(row[1])/1000)>=pop_start and (float(row[1])/1000)<pop_end:
			list.append([(float(row[1])/1000),(float(row[3])/1000)])


	return render_template('scatter.html',list=list)




@app.route('/pop')
def searchtable():
	list1=[]
	list2=[]
	for row in data2:
		if float(row[1])>=2000 and float(row[1])<8000:
			list1.append(row)
		elif float(row[1])>=8000 and float(row[1])<40000:
			list2.append(row)



	return render_template('pop.html',data1=list1,data2=list2)


@app.route('/',methods=['POST','GET'])
def input():
	return render_template('form.html')
	






if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port,debug=True)
