# python 代码
# X Y 轴上的单位向量
import numpy as np

vX = [1, 0]
vY= [0, 1]

vA = [6, 6]
vB = [-6, 6]
vC = [-6, -6]
vD = [6, -6]

c1 = np.cross(vX, vA) # 逆时针 45 度
c2 = np.cross(vX, vB) # 逆时针 90 + 45 度
c3 = np.cross(vX, vC) # 逆时针 180 + 45 度
c4 = np.cross(vX, vD) # 逆时针 270 + 45 度
print(f'c1 {c1} c2 {c2}  c3 {c3} c4 {c4}')
#       c1 6    c2 6     c3 -6    c4 -6

d1 = np.dot(vX, vA) # 逆时针 45 度
d2 = np.dot(vX, vB) # 逆时针 90 + 45 度
d3 = np.dot(vX, vC) # 逆时针 180 + 45 度
d4 = np.dot(vX, vD) # 逆时针 270 + 45 度
print(f'd1 {d1} d2 {d2}  d3 {d3} d4 {d4}')
#       d1  6   d2  -6   d3  -6  d4  6

c5 = np.cross(vX, vY) # X与Y垂直
c6 = np.cross(vA, vD)   # 垂直
c7 = np.cross(vA, vC)   # 共线，方向相反
c8 = np.cross(vB, vD)   # 共线，方向相反
print(f'c5 {c5} c6 {c6}  c7 {c7} c8 {c8}')
#       c5  1   c6 -72   c7  0   c8  0

d5 = np.dot(vX, vY) # X与Y垂直
d6 = np.dot(vA, vD)   # 垂直
d7 = np.dot(vA, vC)   # 共线，方向相反
d8 = np.dot(vB, vD)   # 共线，方向相反
print(f'd5 {d5} d6 {d6}  d7 {d7} d8 {d8}')
#       d5 0    d6   0   d7  -72 d8 -72


print(' ===================================')

# 已知圆心c在(0,0)点, 圆上有一点 a(-36.8577, -33.7862),
# 求 a 的直径为另一端点 b

ptA = [-36.8577, -33.7862]
ptC = [0.0, 0.0]

# 求出a到c 的向量 vCA
vCA = (ptC[0] - ptA[0], ptC[1] - ptA[1])
print('vCA:', vCA)

# 求出vCA的向量长度，即圆的半径
lenCA = np.linalg.norm(vCA)
print('lenCA:', lenCA)

# 求出vCA的单位向量
normalCA = vCA / lenCA
print('normalCA:', normalCA)

# 此直径为半径的两倍，则ac单位向量延长直径的长度为
diameter = normalCA * lenCA * 2
print(diameter)

# 求得直径另一端点b
ptB = ptA + diameter
print('ptB:', ptB)

