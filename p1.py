#Summer 2020 CSCI 4210 Operating Systems project 1
#Team Members: Zhaoxi Sun, Xinyan Sun, Tongyu Wang, Yueting Liao
import sys #get argument
import math # get log
from process import Process#get process class
from copy import deepcopy
from rand48 import Rand48
from queue import PriorityQueue

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

def FCFS(processes, cst):
	"""def printwq(waitq):
		string = " "
		for element in waitq:
			string = string + element + " """
		
	# preprocessing
	process_table = {}
	waiting_queue = []
	event_queue = PriorityQueue()
	time = 0
	current_running = None
	CPU_vacant_at = -1
	# push all processes to event_queue
	for process in processes:
		arrival_time = process.getArrivalTime()
		name = process.getName()
		event_queue.put((arrival_time, (name, "Arrive")))
		process_table[name] = process
		print("Process {} [NEW] (arrival time {} ms) {} CPU bursts".format(process.getName(), process.getArrivalTime(), process.getTotalBursts()))
	print("time 0ms: Simulator started for FCFS [Q <empty>]")
	while(len(process_table) > 0):
		next_event = event_queue.get()
		time = next_event[0]
		process_name = next_event[1][0]
		event_type = next_event[1][1]
		process = process_table[process_name]
		if event_type == "Arrive":
			process.arrive()
			waiting_queue.append(process_name)
			print("time {}ms: Process {} arrived; added to ready queue [Q {}]".format(time, process_name, waiting_queue))
			if len(waiting_queue) == 0 and (current_running == None or time >= CPU_vacant_at):
				waiting_queue.pop(0)
				event_queue.put((time + cst, (process_name, "Run")))
				process.startContextSwitchIn(time)
				current_running = process_name
		elif event_type == "Run":
			expected = process.startRunning(time)
			event_queue.put((time + expected, (process_name, "CSOut")))
			CPU_vacant_at = time + expected + cst
			print("time {}ms: Process {} started using the CPU for {}ms burst [Q {}]".format(time, process_name, expected, waiting_queue))
		elif event_type == "CSOut":
			process.startContextSwitchOut(time)
			event_queue.put((time + cst, (process_name, "EnterIO")))
			print("time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, process.total_bursts-process.index-1, waiting_queue))
			if process.index < process.total_bursts - 1:
				print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, time + cst + process.io_times[process.index], waiting_queue))
		elif event_type == "EnterIO":
			expected = process.finishRunning(time)
			if expected == -1:
				print("time {}ms: Process {} terminated [Q {}]".format(time, process_name, waiting_queue))
				del process_table[process_name]
				continue
			event_queue.put((time + expected, (process_name, "EnterQueue")))
			current_running = None
			# Start running another immediately, if there is another one on the waiting queue
			if len(waiting_queue) > 0:
				new_name = waiting_queue.pop(0)
				new_process = process_table[new_name]
				event_queue.put((time + cst, (new_name, "Run")))
				new_process.startContextSwitchIn(time)
				current_running = new_name
		elif event_type == "EnterQueue":
			process.finishIO(time)
			waiting_queue.append(process_name)
			print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]".format(time, process_name, waiting_queue))
			if len(waiting_queue) == 0 and (current_running == None or time >= CPU_vacant_at):
				waiting_queue.pop(0)
				event_queue.put((time + cst, (process_name, "Run")))
				process.startContextSwitchIn(time)
				current_running = process_name
		else:
			print("Something went wrong")
			return
	

def SJF(processes):
	pass

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
	FCFS(processes1, t_cs/2)
