import os

if __name__ == '__main__':	
	for path,dir_list,file_list in 	os.walk('static'):
		print(dir_list)
		print(file_list)
		for file_name in file_list:
			print(file_name)