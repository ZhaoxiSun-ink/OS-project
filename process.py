class Process():
    def __init__(self, name, arrival_time, burst_times, io_times):
        # Variables received from outside
        self.name = name
        self.arrival_time = arrival_time
        self.burst_times = burst_times
        self.remaining_burst_times = list(burst_times)
        self.io_times = io_times
        self.total_bursts = len(burst_times)
        assert len(burst_times) == len(io_times) + 1
        # Computed Variables
        self.turnaround_times = []
        self.waiting_times = []
        # Status can be: "IO", "Ready", "Running", "Context_Swtich_In" and "Context_Switch_Out"
        self.status = None
        self.index = 0
        # tmp Variables
        self.cpu_start_timestamp = -1
        self.cpu_end_timestamp = -1
    
    def getArrivalTime(self):
        return self.arrival_time

    def getTotalBursts(self):
        return self.total_bursts

    def getStatus(self):
        return self.status
    
    # Process arrives, and gets added to the ready queue
    # Modifies: Adds a new tuple to waiting_times; Changes status to "Ready"
    # Returns： Nothing
    def arrive(self, time):
        pass
    
    # Start Context Switch into CPU
    # Requires: Process must be at "Ready" status
    # Modifies: Adds a new tuple to turnaround_times (start turnaround timer); Changes status to "Context_Switch_In"
    # Modifies: Find last tuple in waiting_times (end waiting timer) and update
    # Returns: Nothing
    def startContextSwitchIn(self, time):
        pass

    # Process enters CPU for CPU burst
    # Requires: Process must be at "Context_Switch_In" status
    # Modifies: Changes status to "Running"
    # Returns: Expected end time of current CPU burst
    def startRunning(self, time):
        pass

    # Start Context Switch out of CPU
    # Requires: Process must be at "Running" status
    # Modifies: Changes status to "Context_Switch_Out"
    def startContextSwitchOut(self, time):
        pass

    # Process leaves running state.
    # Requires: Process must be at "Context_Switch_Out" status
    # Modifies: Adds a new tuple to waiting_times (start waiting timer); Changes status to "Ready"
    # Modifies: Reduce remaining_burst_times[index] by milliseconds already spent running in CPU
    def preempt(self, time):
        pass

    # Process finishes CPU burst.
    # Requires: Process must be at "Context_Switch_Out" status
    # Modifies: Changes status to "IO"
    # Returns: Expected end time of IO, -1 if process already ended
    def finishRunning(self, time):
        pass

    # Process finishes IO and enters ready queue
    # Requires: Process must be at "IO" status
    # Modifies: Adds a new tuple to waiting_times (start waiting timer); Change status to "waiting"
    # Returns: Nothing
    def finishIO(self, time):
        pass


if __name__ == "__main__":
    n = "Process"
    arr_t = 12
    burst_ts = [25, 24, 324, 23]
    io_ts = [12, 34, 632]
    process0 = Process(n, arr_t, burst_ts, io_ts)
    print(process0.getArrivalTime())

