from multiprocessing import Process, Queue

import math
import os

SPLIT_FACTOR = 125

def multiply_sequential(m_a, m_b):
	try:
		product = Matrix(m_a.rows, m_b.cols)
		if m_a.cols != m_b.rows:
			raise Error("Rows and Columns of the multplying matrices are mismatched.")
		for i in range(0, m_a.rows):
			for j in range(0, m_b.cols):
				dot_prod = 0
				for k in range(0, m_a.cols):
					dot_prod += m_a.data[i][k] * m_b.data[k][j]
				product.data[i][j] = dot_prod
		return product
	except Exception as e:
		raise e

def multiply_chunk(m_a, m_b, offset, row_range, seq_no):
	try:
		print("Running process: "+str(seq_no))
		product = Matrix(row_range, m_b.cols)
		if m_a.cols != m_b.rows:
			raise Error("Rows and Columns of the multplying matrices are mismatched.")
		for i in range(0, row_range):
			for j in range(0, m_b.cols):
				dot_prod = 0
				for k in range(0, m_a.cols):
					dot_prod += m_a.data[offset+i][k] * m_b.data[k][j]
				product.data[i][j] = dot_prod
		product.write_to_file(str(seq_no)+".csv")
	except Exception as e:
		raise e

def sum_elements(mat, start_i, start_j, end_i, end_j):
	try:
		final_sum = 0
		for i in range(start_i, end_i+1):
			for j in range(start_j, end_j+1):
				final_sum += mat[i][j]
		return final_sum
	except Exception as e:
		raise e

def sum_elements_pllel(mat, start_i, start_j, end_i, end_j, resultq):
	try:
		final_sum = 0
		for i in range(start_i, end_i+1):
			for j in range(start_j, end_j+1):
				final_sum += mat[i][j]
		resultq.put(final_sum)
	except Exception as e:
		raise e

class Matrix:

	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.data = [[0 for i in range(0, cols)] for j in range(0, rows)]

	def load_from_file(self, file_path):
		try:
			f = open(file_path, "r")
			i = 0
			for line in f.readlines():
				j = 0
				number_list = line.split(',')
				for number in number_list:
					self.data[i][j] = int(number)
					j += 1
				i += 1
		except Exception as e:
			raise e

	def display(self):
		try:
			for i in range(0, self.rows):
				row = " ".join([str(self.data[i][j]) for j in range(0, self.cols)])
				print(row)
		except Exception as e:
			raise e

	def write_to_file(self, filename):
		try:
			f = open(filename, "w")
			for i in range(0, self.rows):
				row = ",".join(str(self.data[i][j]) for j in range(0, self.cols))
				f.write(row+"\n")
			f.close()					
		except Exception as e:
			raise e

	@staticmethod
	def merge_result(rows, cols, processors):
		try:
			product = Matrix(rows, cols)
			result = []
			f_result = open("result_"+str(processors)+".csv", "w")
			for i in range(0, processors):
				f_chunk = open(str(i)+".csv", "r")
				f_result.write(f_chunk.read())
				f_chunk.close()
				os.remove(str(i)+".csv")
			f_result.close()
		except Exception as e:
			raise e

	@staticmethod
	def multiply_parallel(m_a, m_b, processors):
		try:
			row_range = int(m_a.rows/processors)
			procs = []
			for i in range(0, processors):
				proc = Process(target=multiply_chunk, args=(m_a, m_b, i, row_range, i))
				proc.start()
				procs.append(proc)
			for proc in procs:
				proc.join()
			Matrix.merge_result(m_a.rows, m_b.cols, processors)
		except Exception as e:
			raise e

	def sum_range(self, start_i, start_j, end_i, end_j):
		try:
			final_sum = 0
			if (start_i == end_i):
				return sum_elements(self.data, start_i, start_j, end_i, end_j)
			sum_upper_range = sum_elements(self.data, start_i, start_j, start_i, self.cols-1)
			sum_lower_range = sum_elements(self.data, end_i, 0, end_i, end_j)
			intrmdt_rows = end_i - start_i - 1
			processors = math.ceil(intrmdt_rows/SPLIT_FACTOR)
			resultq = Queue(); procs = []
			i1 = start_i + 1
			while(processors):
				i2 = (i1 + SPLIT_FACTOR - 1) if ((i1 + SPLIT_FACTOR - 1) < (end_i - 1)) else (end_i - 1)
				proc = Process(target=sum_elements_pllel, args=(self.data, i1, 0, i2, self.cols-1, resultq))
				proc.start()
				procs.append(proc)
				i1 = i2 + 1
				processors -= 1
			for proc in procs:
				proc.join()
			final_sum = sum_upper_range + sum_lower_range
			while not resultq.empty():
				final_sum += resultq.get()
			return final_sum
		except Exception as e:
			raise