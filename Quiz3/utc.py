# def calctime(curlon):
# 	shangValue=int(curlon//15)
# 	yuValue=float(curlon%15)
# 	if yuValue<=7.5 and yuValue>-7.5:
# 		return shangValue
# 	else:
# 		if yuValue<=-7.5:
# 			return shangValue-1
# 		else:
# 			return shangValue+1


# print(calctime(22.5))
# print('08'>'17')
# print(int('08'))

list=[]
i=0
a=0
j=0

# for i in range(90):
# 	for j in range(180):
# 		list.append([i,i+1,j,j+1,0])
# a=[80,110]
# print(len(list))
# print(list2)

# while i != 90:
# 	j=0
# 	while j !=180:
# 		list.append([i,i+5,j,j+5,0])
# 		j+=5
# 	i+=5

#  print (list)

# for i in range(len(list)):
# 	if (a[0]>=list[i][0] and a[0]<list[i][1]) and (a[1]>=list[i][2] and a[1]<list[i][3]):
# 		list[i][4]+=1
# 		print(list[i])

# print(min('test','tes'))
# print(float(0.2))
import sqlite3
import redis
r=redis.Redis(host='anakin.redis.cache.windows.net',port=6379,password='QuhFzLTrVd+LNdWaF1fAxikpgc6bdfiaimiqk2PJB44=',decode_responses=True)
db=sqlite3.connect('2.db')
cu=db.cursor()
data=cu.execute('select * from quake6')
i=0
r.set('1-2',300)

# for row in data:
# 	r.set('a%d'%i,row[9])
# 	i+=1
# 	print(row[9])
print(r.get('5.0-9.4'))
small=5.0
big=9.4
print(r.get('%.1f-%.1f'%(small,big)),small,big)
print('%.1f-%.1f'%(small,big))


