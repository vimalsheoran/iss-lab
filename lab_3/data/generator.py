import random

matrix_dimensions = [1000,2000,4000,8000,10000]

# for dim in matrix_dimensions:
# 	f_a = open("a_"+str(dim)+".csv", "w")
# 	f_b = open("b_"+str(dim)+".csv", "w")
# 	for i in range(0,1000):
# 		row_a = ""
# 		row_b = ""
# 		for j in range(0, 1000):
# 			row_a += str(random.randint(0,10));
# 			row_b += str(random.randint(0,10));
# 			row_a += ','; row_b += ','
# 		row_a = row_a.rstrip(',');
# 		row_b = row_b.rstrip(',');
# 		row_a += '\n'
# 		row_b += '\n'
# 		f_a.write(row_a)
# 		f_b.write(row_b)
# 	f_a.close()
# 	f_b.close()

for dim in matrix_dimensions:
	f_a = open("sum_test.csv", "w")
	for i in range(0,1000):
		row_a = ""
		for j in range(0, 10):
			row_a += "1,"
		row_a = row_a.rstrip(',')
		row_a += '\n'
		f_a.write(row_a)
	f_a.close()