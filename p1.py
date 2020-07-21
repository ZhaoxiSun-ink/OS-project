#Summer 2020 CSCI 4210 Operating Systems project 1
#Team Members: Zhaoxi Sun, Xinyan Sun, Tongyu Wang, Yueting Liao
import sys #get argument
import math # get log
import operator
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
<<<<<<< HEAD
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
        event_queue.put((arrival_time, 4, name, "Arrive"))
        process_table[name] = process
        print("Process {} [NEW] (arrival time {} ms) {} CPU bursts".format(process.getName(), process.getArrivalTime(), process.getTotalBursts()))
    print("time 0ms: Simulator started for FCFS [Q <empty>]")
    while(len(process_table) > 0):
        next_event = event_queue.get(block=False)
        time = int(next_event[0])
        process_name = next_event[2]
        event_type = next_event[3]
        process = process_table[process_name]
        if event_type == "Arrive":
            process.arrive()
            waiting_queue.append(process_name)
            if time <= 1000:
                print("time {}ms: Process {} arrived; added to ready queue [Q {}]".format(time, process_name, printwq(waiting_queue)))
            if len(waiting_queue) == 1 and current_running == None and time >= CPU_vacant_at:
                waiting_queue.pop(0)
                event_queue.put((time + cst, 2, process_name, "Run"))
                process.startContextSwitchIn(time)
                current_running = process_name
        elif event_type == "Run":
            expected = process.startRunning(time)
            event_queue.put((time + expected, 0, process_name, "CSOut"))
            CPU_vacant_at = time + expected + cst
            if time <= 1000:
                print("time {}ms: Process {} started using the CPU for {}ms burst [Q {}]".format(time, process_name, expected, printwq(waiting_queue)))
        elif event_type == "CSOut":
            process.startContextSwitchOut(time)
            event_queue.put((time + cst, 1, process_name, "EnterIO"))
            remaining_bursts = process.total_bursts-process.index-1
            if remaining_bursts > 1 and time <= 1000:
                print("time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, remaining_bursts, printwq(waiting_queue)))
            elif remaining_bursts == 1 and time <= 1000:
                print("time {}ms: Process {} completed a CPU burst; 1 burst to go [Q {}]".format(time, process_name, printwq(waiting_queue)))
            elif remaining_bursts == 0:
                print("time {}ms: Process {} terminated [Q {}]".format(time, process_name, printwq(waiting_queue)))
            if process.index < process.total_bursts - 1 and time <= 1000:
                print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, int(time + cst + process.io_times[process.index]), printwq(waiting_queue)))
            context_switch_count += 1
        elif event_type == "EnterIO":
            expected = process.finishRunning(time)
            if expected == -1:
                del process_table[process_name]
            else:
                event_queue.put((time + expected, 3, process_name, "EnterQueue"))
            current_running = None
            # Start running another immediately, if there is another one on the waiting queue
            if len(waiting_queue) > 0:
                new_name = waiting_queue.pop(0)
                new_process = process_table[new_name]
                event_queue.put((time + cst, 2, new_name, "Run"))
                new_process.startContextSwitchIn(time)
                current_running = new_name
        elif event_type == "EnterQueue":
            process.finishIO(time)
            waiting_queue.append(process_name)
            if time <= 1000:
                print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]".format(time, process_name, printwq(waiting_queue)))
            if len(waiting_queue) == 1 and current_running == None and time >= CPU_vacant_at:
                waiting_queue.pop(0)
                event_queue.put((time + cst, 2, process_name, "Run"))
                process.startContextSwitchIn(time)
                current_running = process_name
        else:
            print("ERROR: <error-text-here>")
            return
    print("time {}ms: Simulator ended for FCFS [Q <empty>]".format(time))
=======
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
		event_queue.put((arrival_time, 4, name, "Arrive"))
		process_table[name] = process
		print("Process {} [NEW] (arrival time {} ms) {} CPU bursts".format(process.getName(), process.getArrivalTime(), process.getTotalBursts()))
	print("time 0ms: Simulator started for FCFS [Q <empty>]")
	while(len(process_table) > 0):
		next_event = event_queue.get(block=False)
		time = int(next_event[0])
		process_name = next_event[2]
		event_type = next_event[3]
		process = process_table[process_name]
		if event_type == "Arrive":
			process.arrive()
			waiting_queue.append(process_name)
			if time <= 1000:
				print("time {}ms: Process {} arrived; added to ready queue [Q {}]".format(time, process_name, printwq(waiting_queue)))
			if len(waiting_queue) == 1 and current_running == None and time >= CPU_vacant_at:
				waiting_queue.pop(0)
				event_queue.put((time + cst, 2, process_name, "Run"))
				process.startContextSwitchIn(time)
				current_running = process_name
		elif event_type == "Run":
			expected = process.startRunning(time)
			event_queue.put((time + expected, 0, process_name, "CSOut"))
			CPU_vacant_at = time + expected + cst
			if time <= 1000:
				print("time {}ms: Process {} started using the CPU for {}ms burst [Q {}]".format(time, process_name, expected, printwq(waiting_queue)))
		elif event_type == "CSOut":
			process.startContextSwitchOut(time)
			event_queue.put((time + cst, 1, process_name, "EnterIO"))
			remaining_bursts = process.total_bursts-process.index-1
			if remaining_bursts > 1 and time <= 1000:
				print("time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, remaining_bursts, printwq(waiting_queue)))
			elif remaining_bursts == 1 and time <= 1000:
				print("time {}ms: Process {} completed a CPU burst; 1 burst to go [Q {}]".format(time, process_name, printwq(waiting_queue)))
			elif remaining_bursts == 0:
				print("time {}ms: Process {} terminated [Q {}]".format(time, process_name, printwq(waiting_queue)))
			if process.index < process.total_bursts - 1 and time <= 1000:
				print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, int(time + cst + process.io_times[process.index]), printwq(waiting_queue)))
			context_switch_count += 1
		elif event_type == "EnterIO":
			expected = process.finishRunning(time)
			if expected == -1:
				del process_table[process_name]
			else:
				event_queue.put((time + expected, 3, process_name, "EnterQueue"))
			current_running = None
			# Start running another immediately, if there is another one on the waiting queue
			if len(waiting_queue) > 0:
				new_name = waiting_queue.pop(0)
				new_process = process_table[new_name]
				event_queue.put((time + cst, 2, new_name, "Run"))
				new_process.startContextSwitchIn(time)
				current_running = new_name
		elif event_type == "EnterQueue":
			process.finishIO(time)
			waiting_queue.append(process_name)
			if time <= 1000:
				print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]".format(time, process_name, printwq(waiting_queue)))
			if len(waiting_queue) == 1 and current_running == None and time >= CPU_vacant_at:
				waiting_queue.pop(0)
				event_queue.put((time + cst, 2, process_name, "Run"))
				process.startContextSwitchIn(time)
				current_running = process_name
		else:
			print("ERROR: <error-text-here>")
			return

	print("time {}ms: Simulator ended for FCFS [Q <empty>]".format(time))
>>>>>>> e09a31da95b81a70a3e1c908ef5e510e50b8cfcc


# Shortest Job First (SJF) algorithm
# It runs the process in order of shortest ESTIMATED CPU burst times
def SJF(processes, cst):
    # convert the ready_state list to string
    def print_ready(ready_list):
        if len(ready_list) == 0:
            return "<empty>"
        ans = ready_list[0].name
        for i in range(1, len(ready_list)):
            ans = ans + " " + ready_list[i].name
        return ans
    # caculating tau (estimated_burst_time)
    def recaculate_tau(process, index):
        # tau_i+1 =  alpha x t_i   +  (1-alpha) x tau i
        tau_i = math.ceil( alpha * process.burst_times[index] + (1-alpha) * process.estimated_burst_time )
        process.estimated_burst_time = tau_i

    for process in processes:
        tau_0 = (1/parameter) # For every process, tau_0 = 1/lambda
        process.estimated_burst_time = tau_0

    #waiting_queue, sorted by arrival time
    process_table = dict()
    ready_state = list() #list of process
    event_queue = PriorityQueue()
    time = 0
    current_running = None
    CPU_vacant_at = -1
    context_switch_count = 0
    """
    Order Numbers: (handling ties)
    0 - CPU burst completion -> CS out
    1 - EnterIO -> Enter I/O
    2 - Run -> started using the CPU burst
    3 - EnterQueue -> completed I/O or terminate
    4 - Arrive -> arrived
    """
    # push all processes to event_queue
    for process in processes:
        arrival_time = process.getArrivalTime()
        name = process.getName()
        event_queue.put((arrival_time, 4, name, "Arrive"))
        process_table[name] = process
        if process.getTotalBursts() == 1:
            print("Process {} [NEW] (arrival time {} ms) {} CPU burst (tau {:.0f}ms)".format(process.getName(), process.getArrivalTime(), process.getTotalBursts(), process.getEstimatedBurstTime() ))
        else:
            print("Process {} [NEW] (arrival time {} ms) {} CPU bursts (tau {:.0f}ms)".format(process.getName(), process.getArrivalTime(), process.getTotalBursts(), process.getEstimatedBurstTime() ))
    print("time 0ms: Simulator started for SJF [Q <empty>]")
    while( len(process_table) > 0 ):
        next_event = event_queue.get()
        time = int(next_event[0])
        order_num = next_event[1]
        process_name = next_event[2]
        event_type = next_event[3]
        process = process_table[process_name]
        if order_num == 4:
            process.arrive()
            # Sort the ready state by estimated_burst_time
            ready_state.append(process)
            ready_state.sort(key=operator.attrgetter('estimated_burst_time', 'name'))
            #if time <= 1000:
            print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), print_ready(ready_state) ))
            if len(ready_state) != 0 and (current_running == None or time >= CPU_vacant_at):
                ready_state.pop(0)
                event_queue.put((time + cst, 2, process_name, "Run"))
                process.startContextSwitchIn(time)
                current_running = process_name
        elif order_num == 2:
            expected = process.startRunning(time)
            event_queue.put((time + expected, 0, process_name, "CSOut"))
            CPU_vacant_at = time + expected + cst
            #if time <= 1000:
            print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), expected, print_ready(ready_state) ))
        elif order_num == 0:
            process.startContextSwitchOut(time)
            event_queue.put((time + cst, 1, process_name, "EnterIO"))
            remaining_bursts = process.total_bursts-process.index-1
            if remaining_bursts > 1:
                print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), process.total_bursts-process.index-1, print_ready(ready_state) ))
            elif remaining_bursts == 1:
                print("time {}ms: Process {} (tau {}ms) completed a CPU burst; 1 burst to go [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), print_ready(ready_state) ))
            elif remaining_bursts == 0:
                print("time {}ms: Process {} terminated [Q {}]".format(time, process_name, print_ready(ready_state) ))
            if remaining_bursts != 0:
                # recaculate_tau:
                recaculate_tau(process, process.index)
                print("time {}ms: Recalculated tau = {}ms for process {} [Q {}]".format(time, process.getEstimatedBurstTime(), process.name, print_ready(ready_state) ))
                # Sort the ready state by estimated_burst_time
                ready_state.sort(key=operator.attrgetter('estimated_burst_time', 'name'))
            if process.index < process.total_bursts - 1:
                print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, int(time + cst + process.io_times[process.index]), print_ready(ready_state) ))
            context_switch_count += 1
            process.context_switch += 1
        elif order_num == 1:
            expected = process.finishRunning(time)
            if expected == -1:
                del process_table[process_name]
            else:
                event_queue.put((time + expected, 3, process_name, "EnterQueue"))
            current_running = None
            # Start running another immediately, if there is another one on the waiting queue
            if len(ready_state) > 0:
                new_process = ready_state.pop(0)
                new_name = new_process.name
                new_process = process_table[new_name]
                #print("Name: {} | Status: {} | Time: {}".format( new_process.name, new_process.getStatus(), time) )
                event_queue.put((time + cst, 2, new_name, "Run"))
                ready_state.sort(key=operator.attrgetter('estimated_burst_time', 'name'))
                new_process.startContextSwitchIn(time) #problem here
                current_running = new_name
        elif order_num == 3:
            process.finishIO(time)
            ready_state.append(process)
            # Sort the ready state by estimated_burst_time
            ready_state.sort(key=operator.attrgetter('estimated_burst_time', 'name'))
            #if time <= 1000:
            print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), print_ready(ready_state) ))
            if len(ready_state) == 1 and current_running == None and time >= CPU_vacant_at:
                ready_state.pop(0)
                event_queue.put((time + cst, 2, process_name, "Run"))
                process.startContextSwitchIn(time)
                current_running = process_name
        else:
            print("ERROR: <error-text-here>")
            return
    print( "time {}ms: Simulator ended for SJF [Q <empty>]".format(time) )


def SRT(processes,cst):
    def print_ready_queue(waitq):
        if len(waitq) == 0:
            return "<empty>"
        ans = waitq[0].getName()
        for i in range(1,len(waitq)):
            ans = ans + " " + waitq[i].getName()
        return ans

    def recalculate_tau(process,index):
        tau_i = math.ceil(alpha * process.burst_times[index] + (1-alpha) * process.estimated_burst_time)
        process.estimated_burst_time = tau_i

    #initalize all process
    for p in processes:
        p.estimated_burst_time = 1/parameter

    #waiting_queue, sorted by arrival time
    process_table = dict()
    ready_queue = []
    event_queue = PriorityQueue()
    time = 0
    current_running = None
    context_switch_count = 0
    #put all processes into event_queue
    for process in processes:
        arrival_time = process.getArrivalTime()
        name = process.getName()
        event_queue.put((arrival_time, 4, name, "Arrive"))
        process_table[name] = process
        print("Process {} [NEW] (arrival time {} ms) {} CPU bursts (tau {:.0f}ms)".format(process.getName(), process.getArrivalTime(), process.getTotalBursts(), process.getEstimatedBurstTime() ))
    print("time 0ms: Simulator started for SRT [Q <empty>]")

    while(len(process_table) > 0):
        print(process_table["B"].status)
        next_event = event_queue.get(block=False)
        time = int(next_event[0])
        process_name = next_event[2]
        event_type = next_event[3]
        process = process_table[process_name]
        #arrive
        if event_type == "Arrive":
            process.arrive()
            ready_queue.append(process_table[process_name])
            ready_queue.sort(key=operator.attrgetter('estimated_remaining_burst_time', 'name'))
            print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), print_ready_queue(ready_queue) ))
            # Fastest process in the queue
            candidate = ready_queue[0]
            # Nothing running now, just start
            if len(ready_queue) == 1 and (current_running == None):
                ready_queue.pop(0)
                event_queue.put((time + cst, 2, process_name, "Run"))
                process.startContextSwitchIn(time)
                current_running = process
            else:
                if candidate.getEstimatedRemaining() < current_running.getEstimatedRemaining():
                    # if current running is running, just preempt
                    if current_running.getStatus() == "Running":
                        current_running.startContextSwitchOut(time)
                        ignore_list.append(current_running)
                        if(current_running.remaining_burst_times[current_running.index] > 0):
                            event_queue.put((time + cst, 1, current_running.getName(), "EnterQueue"))
                            print("0Process will preempt current running process.")
                        else:
                            event_queue.put((time + cst, 1, current_running.getName(), "EnterIO"))
                            print("0Process will preempt current running process, IO")
                        
                    # if current running is still switching in, do nothing
                    # if current running is switching out, do nothing
        #run
        elif event_type == "Run":
<<<<<<< HEAD
            # If best candidate can preempt current process to be run, do it
            if len(ready_queue) == 0:
                expected = process.startRunning(time)
                event_queue.put((time + expected, 0, process_name, "CSOut"))
                print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), expected, print_ready_queue(ready_queue) ))
                continue
            candidate_name = ready_queue[0]
            candidate = process_table[candidate_name]
            if candidate.getEstimatedRemaining() < process.getEstimatedRemaining():
                process.startContextSwitchOut(time)
                event_queue.push((time + cst, 1, process, "EnterQueue"))
                print("Best candidate will preempt current running process")
            else:
                expected = process.startRunning(time)
                event_queue.put((time + expected, 0, process_name, "CSOut"))
                print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), expected, print_ready_queue(ready_queue) ))

        elif event_type == "CSOut":
            if process in ignore_list:
                ignore_list.pop(ignore_list.index(process))
                continue
            print(process.name, process.status)
=======
            print(time)
            print(process.getStatus())
            expected = process.startRunning(time)
            event_queue.put((time + expected, (process_name, "CSOut")))
            CPU_vacant_at = time + expected + cst
            print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), expected, print_ready_queue(ready_queue) ))

        elif event_type == "CSOut":
>>>>>>> e09a31da95b81a70a3e1c908ef5e510e50b8cfcc
            process.startContextSwitchOut(time)
            print("Remainning", process.remaining_burst_times[process.index])
            if process.remaining_burst_times[process.index] == 0:
                event_queue.put((time + cst, 1, process_name, "EnterIO"))
            else:
                event_queue.put((time + cst, 3, process_name, "EnterQueue"))
            if process.total_bursts-process.index-1 > 0:
                CPU_vacant_at = time + cst
                if process.total_bursts-process.index-1 == 1:
                    print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} burst to go [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), process.total_bursts-process.index-1, print_ready_queue(ready_queue) ))
                else:
                    print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), process.total_bursts-process.index-1, print_ready_queue(ready_queue) ))
                if process.index < process.total_bursts -1:
                    recalculate_tau(process,process.index) #recaculate_tau
                    print("time {}ms: Recalculated tau = {}ms for process {} [Q {}]".format(time, process.getEstimatedBurstTime(), process.name, print_ready_queue(ready_queue) ))
                    # Sort the ready queue by estimated_burst_time
                    ready_queue.sort(key=operator.attrgetter('estimated_remaining_burst_time', 'name'))
                    # switch out
                    print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, int(time + cst + process.io_times[process.index]), print_ready_queue(ready_queue) ))
                context_switch_count += 1

        elif event_type == "EnterIO":
            print("Remaining time", process_name, process.remaining_burst_times[process.index])
            expected = process.finishRunning(time)
            if expected == -1:
                print("time {}ms: Process {} terminated [Q {}]".format(time, process_name, print_ready_queue(ready_queue) ))
                del process_table[process_name]
            else:
                event_queue.put((time+expected, 3, process_name, "EnterQueue"))
            current_running = None
            # immediately add something to the CPU
            if len(ready_queue) > 0:
                new_name = ready_queue.pop(0).getName()
                new_process = process_table[new_name]
                event_queue.put((time+cst, 2, new_name, "Run"))
                new_process.startContextSwitchIn(time)
                current_running = new_process

        elif event_type == "EnterQueue":
            if process.getStatus() == "IO":
                process.finishIO(time)
                print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]".format(time, process_name, print_ready_queue(ready_queue) ))
            if process.getStatus() == "Context_Switch_Out":
                process.preempt(time)
            ready_queue.append(process_table[process_name])
            ready_queue.sort(key=operator.attrgetter('estimated_remaining_burst_time', 'name'))
<<<<<<< HEAD
            
            # Fastest process in the queue
            candidate = ready_queue[0]
            # Nothing running now, just start
            if len(ready_queue) == 1 and (current_running == None):
                new_process = ready_queue.pop(0)
                event_queue.put((time + cst, 2, new_process.getName(), "Run"))
                new_process.startContextSwitchIn(time)
                current_running = new_process
            else:
                if candidate.getEstimatedRemaining() < current_running.getEstimatedRemaining():
                    # if current running is running, just preempt
                    if current_running.getStatus() == "Running":
                        current_running.startContextSwitchOut(time)
                        ignore_list.append(current_running)
                        if(current_running.remaining_burst_times[current_running.index] > 0):
                            event_queue.put((time + cst, 1, current_running.getName(), "EnterQueue"))
                            print("time {}ms: Process {} (tau {}ms) will preempt {} [Q {}]".format(time, process_name, process.getEstimatedRemaining(), current_running.getName(), print_ready_queue(ready_queue)))
                        else:
                            event_queue.put((time + cst, 1, current_running.getName(), "EnterIO"))
                            print("Process will preempt current running process, IO")
                        
                    # if current running is still switching in, do nothing
                    # if current running is switching out, do nothing
=======
            print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]".format(time, process_name, print_ready_queue(ready_queue) ))
            if current_running != None:
                print(current_running.getEstimatedRemaining())
            print(process.getEstimatedRemaining())
            if len(ready_queue) == 1 and current_running == None and time >= CPU_vacant_at:
                ready_queue.pop(0)
                event_queue.put((time + cst, (process_name, "Run")))
                process.startContextSwitchIn(time)
                current_running = process
            if len(ready_queue) == 1 and current_running != None and current_running.getEstimatedRemaining() > process.getEstimatedRemaining():
                print("preemption")
                ready_queue.pop(0)
                event_queue.put((time + cst, (process_name, "Run")))
                process.startContextSwitchIn(time)
                preemption_process = current_running
                current_running = process
                event_queue.put((time+cst,(preemption_process.getName(),"EnterQueue")))
>>>>>>> e09a31da95b81a70a3e1c908ef5e510e50b8cfcc
        else:
            print("ERROR: <error-text-here>")
            return


<<<<<<< HEAD
def RR(processes):
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
    print("time 0ms: Simulator started for RR [Q <empty>]")
    while(len(process_table) > 0):
        next_event = event_queue.get(block=False)
        time = int(next_event[0])
        process_name = next_event[1][0]
        event_type = next_event[1][1]
        process = process_table[process_name]
        if event_type == "Arrive":
            process.arrive()
            waiting_queue.append(process_name)
            if time <= 1000:
                print("time {}ms: Process {} arrived; added to ready queue [Q {}]".format(time, process_name, printwq(waiting_queue)))
            if len(waiting_queue) == 1 and current_running == None and time >= CPU_vacant_at:
                waiting_queue.pop(0)
                event_queue.put((time + cst, (process_name, "Run", 0)))
                process.startContextSwitchIn(time)
                current_running = process_name
        elif event_type == "Run":
            if next_event[1][2] == 1:
                process.startContextSwitchIn(time)
                current_running = process_name
            expected = process.startRunning(time)
            actual = expected
            if expected > t_slice and len(waiting_queue) > 0:
                # preemption occurs
                actual = t_slice
                preemption = 1
                event_queue.put((time + actual, (process_name, "CSOut", 1)))
            else:
                event_queue.put((time + actual, (process_name, "CSOut", 0)))
            CPU_vacant_at = time + actual + cst
            if time <= 1000:
                print("time {}ms: Process {} started using the CPU for {}ms burst [Q {}]".format(time, process_name, expected, printwq(waiting_queue)))
        elif event_type == "CSOut":
            process.startContextSwitchOut(time)
            # if preemption occurs
            if next_event[1][2] == 1:
                event_queue.put((time + cst, (process_name, "EnterIO", 1)))
                if time <= 1000:
                    print("time {}ms: Time slice expired; process {} preempted with {} to go [Q {}]".format(time, process_name, process.remaining_burst_times[process.index], printwq(waiting_queue)))
            else:
                event_queue.put((time + cst, (process_name, "EnterIO", 0)))
                if time <= 1000:
                    print("time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, process.total_bursts-process.index-1, printwq(waiting_queue)))
                if process.index < process.total_bursts - 1:
                    if time <= 1000:
                        print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, int(time + cst + process.io_times[process.index]), printwq(waiting_queue)))
            context_switch_count += 1
        elif event_type == "EnterIO":
            if next_event[1][2] == 1:
                process.preempt(time)
                if rradd == "END":
                    waiting_queue.append(process_name)
                else:
                    waiting_queue.insert(0, process_name)
            else:
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
                event_queue.put((time + cst, (new_name, "Run", 0)))
                new_process.startContextSwitchIn(time)
                current_running = new_name
        elif event_type == "EnterQueue":
            process.finishIO(time)
            waiting_queue.append(process_name)
            if time <= 1000:
                print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]".format(time, process_name, printwq(waiting_queue)))
            if len(waiting_queue) == 1 and current_running == None and time >= CPU_vacant_at:
                waiting_queue.pop(0)
                event_queue.put((time + cst, (process_name, "Run", 0)))
                process.startContextSwitchIn(time)
                current_running = process_name
        else:
            print("ERROR: <error-text-here>")
            return
=======
def RR(processes, cst, t_slice, rradd):
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
		event_queue.put((arrival_time, 4, (name, "Arrive")))
		process_table[name] = process
		print("Process {} [NEW] (arrival time {} ms) {} CPU bursts".format(process.getName(), process.getArrivalTime(), process.getTotalBursts()))
	print("time 0ms: Simulator started for RR [Q <empty>]")
	while(len(process_table) > 0):
		next_event = event_queue.get(block=False)
		time = int(next_event[0])
		process_name = next_event[2][0]
		event_type = next_event[2][1]
		process = process_table[process_name]
		if event_type == "Arrive":
			process.arrive()
			waiting_queue.append(process_name)
			print("time {}ms: Process {} arrived; added to ready queue [Q {}]".format(time, process_name, printwq(waiting_queue)))
			if len(waiting_queue) == 1 and current_running == None and time >= CPU_vacant_at:
				waiting_queue.pop(0)
				event_queue.put((time + cst, 2, (process_name, "Run", 0)))
				process.startContextSwitchIn(time)
				current_running = process_name
		elif event_type == "Run":
			expected = process.startRunning(time)
			actual = expected
			if expected > t_slice:
				actual = t_slice
				event_queue.put((time + actual, 0, (process_name, "CSOut", 1)))
			else:
				event_queue.put((time + actual, 0, (process_name, "CSOut", 0)))
			CPU_vacant_at = time + actual + cst
			if True: #time <= 1000:
				print("time {}ms: Process {} started using the CPU for {}ms burst [Q {}]".format(time, process_name, expected, printwq(waiting_queue)))				
		elif event_type == "CSOut":
			# if preemption occurs
			if next_event[2][2] == 1:
				if len(waiting_queue) > 0:
					process.startContextSwitchOut(time)
					#print("{}  0".format(process.cpu_start_timestamp))
					#print("{}  0".format(process.cpu_end_timestamp))					
					#print("{}  1".format(process.remaining_burst_times[process.index]))
					event_queue.put((time + cst, 1, (process_name, "EnterIO", 1)))
					if True: #time <= 1000:
						print("time {}ms: Time slice expired; process {} preempted with {}ms to go [Q {}]".format(time, process_name, process.remaining_burst_times[process.index], printwq(waiting_queue)))
				else:
					t = process.remaining_burst_times[process.index]
					#print("{}  2".format(t))
					if t > t_slice:
						t = t_slice
					#print("{}  3".format(t))
					process.status = "Running"
					if True: #time <= 1000:
						print("time {}ms: Time slice expirt; no preemption because ready queue is empty [Q {}]".format(time, printwq(waiting_queue)))
					#process.remaining_burst_times[process.index] -= t
					#process.cpu_start_timestamp += t
					#print("{}  4".format(process.remaining_burst_times[process.index]))
					if process.remaining_burst_times[process.index] == 0:
						event_queue.put((time + t, 0, (process_name, "EnterIO", 0)))
						process.status = "Context_Switch_Out"
					else:
						event_queue.put((time + t, 0, (process_name, "CSOut", 1)))
			else:
				process.startContextSwitchOut(time)
				event_queue.put((time + cst, 1, (process_name, "EnterIO", 0)))
				remaining_bursts = process.total_bursts-process.index-1
				if True: #remaining_bursts > 1 and time <= 1000:
					print("time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, remaining_bursts, printwq(waiting_queue)))
				elif True: #remaining_bursts == 1 and time <= 1000:
					print("time {}ms: Process {} completed a CPU burst; 1 burst to go [Q {}]".format(time, process_name, printwq(waiting_queue)))
				elif remaining_bursts == 0:
					print("time {}ms: Process {} terminated [Q {}]".format(time, process_name, printwq(waiting_queue)))
				if process.index < process.total_bursts - 1 and time <= 1000:
					print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, int(time + cst + process.io_times[process.index]), printwq(waiting_queue)))
				context_switch_count += 1
		elif event_type == "EnterIO":
			if next_event[2][2] == 1:
				process.preempt(time)
				if rradd == "END":
					waiting_queue.append(process_name)
				else:
					waiting_queue.insert(0, process_name)
			else:
				expected = process.finishRunning(time)
				if expected == -1:
					del process_table[process_name]
				else:
					event_queue.put((time + expected, 3, (process_name, "EnterQueue")))
			current_running = None
			# Start running another immediately, if there is another one on the waiting queue
			if len(waiting_queue) > 0:
				new_name = waiting_queue.pop(0)
				new_process = process_table[new_name]
				event_queue.put((time + cst, 2, (new_name, "Run", 0)))
				new_process.startContextSwitchIn(time)
				current_running = new_name
		elif event_type == "EnterQueue":
			process.finishIO(time)
			waiting_queue.append(process_name)
			if True: #time <= 1000:
				print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]".format(time, process_name, printwq(waiting_queue)))
			if len(waiting_queue) == 1 and current_running == None and time >= CPU_vacant_at:
				waiting_queue.pop(0)
				event_queue.put((time + cst, 2, (process_name, "Run", 0)))
				process.startContextSwitchIn(time)
				current_running = process_name
		else:
			print("ERROR: <error-text-here>")
			return
	print("time {}ms: Simulator ended for FCFS [Q <empty>]".format(time))
>>>>>>> e09a31da95b81a70a3e1c908ef5e510e50b8cfcc

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
    if len(sys.argv) >= 9:
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
FCFS(processes1, t_cs/2)
processes2 = deepcopy(processes)
processes3 = deepcopy(processes)
processes4 = deepcopy(processes)
<<<<<<< HEAD
print()
# SJF(processes2, t_cs/2)
SRT(processes3, t_cs/2)
=======

SJF(processes2, t_cs/2)
#SRT(processes3,t_cs/2)
# FCSF
FCSF_avg_burst_time = 0
FCSF_avg_waiting_time = 0
FCSF_avg_turn_around_time = 0
FCSF_total_context_switch = 0
FCSF_total_preemption = 0
# SJF
SJF_avg_burst_time = 0
SJF_avg_waiting_time = 0
SJF_avg_turn_around_time = 0
SJF_total_context_switch = 0
SJF_total_preemption = 0
# SRT
SRT_avg_burst_time = 0
SRT_avg_waiting_time = 0
SRT_avg_turn_around_time = 0
SRT_total_context_switch = 0
SRT_total_preemption = 0
# RR
RR_avg_burst_time = 0
RR_avg_waiting_time = 0
RR_avg_turn_around_time = 0
RR_total_context_switch = 0
RR_total_preemption = 0
# For each process, sum the total
for i in range(len(processes)):
    # FCSF
    FCSF_avg_burst_time += ( processes1[i].getTotalBurstTime() / processes1[i].getTotalBursts() )
    FCSF_avg_waiting_time += ( processes1[i].getTotalWaitingTime() / processes1[i].getWaitingTimeNum() )
    FCSF_avg_turn_around_time += ( processes1[i].getTotalTurnaroundTime() / processes1[i].getTurnAroundTimeNum() )
    FCSF_total_context_switch += processes1[i].context_switch
    # SJF
    SJF_avg_burst_time += ( processes2[i].getTotalBurstTime() / processes2[i].getTotalBursts() )
    SJF_avg_waiting_time += ( processes2[i].getTotalWaitingTime() / processes2[i].getWaitingTimeNum() )
    SJF_avg_turn_around_time += ( processes2[i].getTotalTurnaroundTime() / processes2[i].getTurnAroundTimeNum() )
    SJF_total_context_switch += processes2[i].context_switch
    """
    # SRT
    SRT_avg_burst_time += ( processes3[i].getTotalBurstTime() / processes3[i].getTotalBursts() )
    SRT_avg_waiting_time += ( processes3[i].getTotalWaitingTime() / processes3[i].getWaitingTimeNum() )
    SRT_avg_turn_around_time += ( processes3[i].getTotalTurnaroundTime() / processes3[i].getTurnAroundTimeNum() )
    SRT_total_context_switch += processes3[i].context_switch
    SRT_total_preemption += processes3[i].preempt_num
    # RR
    RR_avg_burst_time += ( processes4[i].getTotalBurstTime() / processes4[i].getTotalBursts() )
    RR_avg_waiting_time += ( processes4[i].getTotalWaitingTime() / processes4[i].getWaitingTimeNum() )
    RR_avg_turn_around_time += ( processes4[i].getTotalTurnaroundTime() / processes4[i].getTurnAroundTimeNum() )
    RR_total_context_switch += processes4[i].context_switch
    RR_total_preemption += processes4[i].preempt_num
    """
# divide by total process number
FCSF_avg_burst_time /= len(processes)
FCSF_avg_waiting_time /= len(processes)
FCSF_avg_turn_around_time /= len(processes)

SJF_avg_burst_time /= len(processes)
SJF_avg_waiting_time /= len(processes)
SJF_avg_turn_around_time /= len(processes)

SJF_avg_burst_time /= len(processes)
SJF_avg_waiting_time /= len(processes)
SJF_avg_turn_around_time /= len(processes)

SJF_avg_burst_time /= len(processes)
SJF_avg_waiting_time /= len(processes)
SJF_avg_turn_around_time /= len(processes)

original_stdout = sys.stdout # Save a reference to the original standard output
with open('simout.txt', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    #
    print("Algorithm FCFS")
    print("-- average CPU burst time: {:.3f} ms".format(FCSF_avg_burst_time) )
    print("-- average wait time: {:.3f} ms".format(FCSF_avg_waiting_time) )
    print("-- average turnaround time: {:.3f} ms".format(FCSF_avg_turn_around_time) )
    print("-- total number of context switches: {}".format(FCSF_total_context_switch) )
    print("-- total number of preemptions: {}".format(FCSF_total_preemption) )
    #
    print("Algorithm SJF")
    print("-- average CPU burst time: {:.3f} ms".format(SJF_avg_burst_time) )
    print("-- average wait time: {:.3f} ms".format(SJF_avg_waiting_time) )
    print("-- average turnaround time: {:.3f} ms".format(FCSF_avg_turn_around_time) )
    print("-- total number of context switches: {}".format(SJF_total_context_switch) )
    print("-- total number of preemptions: {}".format(SJF_total_preemption) )
    #
    print("Algorithm SRT")
    print("-- average CPU burst time: {:.3f} ms".format(SRT_avg_burst_time) )
    print("-- average wait time: {:.3f} ms".format(SRT_avg_waiting_time) )
    print("-- average turnaround time: {:.3f} ms".format(SRT_avg_turn_around_time) )
    print("-- total number of context switches: {}".format(SRT_total_context_switch) )
    print("-- total number of preemptions: {}".format(SRT_total_preemption) )
    #
    print("Algorithm RR")
    print("-- average CPU burst time: {:.3f} ms".format(RR_avg_burst_time) )
    print("-- average wait time: {:.3f} ms".format(RR_avg_waiting_time) )
    print("-- average turnaround time: {:.3f} ms".format(RR_avg_turn_around_time) )
    print("-- total number of context switches: {}".format(RR_total_context_switch) )
    print("-- total number of preemptions: {}".format(RR_total_preemption) )
    sys.stdout = original_stdout # Reset the standard output to its original value
>>>>>>> e09a31da95b81a70a3e1c908ef5e510e50b8cfcc
