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
	input_filenames = split_input_data(filename, block_size)
	buffer_size = block_size / len(input_filenames)

	# create file objects for the input data files
	input_files = [open(filename) for filename in input_filenames]

	# fill initial data structure
	input_buffer = []
	for file in input_files:
		lines_read = 0
		buffer = []
		while lines_read < buffer_size:
			data = file.readline()
			if not data:
				break
			lines_read += 1
			buffer.append(int(data.strip()))

		input_buffer.append(buffer)

	merging(input_buffer, block_size)

def merging(input_buffer, block_size):
	while True:
		smallest_element_list = [(buffer[0], i) for i, buffer in enumerate(input_buffer) if len(buffer) > 0]
		print smallest_element_list

		if not smallest_element_list:
			store_min_element(min_element, block_size, True)
			return

		min_element, min_index = min(smallest_element_list)
		input_buffer[min_index].pop(0)
		store_min_element(min_element, block_size)

output_buffer = []
output_filename_counter = 0
output_file = None

def store_min_element(min_element, block_size, forced_write=False):
	global output_file, output_buffer, output_filename_counter

	if forced_write:
		for num in output_buffer:
			output_file.write('%s\n' %num)
		output_file.close()
		return

	if len(output_buffer) % block_size == 0:
		if output_file:
			for num in output_buffer:
				output_file.write('%s\n' %num)
			output_buffer = []
			output_file.close()

		filename = os.path.join(DATA_DIRECTORY, 'output%s.data' %output_filename_counter)
		output_file = open(filename, 'w')
		output_filename_counter += 1

	output_buffer.append(min_element)

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
	num_count = 0
	num_data = []
	input_filenames = []
	input_file = None
	file = open(filename)

	# skip the first line as it contains the number of elements
	file.readline()

	for num in file:
		if (num_count % block_size) == 0:
			if input_file:
				for sorted_num in sorted(num_data):
					input_file.write('%s\n' %sorted_num)
				input_file.close()
				num_data = []

			filename = os.path.join(DATA_DIRECTORY, 'input%s.data' %(num_count/block_size))
			input_filenames.append(filename)
			input_file = open(filename, 'w')

		num_data.append(int(num.strip()))
		num_count += 1

	# store the numbers in the last file
	for sorted_num in sorted(num_data):
		input_file.write('%s\n' %sorted_num)

	input_file.close()
	return input_filenames

if __name__ == "__main__":
	find_median(sys.argv[1])
