#Summer 2020 CSCI 4210 Operating Systems project 1
#Team Members: Zhaoxi Sun, Xinyan Sun, Tongyu Wang, Yueting Liao
import sys #get argument
#test git hub hello

class process(object):
	"""docstring for process"""
	def __init__(self, arg):
		self.pid = arg[0]
		self.arrival = arg[1]
		self.burst_time = arg[2]
		self.num_burst = arg[3]
		self.io = arg[4]
		self.wait_time = [0]*arg[3]
		self.turnaround_times = [0]*arg[3]
		self.count = 0
		self.location = "NULL"



#main part
if __name__ == '__main__':
	if len(sys.argv) != 8:
		print("ERROR: Invalid argument.")
		sys.exit(2)

	num_process = int(sys.argv[1])
	seed = float(sys.argv[2])
	parameter = float(sys.argv[3])
	upper_bound = float(sys.argv[4])
	tcs = float(sys.argv[5])
	alpha = float(sys.argv[6])
	tslice = float(sys.argv[7])
	rradd = float(sys.argv[8])
