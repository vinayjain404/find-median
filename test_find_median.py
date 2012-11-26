import os
import random
import tempfile
import unittest

import find_median

def data_dir():
	return tempfile.mkdtemp()

class FindMedianTestCase(unittest.TestCase):
	def setUp(self):
		find_median.DATA_DIRECTORY = data_dir()
		self.test_filename = os.path.join(data_dir(), 'test.data')
		self.test_file = open(self.test_filename, 'w')

	def tearDown(self):
		os.remove(self.test_filename)

	def testFindMedianForLargeSet(self):
		self.create_input_file(range(500000))
		expected_median = 249999
		actual_median = find_median.find_median(self.test_filename)
		self.assertEqual(expected_median, actual_median)

	def testFindMedianForSmallSet(self):
		self.create_input_file(range(50))
		expected_median = 24
		actual_median = find_median.find_median(self.test_filename)
		self.assertEqual(expected_median, actual_median)

	def testFindMedianWithDuplicateAndNegativeValues(self):
		numbers = ['-1'] * 100 + range(50)
		self.create_input_file(numbers)
		expected_median = -1
		actual_median = find_median.find_median(self.test_filename)
		self.assertEqual(expected_median, actual_median)

	def create_input_file(self, numbers):
		random.shuffle(numbers)
		self.test_file.write('%s\n' %len(numbers))
		for num in numbers:
			self.test_file.write('%s\n' %num)
		self.test_file.close()

if __name__ == '__main__':
    unittest.main()
