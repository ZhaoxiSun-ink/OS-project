#Summer 2020 CSCI 4210 Operating Systems project 1
#Team Members: Zhaoxi Sun, Xinyan Sun, Tongyu Wang, Yueting Liao
import sys #get argument

class process(object):
	"""docstring for process"""
	def __init__(self, arg):
		self.pid = arg[0]
		self.arrival = arg[1]
		self.seed = arg[2]
		self.lambda = arg[3]
		self.upper_bound = arg[4]
		self.wait_time = [0]*arg[3]
		self.alpha = [0]*arg[3]
		self.location = "NULL"



#main part
if __name__ == '__main__':
	if len(sys.argv) != 8:
		print("ERROR: Invalid argument.")
		sys.exit(2)

	arrival = int(sys.argv[1])
	seed = float(sys.argv[2])
	parameter = float(sys.argv[3])
	upper_bound = float(sys.argv[4])
	t_cs = float(sys.argv[5])
	alpha = float(sys.argv[6])
	t_slice = float(sys.argv[7])
	rradd = float(sys.argv[8])
