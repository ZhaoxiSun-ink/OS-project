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
        if process.getTotalBursts() == 1:
            print("Process {} [NEW] (arrival time {} ms) {} CPU burst".format(process.getName(), process.getArrivalTime(), process.getTotalBursts()))
        else:
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
            #if time <= 1000:
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
            #if time <= 1000:
            print("time {}ms: Process {} started using the CPU for {}ms burst [Q {}]".format(time, process_name, expected, printwq(waiting_queue)))
        elif event_type == "CSOut":
            process.startContextSwitchOut(time)
            event_queue.put((time + cst, 1, process_name, "EnterIO"))
            remaining_bursts = process.total_bursts-process.index-1
            if remaining_bursts > 1: #and time <= 1000:
                print("time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, remaining_bursts, printwq(waiting_queue)))
            elif remaining_bursts == 1: #and time <= 1000:
                print("time {}ms: Process {} completed a CPU burst; 1 burst to go [Q {}]".format(time, process_name, printwq(waiting_queue)))
            elif remaining_bursts == 0:
                print("time {}ms: Process {} terminated [Q {}]".format(time, process_name, printwq(waiting_queue)))
            if process.index < process.total_bursts - 1: #and time <= 1000:
                print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, int(time + cst + process.io_times[process.index]), printwq(waiting_queue)))
            context_switch_count += 1
            process.context_switch += 1
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
            #if time <= 1000:
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
            if remaining_bursts > 1: #and time <= 1000:
                print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), process.total_bursts-process.index-1, print_ready(ready_state) ))
            elif remaining_bursts == 1: #and time <= 1000:
                print("time {}ms: Process {} (tau {}ms) completed a CPU burst; 1 burst to go [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), print_ready(ready_state) ))
            elif remaining_bursts == 0 and time:
                print("time {}ms: Process {} terminated [Q {}]".format(time, process_name, print_ready(ready_state) ))
            if remaining_bursts != 0: #and time <= 1000:
                # recaculate_tau:
                recaculate_tau(process, process.index)
                print("time {}ms: Recalculated tau = {}ms for process {} [Q {}]".format(time, process.getEstimatedBurstTime(), process.name, print_ready(ready_state) ))
                # Sort the ready state by estimated_burst_time
                ready_state.sort(key=operator.attrgetter('estimated_burst_time', 'name'))
            if process.index < process.total_bursts - 1: #and time <= 1000:
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
                event_queue.put((time + cst, 2, new_name, "Run"))
                ready_state.sort(key=operator.attrgetter('estimated_burst_time', 'name'))
                new_process.startContextSwitchIn(time) #problem here
                current_running = new_name
        elif order_num == 3:
            process.finishIO(time)
            ready_state.append(process)
            # Sort the ready state by estimated_burst_time
            ready_state.sort(key=operator.attrgetter('estimated_burst_time', 'name'))
            # if time <= 1000:
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
    ignore_list = []
    #put all processes into event_queue
    for process in processes:
        arrival_time = process.getArrivalTime()
        name = process.getName()
        event_queue.put((arrival_time, 4, name, "Arrive"))
        process_table[name] = process
        print("Process {} [NEW] (arrival time {} ms) {} CPU bursts (tau {:.0f}ms)".format(process.getName(), process.getArrivalTime(), process.getTotalBursts(), process.getEstimatedBurstTime() ))
    print("time 0ms: Simulator started for SRT [Q <empty>]")

    while(len(process_table) > 0):
        # print("Length: ", event_queue.qsize(), " Time of prev: ", time)
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
            #if time <= 1000:
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
                if candidate.getEstimatedBurstTime()-candidate.alreadyRunTime(time) < current_running.getEstimatedBurstTime()-current_running.alreadyRunTime(time):
                    # if current running is running, just preempt
                    if current_running.getStatus() == "Running":
                        current_running.startContextSwitchOut(time)
                        ignore_list.append(current_running)
                        if(current_running.remaining_burst_times[current_running.index] > 0):
                            event_queue.put((time + cst, 1, current_running.getName(), "EnterQueue"))
                            #if time <= 1000:
                            print("0Process will preempt current running process.")
                        else:
                            event_queue.put((time + cst, 1, current_running.getName(), "EnterIO"))
                            #if time <= 1000:
                            print("0Process will preempt current running process, IO")
                        
                    # if current running is still switching in, do nothing
                    # if current running is switching out, do nothing
        #run
        elif event_type == "Run":
            # If best candidate can preempt current process to be run, do it
            if len(ready_queue) == 0:
                expected = process.startRunning(time)
                event_queue.put((time + expected, 0, process_name, "CSOut"))
                #if time <= 1000:
                print("time {}ms: Process {} (tau {}ms) started using the CPU with {}ms burst remaining [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), expected, print_ready_queue(ready_queue) ))
                continue
            candidate =  ready_queue[0]
            candidate_name = candidate.getName()
            #print("candidate here is ", candidate.getName())
            #print(candidate.getEstimatedBurstTime() , process.getEstimatedBurstTime())
            if candidate.getEstimatedBurstTime()-candidate.alreadyRunTime(time) < process.getEstimatedBurstTime()-process.alreadyRunTime(time):
                #if time <= 1000:
                print("time {}ms: Process {} (tau {}ms) started using the CPU with {}ms burst remaining [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), expected, print_ready_queue(ready_queue) ))
                process.startRunning(time)
                process.startContextSwitchOut(time)
                event_queue.put((time + cst, 1, process_name, "EnterQueue"))
                #if time <= 1000:
                print("time {}ms: Process {} (tau {}ms) will preempt {} [Q {}]".format(time, candidate.name, candidate.getEstimatedBurstTime(), process.name, print_ready_queue(ready_queue)))
            else:
                expected = process.startRunning(time)
                event_queue.put((time + expected, 0, process_name, "CSOut"))
                #if time <= 1000:
                print("time {}ms: Process {} (tau {}ms) started using the CPU with {}ms burst remaining [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), expected, print_ready_queue(ready_queue) ))

        elif event_type == "CSOut":
            if process in ignore_list:
                ignore_list.pop(ignore_list.index(process))
                continue
            # print(process.name, process.status)
            process.startContextSwitchOut(time)
            # print("Remainning", process.remaining_burst_times[process.index])
            if process.remaining_burst_times[process.index] == 0:
                event_queue.put((time + cst, 1, process_name, "EnterIO"))
            else:
                event_queue.put((time + cst, 3, process_name, "EnterQueue"))
            if process.total_bursts-process.index-1 > 0:
                CPU_vacant_at = time + cst
                if process.total_bursts-process.index-1 == 1:
                    #if time <= 1000:
                    print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} burst to go [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), process.total_bursts-process.index-1, print_ready_queue(ready_queue) ))
                else:
                    #if time <= 1000:
                    print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), process.total_bursts-process.index-1, print_ready_queue(ready_queue) ))
                if process.index < process.total_bursts -1:
                    recalculate_tau(process,process.index) #recaculate_tau
                    #if time <= 1000:
                    print("time {}ms: Recalculated tau = {}ms for process {} [Q {}]".format(time, process.getEstimatedBurstTime(), process.name, print_ready_queue(ready_queue) ))
                    # Sort the ready queue by estimated_burst_time
                    ready_queue.sort(key=operator.attrgetter('estimated_remaining_burst_time', 'name'))
                    # switch out
                    #if time <= 1000:
                    print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, int(time + cst + process.io_times[process.index]), print_ready_queue(ready_queue) ))
                context_switch_count += 1
                process.context_switch += 1

        elif event_type == "EnterIO":
            ready_queue.sort(key=operator.attrgetter('estimated_remaining_burst_time', 'name'))
            # print("Remaining time", process_name, process.remaining_burst_times[process.index])
            expected = process.finishRunning(time)
            if expected == -1:
                print("time {}ms: Process {} terminated [Q {}]".format(int(time-cst), process_name, print_ready_queue(ready_queue) ))
                del process_table[process_name]
            else:
                event_queue.put((time+expected, 3, process_name, "EnterQueue"))
            current_running = None
            # immediately add something to the CPU
            if len(ready_queue) > 0:
                new_name = ready_queue.pop(0).getName()
                new_process = process_table[new_name]
                event_queue.put((time+cst, 2, new_name, "Run"))
                # print(time, new_process.name, new_process.status)
                new_process.startContextSwitchIn(time)
                current_running = new_process

        elif event_type == "EnterQueue":
            ready_queue.append(process_table[process_name])
            ready_queue.sort(key=operator.attrgetter('estimated_remaining_burst_time', 'name'))
            if process.getStatus() == "IO":
                process.finishIO(time)
                #if time <= 1000:
                print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue [Q {}]".format(time, process_name,process.getEstimatedBurstTime(), print_ready_queue(ready_queue) ))
                
            if process.getStatus() == "Context_Switch_Out":
                process.preempt(time)
                current_running = None

            # Fastest process in the queue
            candidate = ready_queue[0]
            # print("Candidate is ", candidate.name)
            # Nothing running now, just start
            #print(current_running)
            if current_running == None:
                ready_queue.pop(0)
                event_queue.put((time + cst, 2, candidate.getName(), "Run"))
                candidate.startContextSwitchIn(time)
                current_running = candidate
            else:
                # print(candidate.getEstimatedBurstTime(),candidate.alreadyRunTime(time) , current_running.getEstimatedBurstTime(),current_running.alreadyRunTime(time))
                if candidate.getEstimatedBurstTime()-candidate.alreadyRunTime(time) < current_running.getEstimatedBurstTime()-current_running.alreadyRunTime(time):
                    # print("Evil begins here", candidate.getEstimatedRemaining() , current_running.getEstimatedRemaining())
                    # if current running is running, just preempt
                    if current_running.getStatus() == "Running":
                        current_running.startContextSwitchOut(time)
                        ignore_list.append(current_running)
                        if(current_running.remaining_burst_times[current_running.index] > 0):
                            event_queue.put((time + cst, 1, current_running.getName(), "EnterQueue"))
                            #print("time {}ms: Process {} (tau {}ms) will preempt {} [Q {}]".format(time, process_name, process.getEstimatedRemaining(), current_running.getName(), print_ready_queue(ready_queue)))
                        else:
                            event_queue.put((time + cst, 1, current_running.getName(), "EnterIO"))
                            #if time <= 1000:
                            print("Process will preempt current running process, IO")
                        
                    # if current running is still switching in, do nothing
                    # if current running is switching out, do nothing
        else:
            print("ERROR: <error-text-here>")
            return
    print("time {}ms: Simulator ended for SRT [Q <empty>]".format(time))


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
        event_queue.put((arrival_time, 4, (name, "Arrive", 0)))
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
            if next_event[2][2] == 1:
                process.startContextSwitchIn(time)
                current_running = process_name
            expected = process.startRunning(time)
            actual = expected
            '''
            if time < 1000:#time < 39000 and time > 37000:
                a = len(waiting_queue) > 0
                print("ex: {}; t_s: {}; {}".format(expected, t_slice, len(waiting_queue)))
            '''
            if expected > t_slice:
                # preemption occurs
                actual = t_slice
                preemption = 1
                event_queue.put((time + actual, 0, (process_name, "CSOut", 1)))
            else:
                event_queue.put((time + actual, 0, (process_name, "CSOut", 0)))
            CPU_vacant_at = time + actual + cst
            #if time <= 1000:#time < 39000 and time > 37000:
            print("time {}ms: Process {} started using the CPU for {}ms burst [Q {}]".format(time, process_name, expected, printwq(waiting_queue)))
        elif event_type == "CSOut":
            process.startContextSwitchOut(time)
            # if preemption occurs
            if next_event[2][2] == 1:
                event_queue.put((time + cst, 1, (process_name, "EnterIO", 1)))
                #if time <= 1000:#time < 39000 and time > 37000:
                print("time {}ms: Time slice expired; process {} preempted with {}ms to go [Q {}]".format(time, process_name, process.remaining_burst_times[process.index], printwq(waiting_queue)))
            else:
                event_queue.put((time + cst, 1, (process_name, "EnterIO", 0)))
                remaining_bursts = process.total_bursts-process.index-1
                if remaining_bursts > 1: #and time <= 1000:
                    print("time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, remaining_bursts, printwq(waiting_queue)))
                elif remaining_bursts == 1: #and time <= 1000:
                    print("time {}ms: Process {} completed a CPU burst; 1 burst to go [Q {}]".format(time, process_name, printwq(waiting_queue)))
                elif remaining_bursts == 0:
                    print("time {}ms: Process {} terminated [Q {}]".format(time, process_name, printwq(waiting_queue)))
                if process.index < process.total_bursts - 1: #and time <= 1000:
                    print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, int(time + cst + process.io_times[process.index]), printwq(waiting_queue)))
            context_switch_count += 1
            process.context_switch += 1
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
                    event_queue.put((time + expected, 3, (process_name, "EnterQueue", 0)))
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
            #if time <= 1000:#time < 39000 and time > 37000:
            print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]".format(time, process_name, printwq(waiting_queue)))
            if len(waiting_queue) == 1 and current_running == None and time >= CPU_vacant_at:
                waiting_queue.pop(0)
                event_queue.put((time + cst, 2, (process_name, "Run", 0)))
                process.startContextSwitchIn(time)
                current_running = process_name
        else:
            print("ERROR: <error-text-here>")
            return
    print("time {}ms: Simulator ended for RR [Q <empty>]".format(time))


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
processes2 = deepcopy(processes)
processes3 = deepcopy(processes)
processes4 = deepcopy(processes)
#FCFS(processes1, t_cs/2)
print()
#SJF(processes2, t_cs/2)
print()
SRT(processes3,t_cs/2)
print()
#RR(processes4,t_cs/2,t_slice,rradd)
"""
FCFS_burst = 0
FCFS_total_burst = 0
FCFS_waiting = 0
FCFS_waiting_num = 0
FCFS_around = 0
FCFS_around_num = 0
FCFS_total_context_switch = 0
# SJF
SJF_burst = 0
SJF_total_burst = 0
SJF_waiting = 0
SJF_waiting_num = 0
SJF_around = 0
SJF_around_num = 0
SJF_total_context_switch = 0
# SRT
SRT_burst = 0
SRT_total_burst = 0
SRT_waiting = 0
SRT_waiting_num = 0
SRT_around = 0
SRT_around_num = 0
SRT_total_context_switch = 0
SRT_total_preemption = 0
# RR
RR_burst = 0
RR_total_burst = 0
RR_waiting = 0
RR_waiting_num = 0
RR_around = 0
RR_around_num = 0
RR_total_context_switch = 0
RR_total_preemption = 0
# For each process, sum the total
for i in range(len(processes)):
    # FCSF
    FCFS_burst += processes1[i].getTotalBurstTime()
    FCFS_total_burst += processes1[i].getTotalBursts()
    FCFS_waiting += processes1[i].getTotalWaitingTime()
    FCFS_waiting_num += processes1[i].getWaitingTimeNum()
    FCFS_around += processes1[i].getTotalTurnaroundTime()
    FCFS_around_num += processes1[i].getTurnAroundTimeNum()
    FCFS_total_context_switch += processes1[i].context_switch
    # SJF
    SJF_burst += processes2[i].getTotalBurstTime()
    SJF_total_burst += processes2[i].getTotalBursts()
    SJF_waiting += processes2[i].getTotalWaitingTime()
    SJF_waiting_num += processes2[i].getWaitingTimeNum()
    SJF_around += processes2[i].getTotalTurnaroundTime()
    SJF_around_num += processes2[i].getTurnAroundTimeNum()
    SJF_total_context_switch += processes2[i].context_switch

    # SRT
    SRT_burst += processes3[i].getTotalBurstTime()
    SRT_total_burst += processes3[i].getTotalBursts()
    SRT_waiting += processes3[i].getTotalWaitingTime()
    SRT_waiting_num += processes3[i].getWaitingTimeNum()
    SRT_around += processes3[i].getTotalTurnaroundTime()
    SRT_around_num += processes3[i].getTurnAroundTimeNum()
    SRT_total_context_switch += processes3[i].context_switch
    SRT_total_preemption += processes3[i].preempt_num
    # RR
    RR_burst += processes4[i].getTotalBurstTime()
    RR_total_burst += processes4[i].getTotalBursts()
    RR_waiting += processes4[i].getTotalWaitingTime()
    RR_waiting_num += processes4[i].getWaitingTimeNum()
    RR_around += processes4[i].getTotalTurnaroundTime()
    RR_around_num += processes4[i].getTurnAroundTimeNum()
    RR_total_context_switch += processes4[i].context_switch
    RR_total_preemption += processes3[i].preempt_num

# divide by total process number
FCSF_avg_burst_time  = FCFS_burst / FCFS_total_burst
FCSF_avg_waiting_time  = FCFS_waiting / FCFS_waiting_num
FCSF_avg_turn_around_time  = (FCFS_around+FCFS_waiting) / FCFS_around_num

SJF_avg_burst_time  = SJF_burst / SJF_total_burst
SJF_avg_waiting_time  = SJF_waiting / SJF_waiting_num
SJF_avg_turn_around_time  = (SJF_around+SJF_waiting) / SJF_around_num


SRT_avg_burst_time  = SRT_burst / SRT_total_burst
SRT_avg_waiting_time  = SRT_waiting / SRT_waiting_num
SRT_avg_turn_around_time  = (SRT_around+SRT_waiting) / SRT_around_num

RR_avg_burst_time  = RR_burst / RR_total_burst
RR_avg_waiting_time  = RR_waiting / RR_waiting_num
RR_avg_turn_around_time  = (RR_around+RR_waiting) / RR_around_num


original_stdout = sys.stdout # Save a reference to the original standard output
with open('simout.txt', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    #
    print("Algorithm FCFS")
    print("-- average CPU burst time: {:.3f} ms".format(FCSF_avg_burst_time) )
    print("-- average wait time: {:.3f} ms".format(FCSF_avg_waiting_time) )
    print("-- average turnaround time: {:.3f} ms".format(FCSF_avg_turn_around_time) )
    print("-- total number of context switches: {}".format(FCFS_total_context_switch) )
    print("-- total number of preemptions: 0")
    #
    print("Algorithm SJF")
    print("-- average CPU burst time: {:.3f} ms".format(SJF_avg_burst_time) )
    print("-- average wait time: {:.3f} ms".format(SJF_avg_waiting_time) )
    print("-- average turnaround time: {:.3f} ms".format(FCSF_avg_turn_around_time) )
    print("-- total number of context switches: {}".format(SJF_total_context_switch) )
    print("-- total number of preemptions: 0")
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
"""