from matrix import Matrix

mat_sum = Matrix(1000, 10)
mat_sum.load_from_file("data/sum_test.csv")
print(mat_sum.sum_range(0,3,150,8))