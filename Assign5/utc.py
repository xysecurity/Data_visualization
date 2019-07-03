from sklearn.cluster import KMeans
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
import base64
from io import BytesIO

db=sqlite3.connect('1.db')
cu=db.cursor()
data=cu.execute('select * from titanic3')
data2=[]
list=[]
for row in data:
	if row[4] and row[8]:
		list.append((float(row[4]),float(row[8])))
db.commit()
db.close()

def kmeans(list,kn):
	# X = np.array([[15, 17], [12,18], [14,15], [13,16], [12,15], [16,12],
	# 	[4,6], [5,8], [5,3], [7,4], [7,2], [6,5]])
	X=np.array(list)
	# print(X)
	y_pred = KMeans(n_clusters=kn, random_state=0).fit_predict(X)
	k=KMeans(n_clusters=kn, random_state=0,n_init=20).fit(X)
	print(y_pred)
	print(k)
	print(k.cluster_centers_)
	print(k.inertia_)
	print(k.labels_)
	plt.figure(figsize=(8, 8))
	plt.grid(linestyle='--',linewidth='0.5')
	plt.xlabel('Age')
	plt.ylabel('Fare')
	# color = ("red", "green",'blue','yellow','black','magenta')
	# colors=np.array(color)[y_pred]
	plt.scatter(X[:, 0], X[:, 1],cmap=plt.cm.coolwarm,alpha='0.5',label='$quake$')
	plt.scatter(k.cluster_centers_[:,0],k.cluster_centers_[:,1],c='r',marker='+',label='$center$',alpha='0.8')
	plt.legend()
	plt.show()
	sio=BytesIO()
	plt.savefig(sio,format='png')
	data=base64.encodebytes(sio.getvalue()).decode()
	# print(data)
	return data
	plt.close()

kmeans(list,8)
data={}
data['test']='test'
list=[1,2]
print(list+[3])
print(data)
print(data.get('test'))

i=3
lists=[[] for i in range(i)]
print(lists)
print(lists[0])

