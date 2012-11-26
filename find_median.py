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

	# if there are less then 100 elements then find median directly
	# as current algorithm does not support manipulating 10 input files
	# with max capacity less then 10 i.e len(elements) < 100
	if number_of_elements < 100:
		return find_median_for_small_list(filename)

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

	output_files = merge_numbers(input_buffers, max_capacity, input_buffer_size, input_files)

	# remove 1 as list are indexed from 0
	median_element_index = (number_of_elements -1) / 2

	file_number =  median_element_index / max_capacity
	index_number = median_element_index % max_capacity
	return fetch_value(output_files[file_number], index_number)

def find_median_for_small_list(filename):
	"""
		Returns median for a small list of numbers
	"""
	file = open(filename)
	len_numbers = int(file.readline().strip())
	numbers = sorted([int(num.strip()) for num in file.readlines()])
	return numbers[(len_numbers-1)/2]

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

def fetch_value(filename, index_number):
	"""
		Return a value at an index from a given file.
	"""
	value = open(filename).readlines()[index_number]
	return int(value.strip())

def merge_numbers(input_buffers, max_capacity, input_buffer_size, input_files):
	"""
		Given a set of buffered numbers for each input file perform a
		merge to sort them. The sorted numbers are successively stored
		into output files of max_capacity.
		Returns a list of output files created.

		Arguments:
		input_buffers: pre filled buffers with numbers from each file
		max_capacity: max capacity of each node/resource
		input_buffer_size: max size of each input buffer
		input_files: list of file objects for each input file
	"""

	buffer_write = BufferedWrite(max_capacity)
	while True:
		# build a list of smallest elements and index for each of the
		# input buffers if they are not empty
		smallest_element_list = [(buffer[0], i)
			for i, buffer in enumerate(input_buffers)
			if len(buffer) > 0]

		# save the buffered elements to disk if all input buffers empty
		if not smallest_element_list:
			buffer_write.flush()
			return buffer_write.files

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

		buffer_write.write(min_element)

class BufferedWrite:
	"""
		Class to handle buffered writes to a file in batches of
		size max_capacity.
	"""

	def __init__(self, max_capacity):
		self.max_capacity = max_capacity
		self.buffer = []
		self.file = None
		self.files = []
		self.filename_counter = 0

	def write(self, number):
		"""
			Writes a number to the buffer or disk if buffer size is
			equal to max_capacity.
		"""
		if (len(self.buffer) % self.max_capacity) == 0:
			if self.file:
				for num in self.buffer:
					self.file.write('%s\n' %num)
				self.buffer = []
				self.file.close()

			filename = os.path.join(
				DATA_DIRECTORY,
				'output%s.data' %self.filename_counter)

			self.file = open(filename, 'w')
			self.filename_counter += 1
			self.files.append(filename)

		self.buffer.append(number)

	def flush(self):
		"""
			Writes the buffer to disk if called.
		"""
		for num in self.buffer:
			self.file.write('%s\n' %num)
		self.file.close()

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
