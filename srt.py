def SRT(processes,cst):

	def print_ready_queue(waitq):
		if(waitq) == 0:
			return "<empty>"
		ans = waitq[0]
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
    CPU_vacant_at = -1
    context_switch_count = 0
    # push all processes to event_queue
    for process in processes:
        arrival_time = process.getArrivalTime()
        name = process.getName()
        event_queue.put((arrival_time, (name, "Arrive")))
        process_table[name] = process
        print("Process {} [NEW] (arrival time {} ms) {} CPU bursts (tau {:.0f}ms)".format(process.getName(), process.getArrivalTime(), process.getTotalBursts(), process.getEstimatedBurstTime() ))
    print("time 0ms: Simulator started for SRT [Q <empty>]")

	while(len(process_table) > 0):
		next_event = event_queue.get()
		time = int(next_event[0])
		process_name = next_event[1][0]
		event_type = next_event[1][1]
		process = process_table[process_name]
		#a process arrive
		if event_type == "Arrive":
			process.arrive()
			ready_queue.append(process_table[process_name])
			ready_queue.sort(key=operator.attrgetter('estimated_remaining_burst_time', 'name'))
			print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), print_ready_queue(ready_queue) ))
			if len(ready_queue) != 0 and (current_running == None and time >= CPU_vacant_at):
				ready_queue.pop(0)
				event_queue.put((time+cst,(process_name,"Run")))
				process.startContextSwitchIn(time)
				current_running = process
		#a process run
		elif event_type == "Run":
			expected = process.startRunning(time)
            event_queue.put((time + expected, (process_name, "CSOut")))
            CPU_vacant_at = time + expected + cst
            print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), expected, print_ready_queue(ready_queue) ))
		
		#context-switch out
		elif event_type == "CSOut":
			process.startContextSwitchOut(time)
			if process.total_bursts-process.index-1 == 0:
				event_queue.put((time,(process_name, "EnterIO")))
			else:
				event_queue.put((time + expected, (process_name, "CSOut")))
            	CPU_vacant_at = time + expected + cst
				if process.total_bursts-process.index-1 == 1:
            		print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} burst to go [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), process.total_bursts-process.index-1, print_ready_queue(ready_queue) ))
				else:
					print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q {}]".format(time, process_name, process.getEstimatedBurstTime(), process.total_bursts-process.index-1, print_ready_queue(ready_queue) ))
			if process.index < process.total_bursts -1:
				recalculate_tau(process,process.index) #recaculate_tau
				print("time {}ms: Recalculated tau = {}ms for process {} [Q {}]".format(time, process.getEstimatedBurstTime(), process.name, print_ready_queue(ready_queue) ))
                # Sort the ready queue by estimated_brust_time
                ready_queue.sort(key=operator.attrgetter('estimated_remaining_burst_time', 'name'))
                # switch out
                print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(time, process_name, int(time + cst + process.io_times[process.index]), print_ready_queue(ready_queue) ))
            context_switch_count += 1

		#enter I/O
		elif event_type == "EnterIO":
			expected = process.finishRunning(time)
			if expected = -1:
				print("time {}ms: Process {} terminated [Q {}]".format(time, process_name, print_ready_queue(ready_queue) ))
                del process_table[process_name]
			else:
				event_queue.put((time+expected, (process_name, "EnterQueue")))
			current_running = None
			if len(ready_queue) > 0:
				new_name = ready_queue.pop(0)
				new_process = process_table[new_name]
				event_queue.put((time+cst, (new_name, "Run")))
				new_process.startContextSwitchIn(time)
				current_running = new_process
		
		elif event_type == "EnterQueue":
			if process.getStatus == "IO":
				process.finishIO(time)
			ready_queue.append(process_table[process_name])
			ready_queue.sort(key=operator.attrgetter('estimated_remaining_burst_time', 'name'))
			print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]".format(time, process_name, print_ready_queue(ready_queue) ))
            if len(ready_queue) == 1 and current_running == None and time >= CPU_vacant_at:
                ready_queue.pop(0)
                event_queue.put((time + cst, (process_name, "Run")))
                process.startContextSwitchIn(time)
                current_running = process
			if len(ready_queue) == 1 and current_running != None and current_running.getEstimatedRemaining() > process.getEstimatedRemaining():
				ready_queue.pop(0)
				event_queue.put((time + cst, (process_name, "Run")))
                process.startContextSwitchIn(time)
				preemption_process = current_running
				current_running = process
				event_queue.put((time+cst,(preemption_process.getName(),"EnterQueue")))
				preemption_process.startContextSwitchOut()
				preemption_process.preempt()




		else:
			print("ERROR: <error-text-here>")
			return
