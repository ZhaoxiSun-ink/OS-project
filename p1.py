#Summer 2020 CSCI 4210 Operating Systems project 1
#Team Members: Zhaoxi Sun, Xinyan Sun, Tongyu Wang, Yueting Liao
import sys #get argument
import math # get log
from process import Process#get process class
from copy import deepcopy
from rand48 import Rand48
from queue import PriorityQueue
from collections import deque

#global variable
letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q',
           'R','S','T','U','V','W','X','Y','Z']

#check upper_bound
def checkUpperBound(upper):
	while(True):
		temp = generator.drand()
		if(temp > upper):
			continue
		else:
			return temp

def FCFS(processes):
	waiting_queue = []
	event_queue = PriorityQueue()
	event_queue.put((4, "first"))
	event_queue.put((3, "Third"))
	event_queue.put((2, "Second"))
	for i in range(3):
		a = event_queue.get()
		print(a)


# Shortest Job First (SJF) algorithm
# It runs the process in order of shortest ESTIMATED CPU burst times

#arg line - python3 p1.py 1 2 0.05 256 4 0.5 128 3
#   tau i+1 =  alpha x t i   +  (1-alpha) x tau i
def SJF(processes):
    tau_0 = (1/parameter) # For every process, tau_0 = 1/lambda
    for process in processes:
        print(process.name)
        tau_i = tau_0
        estimated_brust_time = list()
        for i in range(len(process.burst_times)):
            tau_i = math.ceil( alpha * process.burst_times[i] + (1-alpha) * tau_i )
            print("actual CPU brust: {} | estimated CPU brust {}".format(process.burst_times[i], tau_i) )
            estimated_brust_time.append(tau_i)
        process.setEstimatedBurstTime(estimated_brust_time)
        process.printEstimatedBurstTime()

def SRT(processes):
	pass
		
def RR(processes):
	pass

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
		temp = checkUpperBound(upper_bound)
		arr = math.floor(-(math.log(temp)) / parameter)
		num_burst = math.floor(checkUpperBound(upper_bound)*100)+1
		burst = []
		io = []
		for y in range(num_burst-1):
			a = checkUpperBound(upper_bound)
			b = checkUpperBound(upper_bound)
			burst.append(math.ceil(-(math.log(a)) / parameter))
			io.append(math.ceil(-(math.log(b)) / parameter))
		c = checkUpperBound(upper_bound)
		burst.append(math.ceil(-(math.log(c)) / parameter))
		process = Process(pid,arr,burst,io)
		processes.append(process)

processes1 = deepcopy(processes)
processes2 = deepcopy(processes)
processes3 = deepcopy(processes)
processes4 = deepcopy(processes)
FCFS(processes1)
SJF(processes2)
