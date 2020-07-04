#Summer 2020 CSCI 4210 Operating Systems project 1
import sys #get argument

#main part
if __name__ == '__main__':
	if len(sys.argv) != 8:
		print("ERROR: Invalid argument.")
		sys.exit(2)

	number_process = int(sys.argv[1])
	seed = float(sys.argv[2])
	parameter = float(sys.argv[3])
	upper_bound = float(sys.argv[4])
	tcs = float(sys.argv[5])
	alpha = float(sys.argv[6])
	tslice = float(sys.argv[7])
	rradd = float(sys.argv[8])