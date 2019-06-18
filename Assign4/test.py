count=[[1,5,0],[5,10,0],[10,20,0],[20,50,0],[50,100,0]]
if 65>count[4][0] and 90<count[4][1]:
	count[4][2]+=1

print(range(len(count)))
for i in range(len(count)):
	print (count[i])
print(65>count[4][0] and 110<count[4][1])
