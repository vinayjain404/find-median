# python imports
import glob
import os
import sys

DATA_DIRECTORY = 'data'
MAX_FILE_SIZE = 10

def find_median(filename):
	refresh_data_directory()
	number_of_elements = get_number_of_elements(filename)
	block_size = (number_of_elements / MAX_FILE_SIZE)
	split_input_data(filename, block_size)

def refresh_data_directory():
	# Create data directory if it does not exist and empty it if it does
	if os.path.exists(DATA_DIRECTORY):
		files = glob.glob(os.path.join(DATA_DIRECTORY,'*'))
		for f in files:
		    os.remove(f)
	else:
		os.makedirs(DATA_DIRECTORY)

def get_number_of_elements(filename):
	# parse the first line in the file to get the number of elements
	file = open(filename)
	number_of_elements = int(file.readline().strip())
	file.close()
	return number_of_elements

def split_input_data(filename, block_size):
	data_count = 0
	input_files = []
	output_file = None

	file = open(filename)
	# skip the first line as it contains the number of elements
	file.readline()

	for data in file:
		if (data_count % block_size) == 0:
			if output_file:
				output_file.close()
			filename = os.path.join(DATA_DIRECTORY, "input%s.data" %(data_count/block_size)) 
			input_files.append(filename)
			output_file = open(filename, 'w')
		output_file.write("%s" %data)
		data_count += 1
	return input_files

if __name__ == "__main__":
	find_median(sys.argv[1])
