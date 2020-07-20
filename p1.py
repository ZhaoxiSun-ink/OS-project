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
		temp = math.ceil(-(math.log(generator.drand())) / parameter)
		if(temp > upper):
			continue
		else:
			return temp

def FCFS(processes, cst):
	def printwq(waitq):
		if len(waitq) == 0:
			return "<empty>"
		ans = waitq[0]
		for i in range(1, len(waitq)):
			ans = ans + " " + waitq[i]
		return ans
	# preprocessing
	process_table = {}
	waiting_queue = []
	event_queue = PriorityQueue()
	time = 0
	current_running = None
	CPU_vacant_at = -1
	context_switch_count = 0
	# push all processes to event_queue
	for process in processes:
		arrival_time = process.getArrivalTime()
		name = process.getName()
		event_queue.put((arrival_time, (name, "Arrive")))
		process_table[name] = process
		print("Process {} [NEW] (arrival time {} ms) {} CPU bursts".format(process.getName(), process.getArrivalTime(), process.getTotalBursts()))
	print("time 0ms: Simulator started for FCFS [Q <empty>]")
	while(len(process_table) > 0):
		next_event = event_queue.get(block=False)
		time = int(next_event[0])
		process_name = next_event[1][0]
		event_type = next_event[1][1]
		process = process_table[process_name]
		if event_type == "Arrive":
			process.arrive()
			waiting_queue.append(process_name)
			print("time {}ms: Process {} arrived; added to ready queue [Q {}]".format(time, process_name, printwq(waiting_queue)))
			if len(waiting_queue) == 1 and (current_running == None or time >= CPU_vacant_at):
				waiting_queue.pop(0)
				event_queue.put((time + cst, (process_name, "Run")))
				process.startContextSwitchIn(time)
				current_running = process_name
		elif event_type == "Run":
			expected = process.startRunning(time)
			event_queue.put((time + expected, (process_name, "CSOut")))
			CPU_vacant_at = time + expected + cst
			print("time {}ms: Process {} started using the CPU for {}ms burst [Q {}]".format(time, process_name, expected, printwq(waiting_queue)))
		elif event_type == "CSOut":
			process.startContextSwitchOut(time)
			event_queue.put((time + cst, (process_name, "EnterIO")))
			print("time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, process.total_bursts-process.index-1, printwq(waiting_queue)))
			if process.index < process.total_bursts - 1:
				print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, int(time + cst + process.io_times[process.index]), printwq(waiting_queue)))
			context_switch_count += 1
		elif event_type == "EnterIO":
			expected = process.finishRunning(time)
			if expected == -1:
				print("time {}ms: Process {} terminated [Q {}]".format(time, process_name, printwq(waiting_queue)))
				del process_table[process_name]
			else:
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
			print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]".format(time, process_name, printwq(waiting_queue)))
			if len(waiting_queue) == 1 and (current_running == None or time >= CPU_vacant_at):
				waiting_queue.pop(0)
				event_queue.put((time + cst, (process_name, "Run")))
				process.startContextSwitchIn(time)
				current_running = process_name
		else:
			print("ERROR: <error-text-here>")
			return



# Shortest Job First (SJF) algorithm
# It runs the process in order of shortest ESTIMATED CPU burst times

#arg line - python3 p1.py 5 2 0.05 256 4 0.5 128 3
def SJF(processes, cst):
    # convert the ready_queue list to string
    def print_ready_queue(waitq):
        if len(waitq) == 0:
            return "<empty>"
        ans = waitq[0]
        for i in range(1, len(waitq)):
            ans = ans + " " + waitq[i]
        return ans
    # caculating tau (estimated_brust_time)
    def recaculate_tau(process, index):
        # tau_i+1 =  alpha x t_i   +  (1-alpha) x tau i
        tau_i = math.ceil( alpha * process.burst_times[index] + (1-alpha) * process.estimated_brust_time )
        process.estimated_brust_time = tau_i

    for process in processes:
        tau_0 = (1/parameter) # For every process, tau_0 = 1/lambda
        process.estimated_brust_time = tau_0

    #waiting_queue, sorted by arrival time
    process_table = dict()
    ready_queue = list()
    event_queue = PriorityQueue()
    time = 0
    current_running = None
    CPU_vacant_at = -1
    context_switch_count = 0
    # push all processes to event_queue
    for process in processes:
        arrival_time = process.getArrivalTime()
        name = process.getName()
        event_queue.put((arrival_time, (name, "Arrive")))
        process_table[name] = process
        print("Process {} [NEW] (arrival time {} ms) {} CPU bursts (tau {:.0f}ms)".format(process.getName(), process.getArrivalTime(), process.getTotalBursts(), process.getEstimatedBurstTime() ))
    print("time 0ms: Simulator started for SJF [Q <empty>]")
    while( len(process_table) > 0 ):
        next_event = event_queue.get()
        time = int(next_event[0])
        process_name = next_event[1][0]
        event_type = next_event[1][1]
        process = process_table[process_name]
        if event_type == "Arrive":
            process.arrive()
            ready_queue.append(process_name)
            print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), print_ready_queue(ready_queue) ))
            if len(ready_queue) != 0 and (current_running == None or time >= CPU_vacant_at):
                #sort the ready_queue
                ready_queue.pop(0)
                event_queue.put((time + cst, (process_name, "Run")))
                process.startContextSwitchIn(time)
                current_running = process_name
        elif event_type == "Run":
            expected = process.startRunning(time)
            event_queue.put((time + expected, (process_name, "CSOut")))
            CPU_vacant_at = time + expected + cst
            print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), expected, print_ready_queue(ready_queue) ))
        elif event_type == "CSOut":
            process.startContextSwitchOut(time)
            event_queue.put((time + cst, (process_name, "EnterIO")))
            print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), process.total_bursts-process.index-1, print_ready_queue(ready_queue) ))
            if process.index < process.total_bursts - 1:
                # recaculate_tau:
                recaculate_tau(process, process.index)
                print("time {}ms: Recalculated tau = {}ms for process {} [Q {}]".format(time, process.getEstimatedBurstTime(), process.name, print_ready_queue(ready_queue) ))
                # Sort the ready queue by estimated_brust_time
                sorted(ready_queue, key=lambda ready_queue: process.estimated_brust_time)
                # switch out
                print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, int(time + cst + process.io_times[process.index]), print_ready_queue(ready_queue) ))
            context_switch_count += 1
        elif event_type == "EnterIO":
            expected = process.finishRunning(time)
            if expected == -1:
                print("time {}ms: Process {} terminated [Q {}]".format(time, process_name, print_ready_queue(ready_queue) ))
                del process_table[process_name]
            else:
                event_queue.put((time + expected, (process_name, "EnterQueue")))
            current_running = None
            # Start running another immediately, if there is another one on the waiting queue
            if len(ready_queue) > 0:
                new_name = ready_queue.pop(0)
                new_process = process_table[new_name]
                event_queue.put((time + cst, (new_name, "Run")))
                new_process.startContextSwitchIn(time)
                current_running = new_name
        elif event_type == "EnterQueue":
            process.finishIO(time)
            ready_queue.append(process_name)
            print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]".format(time, process_name, print_ready_queue(ready_queue) ))
            if len(ready_queue) == 1 and (current_running == None or time >= CPU_vacant_at):
                ready_queue.pop(0)
                event_queue.put((time + cst, (process_name, "Run")))
                process.startContextSwitchIn(time)
                current_running = process_name
        else:
            print("ERROR: <error-text-here>")
            return
def SRT(processes):
	pass

def RR(processes):
	pass

#main part
if __name__ == '__main__':
	if len(sys.argv) < 8:
		print("ERROR: Invalid argument.")
		sys.exit(2)

	n = int(sys.argv[1])
	seed = int(sys.argv[2])
	parameter = float(sys.argv[3])
	upper_bound = float(sys.argv[4])
	t_cs = float(sys.argv[5])
	alpha = float(sys.argv[6])
	t_slice = float(sys.argv[7])
	rradd = "END"
	if sys.argv >= 9:
		rradd = sys.argv[8]

	processes = []

	#random generator
	generator = Rand48(0)
	generator.srand(seed)

	for x in range(n):
		pid = letters[x]
		while True:
			tt = generator.drand()
			temp = math.floor(-(math.log(tt)) / parameter)
			if temp > upper_bound:
				continue
			else:
				arr = temp
				break
		while True:
			num_burst = math.floor(generator.drand()*100)+1
			if num_burst > upper_bound:
				continue
			else:
				break
		burst = []
		io = []
		for y in range(num_burst-1):
			a = checkUpperBound(upper_bound)
			b = checkUpperBound(upper_bound)
			burst.append(a)
			io.append(b)
		c = checkUpperBound(upper_bound)
		burst.append(c)
		process = Process(pid,arr,burst,io)
		processes.append(process)
processes1 = deepcopy(processes)
#FCFS(processes1, t_cs/2)
processes2 = deepcopy(processes)
processes3 = deepcopy(processes)
processes4 = deepcopy(processes)
print()
SJF(processes2, t_cs/2)
