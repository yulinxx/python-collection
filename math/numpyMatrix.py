'''
Author: xx xx@ubuntu.com
Date: 2022-05-29 17:56:54
LastEditors: xx xx@ubuntu.com
LastEditTime: 2022-05-29 22:32:49
FilePath: /python-collection/math/numpyMatrix.py
Description: 点通过矩阵进行旋转, 并绘制出旋转前后的点 
'''

# pip install numpy

# Python - 矩阵 - Python数据结构 | 编程字典
# https://codingdict.com/article/4835

# matplotlib 之形状与路径：patches和path - 简书
# https://www.jianshu.com/p/d52132ab9ccc/

import matplotlib.pyplot as plt
import matplotlib.patches as mpathes

import numpy as np
import math

PI = 3.1415926

ptXArray = [0, 10, 10, 0]
ptYArray = [0, 0, 10, 10]

# 旋转
angle = -45  # 旋转角度
radian = angle * PI / 180

# 三角函数,度数的sin cos值
sinValue = math.sin(radian)
cosValue = math.cos(radian)

print(f'  ------ 三角函数,度数的sin cos值')
print(f'{sinValue}, {cosValue}')


print('------ 旋转矩阵')
rotateMatrix = np.array([
    [cosValue, -sinValue, 0],
    [sinValue, cosValue,  0],
    [0,         0,        1]])
    
print(rotateMatrix)

# 旋转点
ptXResArray = []
ptYResArray = []

for i in range(len(ptXArray)):
    rotatePt = np.array([[ptXArray[i]], [ptYArray[i]], [0]])

    ptRes = rotateMatrix.dot(rotatePt)
    # print(f'------ 旋转矩阵 点乘 点 结果为: {ptRes}')
    ptXResArray.append(ptRes[0][0])
    ptYResArray.append(ptRes[1][0])

ptXResArray.append(ptXResArray[0]) # 加入起点,使图形闭合
ptYResArray.append(ptYResArray[0])
fig = plt.figure(figsize=(26, 26))  # 设置图像大小
plt.plot(ptXResArray, ptYResArray, label='firt line', linewidth=1, color='blue',
         marker='o', markerfacecolor='blue', markersize=4)

ptXArray.append(ptXArray[0])
ptYArray.append(ptYArray[0])
plt.plot(ptXArray, ptYArray, label='second line', linewidth=1, color='red',
         marker='o', markerfacecolor='blue', markersize=4)

plt.show()

# 缩放

# 切变
