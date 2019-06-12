#!/usr/bin/env python3
from flask import Flask
import os
import csv
from flask import render_template
from flask import request

app = Flask(__name__)

# print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))
print(port)

# @app.route('/')
# def hello_world():
# 	return"Pengyun Wang ID:1710"
	# return 'Hello World! I am running on port ' + str(port)
@app.route('/pic')
def pic():
	# os.walk(r'/static')
	# print(g)
	list=[]
	for path,dir_list,file_list in 	os.walk(r'static'):
		# print(dir_list)
		# print(file_list)
		for file_name in file_list:
			list.append((file_name,os.path.getsize(os.path.join('static/',file_name))))
			print(file_name)
			print(os.path.getsize(os.path.join('static/',file_name)))
	# print('/static/')
	# with open("./people.csv", "r") as fr:
	# 	rows = csv.reader(fr)

	# 	for row in rows:
	# 		print( row[0])
	return render_template('Pic.html',data=list)
@app.route('/choose')
def choose():
	id=request.args.get('id')
	list=[]
	with open("./people.csv", "r") as fr:
		rows = csv.reader(fr)
		for row in rows:
			if id == row[1]:
				print(row[4])
				list.append(row)
		return render_template('search.html',data=list) 
	
	# return 'no picture available'
@app.route('/choose2')
def choose2():
	startid=request.args.get('start')
	endid=request.args.get('end')
	favor=request.args.get('favor')
	list=[]
	if int(startid)>int(endid):
		return 'Ur input is invalid, plz go back'
	with open("./people.csv", "r") as fr:
		rows = csv.reader(fr)
		for row in rows:
			if row[0]=='Name':
				list.append(row)
			else:
				if row[1] == '':
					pass
				else:
					if int(row[1])>int(startid) and int(row[1])<int(endid):
						if favor in row[5]:
							print(row[0])
							list.append(row)
					# print(row[3]+'>'+endid)
					
					
		return render_template('showinfo.html',data=list) 	
@app.route('/choose3')
def choose3():
	point=request.args.get('point')
	name=request.args.get('name')
	nname=request.args.get('nname')
	npoint=request.args.get('npoint')
	favor=request.args.get('favor')
	list=''
	rows1=[]
	headers=[]
	with open("./people.csv", "r") as fr:
		rows = csv.reader(fr)
		for row in rows:
	

			if point ==row[1] and name==row[0]:
				print(row[0])
				row[0]=nname
				row[1]=npoint
				row[5]=favor
			rows1.append(row)

			list+=row[0]+','+row[1]+','+row[2]+','+row[3]+','+row[4]+','+row[5]+'\n'
	with open("./people.csv", "w") as fr:
		fr.write(list)
	return render_template('showinfo.html',data=rows1) 	



	# if id=='CA' or id=='ca':
	# 	return render_template('pic1.html')
	# elif id=='TX' or id=='tx':
	# 	return render_template('pic2.html')
	# elif id=='NN' or id=='nn':
	# 	return render_template('pic3.html')
	# elif id =='OK' or id=='ok':
	# 	return render_template('pic4.html')
	# else:
	# 	return('no picture available')
# @app.route()
@app.route('/',methods=['POST','GET'])
def input():
	if request.method=='POST':
		f=request.files['file']
		basepash=os.path.dirname(__file__)
		uploadpath=os.path.join(basepash,'static/',f.filename)
		f.save(uploadpath)

	return render_template('form.html')



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port,debug=True)
