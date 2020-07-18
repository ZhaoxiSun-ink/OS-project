#Summer 2020 CSCI 4210 Operating Systems project 1
#Team Members: Zhaoxi Sun, Xinyan Sun, Tongyu Wang, Yueting Liao
import sys #get argument
import math # get log
from process import Process#get process class
from rand48 import Rand48

#global variable
letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q',
           'R','S','T','U','V','W','X','Y','Z']

#main part
if __name__ == '__main__':
	if len(sys.argv) != 9:
		print("ERROR: Invalid argument.")
		sys.exit(2)

	n = int(sys.argv[1])
	seed = int(sys.argv[2])
	parameter = float(sys.argv[3])
	upper_bound = float(sys.argv[4])
	t_cs = float(sys.argv[5])
	alpha = float(sys.argv[6])
	t_slice = float(sys.argv[7])
	rradd = float(sys.argv[8])
	
	processes = []
	
	#random generator
	generator = Rand48(0)
	generator.srand(seed)
	
	for x in range(n):
		pid = letters[x]
		temp = generator.drand()
		arr = -(math.log(temp)) / parameter
		num_burst = math.floor(generator.drand())+1
		burst = []
		io = []
		for y in range(num_burst-2):
			burst.append(math.ceil(generator.drand()))
			io.append(math.ceil(generator.drand()))
		burst.append(math.ceil(generator.drand()))
		process = Process(pid,arr,burst,io)
		processes.append(process)
		
	for process in processes:
		process.print()