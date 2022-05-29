'''
Author: xx xx@ubuntu.com
Date: 2022-05-29 17:56:54
LastEditors: xx xx@ubuntu.com
LastEditTime: 2022-05-29 22:53:07
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

ptXArray = [0, 10, 10, 0, 0]
ptYArray = [0, 0, 10, 10, 0]

###########################################
# 绕Z轴旋转
angle = -45  # 旋转角度
radian = angle * PI / 180

# 三角函数,度数的sin cos值
sinValue = math.sin(radian)
cosValue = math.cos(radian)

print(f'  ------ 三角函数,度数的sin cos值')
print(f'{sinValue}, {cosValue}')


print('------ 旋转矩阵')
rotateMatrix = np.array([
    [cosValue, -sinValue, 0, 0],
    [sinValue, cosValue,  0, 0],
    [0,         0,        1, 0],
    [0,         0,        0, 1] ])
    
print(rotateMatrix)

# 旋转点
ptXRotateArray = []
ptYRotateArray = []
for i in range(len(ptXArray)):
    rotatePt = np.array([[ptXArray[i]], [ptYArray[i]], [0], [0]])

    ptRes = rotateMatrix.dot(rotatePt)
    # print(f'------ 旋转矩阵 点乘 点 结果为: {ptRes}')
    ptXRotateArray.append(ptRes[0][0])
    ptYRotateArray.append(ptRes[1][0])

###########################################
# 缩放
print('------ 缩放矩阵')
scaleMatrix = np.array([
    [0.6, 0,   0, 0],
    [0,   0.6, 0, 0],
    [0,   0,   1, 0],
    [0,   0,   0, 1] ])
    
print(scaleMatrix)

# 缩放点
ptXScaleArray = []
ptYScaleArray = []

for i in range(len(ptXArray)):
    scalePt = np.array([[ptXArray[i]], [ptYArray[i]], [0], [0]])

    ptRes = scaleMatrix.dot(scalePt)
    # print(f'------ 旋转矩阵 点乘 点 结果为: {ptRes}')
    ptXScaleArray.append(ptRes[0][0])
    ptYScaleArray.append(ptRes[1][0])

###########################################
# 平移 
print('------ 平移 矩阵')
xMov = -10
yMov = -10
transMatrix = np.array([
    [1,    0,    0,  0],
    [0,    1,    0,  0],
    [0,    0,    1,  0],
    [xMov, yMov, 0,  1] ])
    
print(transMatrix)

# 缩放点
ptXTransArray = []
ptYTransArray = []

for i in range(len(ptXArray)):
    transPt = np.array([[ptXArray[i]], [ptYArray[i]], [0], [0]])

    ptRes = transMatrix.dot(transPt)
    ptXTransArray.append(ptRes[0][0])
    ptYTransArray.append(ptRes[1][0])

###########################################
# 切变



fig = plt.figure(figsize=(26, 26))  # 设置图像大小

# 原图
ptXArray.append(ptXArray[0])
ptYArray.append(ptYArray[0])

plt.plot(ptXArray, ptYArray, label='origin', linewidth=1, color='green',
         marker='o', markerfacecolor='green', markersize=4)

# 旋转后
ptXRotateArray.append(ptXRotateArray[0]) # 加入起点,使图形闭合
ptYRotateArray.append(ptYRotateArray[0])
plt.plot(ptXRotateArray, ptYRotateArray, label='rotate', linewidth=1, color='blue',
         marker='o', markerfacecolor='blue', markersize=4)

# 缩放后
ptXScaleArray.append(ptXScaleArray[0]) # 加入起点,使图形闭合
ptYScaleArray.append(ptYScaleArray[0])
plt.plot(ptXScaleArray, ptYScaleArray, label='scale', linewidth=1, color='red',
         marker='o', markerfacecolor='red', markersize=4)

# 平移后
ptXTransArray.append(ptXTransArray[0]) # 加入起点,使图形闭合
ptYTransArray.append(ptYTransArray[0])
plt.plot(ptXTransArray, ptYTransArray, label='trans', linewidth=1, color='red',
         marker='o', markerfacecolor='red', markersize=4)
         
plt.show()