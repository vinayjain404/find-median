# python imports
import glob
import os
import sys

DATA_DIRECTORY = 'data'

# Scaled down capacity of each function/node
SCALED_DOWN_FACTOR = 10

def find_median(filename):
	"""
		Return the median of a list of numbers in a given file.
		Argument is name of the file containing the list of numbers.
	"""
	refresh_data_directory()
	number_of_elements = get_number_of_elements(filename)
	max_capacity = number_of_elements / SCALED_DOWN_FACTOR
	input_filenames = split_input_data(filename, max_capacity)
	input_buffer_size = max_capacity / len(input_filenames)

	# create a list of file objects for the input data files
	input_files = [open(filename) for filename in input_filenames]

	# Fill up the input buffers initially with at MAX input_buffer_size
	# values from each of the input files.
	input_buffers = []
	for file in input_files:
		numbers = read_numbers_from_file(file, input_buffer_size)
		input_buffers.append(numbers)

	merge_numbers(input_buffers, max_capacity, input_buffer_size, input_files)

	# remove 1 as list are indexed from 0
	median_element_index = (number_of_elements / 2) - 1

	file_number =  median_element_index / max_capacity
	index_number = median_element_index % max_capacity
	return fetch_value(file_number, index_number)

def read_numbers_from_file(file, max_size):
	"""
		Returns a list of numbers read from a file object with either
		max_size elements or number of elements till EOF
	"""
	lines_read = 0
	numbers = []
	while lines_read < max_size:
		data = file.readline()
		if not data:
			break
		lines_read += 1
		numbers.append(int(data.strip()))
	return numbers

def fetch_value(file_number, index_number):
	"""
		Return a value at an index from a given file.
	"""
	return open(output_files[file_number]).readlines()[index_number]

def merge_numbers(input_buffers, max_capacity, input_buffer_size, input_files):
	"""
		Given a set of buffered numbers for each input file perform a
		merge to sort them. The sorted numbers are successively stored
		into output files of max_capacity.

		Arguments:
		input_buffers: pre filled buffers with numbers from each file
		max_capacity: max capacity of each node/resource
		input_buffer_size: max size of each input buffer
		input_files: list of file objects for each input file
	"""
	while True:
		# build a list of smallest elements and index for each of the
		# input buffers if they are not empty
		smallest_element_list = [(buffer[0], i)
			for i, buffer in enumerate(input_buffers)
			if len(buffer) > 0]

		# save the buffered elements to disk if all input buffers empty
		if not smallest_element_list:
			buffer_and_write_numbers(min_element, max_capacity, True)
			return

		# find the smallest element in the input buffers
		min_element, min_index = min(smallest_element_list)

		# remove the smallest element from the input buffer
		input_buffers[min_index].pop(0)

		# if the input buffer is empty we fill it with remaining values
		# from the corresponding input file
		if len(input_buffers[min_index]) == 0:
			numbers = read_numbers_from_file(
				input_files[min_index],
				input_buffer_size)
			input_buffers[min_index].extend(numbers)

		buffer_and_write_numbers(min_element, max_capacity)

# TODO To not use global variables and abstract it into its own class
output_buffer = []
output_file = None
output_files = []
output_filename_counter = 0

def buffer_and_write_numbers(number, max_capacity, forced_write=False):
	"""
		Buffers and writes a set of numbers into output files in
		batches of size max_capacity.
		forced_write: is True the current set of numbers are written
		to a file even if the batch is not of max_capacity.
	"""
	global output_file, output_buffer, output_filename_counter

	if forced_write:
		for num in output_buffer:
			output_file.write('%s\n' %num)
		output_file.close()
		return

	# write the buffer to disk if buffer size is equal to max_capacity
	if len(output_buffer) % max_capacity == 0:
		if output_file:
			for num in output_buffer:
				output_file.write('%s\n' %num)
			output_buffer = []
			output_file.close()

		filename = os.path.join(
			DATA_DIRECTORY,
			'output%s.data' %output_filename_counter)

		output_file = open(filename, 'w')
		output_filename_counter += 1
		output_files.append(filename)

	output_buffer.append(number)

def refresh_data_directory():
	"""
		Create an empty data directory or clear it if exists already.
	"""
	if os.path.exists(DATA_DIRECTORY):
		files = glob.glob(os.path.join(DATA_DIRECTORY,'*'))
		for f in files:
		    os.remove(f)
	else:
		os.makedirs(DATA_DIRECTORY)

def get_number_of_elements(filename):
	"""
		Fetch the numbers of elements in the file.
	"""
	file = open(filename)
	number_of_elements = int(file.readline().strip())
	file.close()

	return number_of_elements

def split_input_data(filename, max_capacity):
	"""
		Split the given numbers in a single file into multiple files of
		max_capacity.
		Return a list of split input filenames.
	"""
	num_count = 0
	num_data = []
	input_filenames = []
	input_file = None

	file = open(filename)
	# skip the first line as it contains the number of elements
	file.readline()

	for num in file:
		# store the max_capacity list of numbers into a file
		if (num_count % max_capacity) == 0:
			if input_file:
				# sort and store the given set of numbers into
				# a file
				for sorted_num in sorted(num_data):
					input_file.write('%s\n' %sorted_num)
				input_file.close()
				num_data = []

			# dynamically build the filename
			filename = os.path.join(
				DATA_DIRECTORY,
				'input%s.data' %(num_count/max_capacity))

			input_filenames.append(filename)
			input_file = open(filename, 'w')

		# convert the num string read from file to int
		num_data.append(int(num.strip()))
		num_count += 1

	# store the remaining numbers into the last file
	for sorted_num in sorted(num_data):
		input_file.write('%s\n' %sorted_num)

	input_file.close()
	return input_filenames

if __name__ == "__main__":
	median = find_median(sys.argv[1])
	print "Median is %s" %median
