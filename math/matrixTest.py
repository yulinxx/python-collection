import numpy as np

a = np.array([[1, 2], [3, 4]])  # 初始化一个非奇异矩阵(数组)
print(a)
resA = np.linalg.inv(a)
print(np.linalg.inv(a))  # 对应于MATLAB中 inv() 函数

# 矩阵对象可以通过 .I 更方便的求逆
A = np.matrix(a)
resB = A.I
print(A.I)

print('-----------------')
res = a.dot(np.linalg.inv(a))
print(res)