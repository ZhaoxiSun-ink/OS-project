class Process():
    def __init__(self, name, arrival_time: int, burst_times: list, io_times: list):
        # Variables received from outside
        self.name = name
        self.arrival_time = arrival_time
        self.burst_times = burst_times
        self.estimated_burst_time = 0
        self.remaining_burst_times = list(burst_times)
        self.io_times = io_times
        self.total_bursts = len(burst_times)
        assert len(burst_times) == len(io_times) + 1
        # Computed Variables
        self.turnaround_times = [] # [(start_time, end_time), (start_time, end_time), ...]
        self.waiting_times = [] # [(start_time, end_time), (start_time, end_time), ...]
        # Status can be: "IO", "Ready", "Running", "Context_Swtich_In" and "Context_Switch_Out"
        self.status = None
        # i-th CPU burst we are now in
        self.index = 0
        # tmp Variables
        self.cpu_start_timestamp = -1
        self.cpu_end_timestamp = -1
        self.estimated_remaining_burst_time = self.estimated_burst_time - (self.burst_times[self.index] - self.remaining_burst_times[self.index])

    # You can add getters to fill your needs
    def getName(self):
        return self.name

    def getArrivalTime(self):
        return self.arrival_time

    def getTotalBursts(self):
        return self.total_bursts

    def getStatus(self):
        return self.status

    def getEstimatedRemaining(self,time):
        return self.startRunning(time) - time

    def getTotalBurstTime(self):
        ans = 0
        for burst in self.burst_times:
            ans += burst
        return int(ans)

    def getTotalWaitingTime(self):
        ans = 0
        for interval in self.waiting_times:
            if interval[1] == -1:
                break
            ans += interval[1] - interval[0]
        return ans

    def getTotalTurnaroundTime(self):
        ans = 0
        for interval in self.turnaround_times:
            if interval[1] == -1:
                break
            ans += interval[1] - interval[0]
        return ans

    # For SJF and SRT
    def getEstimatedBurstTime(self):
        return int(self.estimated_burst_time)


    def print(self):
        print("Process {} has {} CPU bursts, and arrvies at {}.".format(self.name, self.total_bursts, self.arrival_time))
        for i in range(self.total_bursts-1):
            print("Burst {} has a time {}, remains time {}, and IO time {}.".format(i, self.burst_times[i], self.remaining_burst_times[i], self.io_times[i]))
        print("Last Burst has a time {}, and remains time {}.".format(self.burst_times[self.total_bursts-1], self.remaining_burst_times[self.total_bursts-1]))
        print("Process is at burst {} and has status {}.".format(self.index, self.status))


    # Process arrives, and gets added to the ready queue
    # Modifies: Adds a new tuple to waiting_times; Changes status to "Ready"
    # Returns: Nothing
    def arrive(self):
        assert self.status == None
        self.waiting_times.append((self.arrival_time, -1))
        self.status = "Ready"

    # Start Context Switch into CPU
    # Requires: Process must be at "Ready" status
    # Modifies: Adds a new tuple to turnaround_times (start turnaround timer); Changes status to "Context_Switch_In"
    # Modifies: Find last tuple in waiting_times (end waiting timer) and update
    # Returns: Nothing
    def startContextSwitchIn(self, time):
        assert self.status == "Ready"
        waiting_time_start_timestamp = self.waiting_times[len(self.waiting_times)-1][0]
        self.waiting_times[len(self.waiting_times)-1] = (waiting_time_start_timestamp, time)
        self.turnaround_times.append((time, -1))
        self.status = "Context_Switch_In"

    # Process enters CPU for CPU burst
    # Requires: Process must be at "Context_Switch_In" status
    # Modifies: Changes status to "Running"
    # Returns: Expected end time of current CPU burst
    def startRunning(self, time):
        assert self.status == "Context_Switch_In"
        self.status = "Running"
        self.cpu_start_timestamp = time
        return self.remaining_burst_times[self.index]

    # Start Context Switch out of CPU
    # Requires: Process must be at "Running" status
    # Modifies: Changes status to "Context_Switch_Out"
    # Modifies: Reduce remaining_burst_times[index] by milliseconds already spent running in CPU
    def startContextSwitchOut(self, time):
        assert self.status == "Running"
        self.status = "Context_Switch_Out"
        self.cpu_end_timestamp = time
        self.remaining_burst_times[self.index] -= self.cpu_end_timestamp - self.cpu_start_timestamp

    # Process leaves running state.
    # Requires: Process must be at "Context_Switch_Out" status
    # Modifies: Adds a new tuple to waiting_times (start waiting timer); Changes status to "Ready"
    def preempt(self, time):
        assert self.status == "Context_Switch_Out"
        self.status = "Ready"
        self.waiting_times.append((time, -1))

    # Process finishes CPU burst.
    # Requires: Process must be at "Context_Switch_Out" status
    # Modifies: Changes status to "IO"; Find last tuple in turnaround_times (stop turnaround timer)
    # Returns: Expected end time of IO, -1 if process already ended
    def finishRunning(self, time):
        assert self.status == "Context_Switch_Out"
        assert self.remaining_burst_times[self.index] == 0
        self.status = "IO"
        turnaround_time_start_timestamp = self.turnaround_times[len(self.turnaround_times) - 1][0]
        self.turnaround_times[len(self.turnaround_times) - 1] = (turnaround_time_start_timestamp, time)
        if self.index == self.total_bursts - 1:
            self.status = "Terminated"
            return -1
        return self.io_times[self.index]

    # Process finishes IO and enters ready queue
    # Requires: Process must be at "IO" status
    # Modifies: Adds a new tuple to waiting_times (start waiting timer); Change status to "waiting"
    # Modifies: Increases index by 1
    # Returns: Nothing
    def finishIO(self, time):
        assert self.status == "IO"
        self.status = "Ready"
        self.waiting_times.append((time, -1))
        self.index += 1

if __name__ == "__main__":
    n = "Process"
    arr_t = 12
    burst_ts = [25, 24, 324, 23]
    io_ts = [12, 34, 632]
    process0 = Process(n, arr_t, burst_ts, io_ts)
    process0.arrive()
    process0.startContextSwitchIn(14)
    future = process0.startRunning(16)
    process0.startContextSwitchOut(16 + future)
    process0.finishRunning(18 + future)
    process0.print()
