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
from tzwhere import tzwhere
tz=tzwhere.tzwhere()
print(tz.tzNameAt(39.54,116.23))

list=[]
i=0
a=0
j=0

# for i in range(90):
# 	for j in range(180):
# 		list.append([i,i+1,j,j+1,0])
a=[80,110]
print(len(list))
# print(list2)

# while i != 90:
# 	j=0
# 	while j !=180:
# 		list.append([i,i+5,j,j+5,0])
# 		j+=5
# 	i+=5

# # print (list)

# for i in range(len(list)):
# 	if (a[0]>=list[i][0] and a[0]<list[i][1]) and (a[1]>=list[i][2] and a[1]<list[i][3]):
# 		list[i][4]+=1
# 		print(list[i])

