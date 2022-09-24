import numpy as np

# 先构建一个ndarray对象\
matrix = np.array([  # 矩阵
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 0],
    [5, 4, 3, 2, 1]
])

t = np.array( [[0.], [0.], [0.], [1.]] )
x = t[0][0]
print(t)
print(x)
