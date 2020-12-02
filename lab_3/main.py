from matrix import Matrix
from datetime import datetime

mat_a = Matrix(1000, 1000)
mat_b = Matrix(1000, 1000)
mat_a.load_from_file("data/a_1000.csv")
mat_b.load_from_file("data/b_1000.csv")

processors = [1,2,4,8,10]

for p in processors:
	mat_a = Matrix(2000, 2000)
	mat_b = Matrix(2000, 2000)
	mat_a.load_from_file("data/a_1000.csv")
	mat_b.load_from_file("data/b_1000.csv")
	start_time = datetime.now()
	Matrix.multiply_parallel(mat_a, mat_b, p)
	time_taken = datetime.now() - start_time
	print("Processor Count: " + str(p))
	print("Time Taken: " + str(time_taken))
	del mat_a
	del mat_b