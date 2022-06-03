"""
Author: xx xx@ubuntu.com
Date: 2022-05-29 17:56:54
LastEditors: xx xx@ubuntu.com
LastEditTime: 2022-05-29 22:53:07
FilePath: /python-collection/math/numpyMatrix.py
Description: 点通过矩阵进行旋转, 并绘制出旋转前后的点 
"""

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

# 要进行操作的三角形
ptXArray = [10, 20, 15]
ptYArray = [10, 10, 20]

###########################################
# 绕Z轴旋转 (原点旋转)

# 若要进行 非原点的旋转变换:
# 1. 将物体旋转要绕的点移动到原点，
# 2. 移到原点后做旋转变换
# 3. 旋转变换完成后平移回原来的位置

angle = 75  # 旋转角度
radian = angle * PI / 180

# 三角函数,度数的sin cos值
sinValue = math.sin(radian)
cosValue = math.cos(radian)

print('------ 旋转矩阵')
rotateMatrix = np.array([
    [cosValue, -sinValue, 0, 0],
    [sinValue, cosValue, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])

print(rotateMatrix)

ptXRotateArray = []
ptYRotateArray = []
for i in range(len(ptXArray)):
    rotatePt = np.array([[ptXArray[i]], [ptYArray[i]], [0], [1]])

    ptRes = rotateMatrix.dot(rotatePt)
    ptXRotateArray.append(ptRes[0][0])
    ptYRotateArray.append(ptRes[1][0])

###########################################
# 缩放
print('------ 缩放矩阵')
xScale = 0.8
yScale = 0.6
scaleMatrix = np.array([
    [xScale, 0, 0, 0],
    [0, yScale, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])

print(scaleMatrix)

ptXScaleArray = []
ptYScaleArray = []

for i in range(len(ptXArray)):
    scalePt = np.array([[ptXArray[i]], [ptYArray[i]], [0], [1]])

    ptRes = scaleMatrix.dot(scalePt)
    ptXScaleArray.append(ptRes[0][0])
    ptYScaleArray.append(ptRes[1][0])

###########################################
# 平移 
print('------ 平移 矩阵')
xMov = 15
yMov = 15
transMatrix = np.array([
    [1, 0, 0, xMov],
    [0, 1, 0, yMov],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])

print(transMatrix)

ptXTransArray = []
ptYTransArray = []

for i in range(len(ptXArray)):
    transPt = np.array([[ptXArray[i]], [ptYArray[i]], [0], [1]])
    ptRes = transMatrix.dot(transPt)
    ptXTransArray.append(ptRes[0][0])
    ptYTransArray.append(ptRes[1][0])

###########################################
# 镜像

# 以指定直线进行镜像
# https://blog.csdn.net/cuixiping/article/details/11934085

print('------ 镜像 矩阵')
mirrorMatrix = np.array([
    [-1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])
print(mirrorMatrix)

ptXMirrorArray = []
ptYMirrorArray = []

for i in range(len(ptXArray)):
    mirrorPt = np.array([[ptXArray[i]], [ptYArray[i]], [0], [1]])

    ptRes = mirrorMatrix.dot(mirrorPt)
    ptXMirrorArray.append(ptRes[0][0])
    ptYMirrorArray.append(ptRes[1][0])

###########################################
# 中心X轴镜像
print('------ 中心X轴镜像 矩阵')
centerXMatrix = np.array([
    [-1,   0,   0,  0],
    [0,   1,   0,  0],
    [0,   0,   1,  0],
    [0,   0,   0,  1] ])

# 左移10
movLMatrix = np.array([
    [1,   0,   0,  -15],
    [0,   1,   0,  0],
    [0,   0,   1,  0],
    [0,   0,   0,  1] ])

# 右移10
movRMatrix = np.array([
    [1,   0,   0,  15],
    [0,   1,   0,  0],
    [0,   0,   1,  0],
    [0,   0,   0,  1] ])

# 组合矩阵
matX = movRMatrix.dot(centerXMatrix).dot(movLMatrix)

print(f'maX = \n{matX}')

ptXCMirrorArray = []
ptYCMirrorArray= []

for i in range(len(ptXArray)):
    mirPt = np.array([[ptXArray[i]], [ptYArray[i]], [0], [1]])

    ptR = matX.dot(mirPt)
    
    # 单个矩阵进行变换
    # ptResL = movLMatrix.dot(mirPt)
    # ptC = centerXMatrix.dot(ptResL)
    # ptR = movRMatrix.dot(ptC)

    ptXCMirrorArray.append(ptR[0][0])
    ptYCMirrorArray.append(ptR[1][0])
    

###########################################
# 切变 Shearing
# 切变是坐标系的变换，非均匀的拉伸。切变时候，角度变化，但是面积或体积不变。也可以理解为坐标轴间的角度变化，造成的扭曲。
# 剪切变换(shear transformation)是空间线性变换之一，是仿射变换的一种原始变换。
# 它指的是类似于四边形不稳定性那种性质，方形变平行四边形，任意一边都可以被拉长的过程

print('------ 切变矩阵')
s = 0.3  # y坐标根据x坐标的切变
t = 0.3  # x坐标根据y坐标的切变

shearMatrix = np.array([
    [1, s, 0, 0],
    [t, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])

print(shearMatrix)

ptXShearArray = []
ptYShearArray = []

for i in range(len(ptXArray)):
    shearPt = np.array([[ptXArray[i]], [ptYArray[i]], [0], [1]])

    ptRes = shearMatrix.dot(shearPt)
    ptXShearArray.append(ptRes[0][0])
    ptYShearArray.append(ptRes[1][0])

    print(ptRes[0][0])
    print(ptRes[1][0])
    print('------')

###########################################
# 对上边的切变求逆,即还原

print('------ 切变矩阵的逆矩陣')
invShearMatrix = np.matrix(shearMatrix).I
print(invShearMatrix)
print(invShearMatrix.shape)
print('----\n')

ptXInvShearArray = []  # 乘以逆矩陣后的点,即还原成最初的原始矩形
ptYInvShearArray = []

for i in range(len(ptXShearArray)):
    invShearPt = np.array([[ptXShearArray[i]], [ptYShearArray[i]], [0], [1]])
    print(invShearPt.shape)

    ptRes = invShearMatrix.dot(invShearPt)
    print(ptRes.shape)
    print(ptRes[0])
    print(ptRes[0].shape)
    print(ptRes[1])
    print(ptRes[1].shape)
    print('------')
    ptXInvShearArray.append(ptRes[0][0][0])
    ptYInvShearArray.append(ptRes[1][0][0])

###########################################
# 投影
print('------ 投影矩阵')

######################################################
# 绘图

# 原图
ptXArray.append(ptXArray[0])
ptYArray.append(ptYArray[0])

plt.plot(ptXArray, ptYArray, label='origin', linewidth=15, color='green',
         marker='o', markerfacecolor='green', markersize=4)

# 旋转
ptXRotateArray.append(ptXRotateArray[0])  # 加入起点,使图形闭合
ptYRotateArray.append(ptYRotateArray[0])
plt.plot(ptXRotateArray, ptYRotateArray, label='rotate', linewidth=1, color='blue',
         marker='o', markerfacecolor='blue', markersize=4)

# 缩放
ptXScaleArray.append(ptXScaleArray[0])
ptYScaleArray.append(ptYScaleArray[0])
plt.plot(ptXScaleArray, ptYScaleArray, label='scale', linewidth=1, color='#998866',
         marker='o', markerfacecolor='yellow', markersize=4)

# 平移
ptXTransArray.append(ptXTransArray[0])
ptYTransArray.append(ptYTransArray[0])
plt.plot(ptXTransArray, ptYTransArray, label='trans', linewidth=1, color='#AABBCC',
         marker='o', markerfacecolor='red', markersize=4)

# 镜像
ptXMirrorArray.append(ptXMirrorArray[0])
ptYMirrorArray.append(ptYMirrorArray[0])
plt.plot(ptXMirrorArray, ptYMirrorArray, label='Mirror', linewidth=1, color='#775599',
         marker='o', markerfacecolor='red', markersize=4)

# 对象中心X轴镜像 
ptXCMirrorArray.append(ptXCMirrorArray[0]) # 加入起点,使图形闭合
ptYCMirrorArray.append(ptYCMirrorArray[0])
plt.plot(ptXCMirrorArray, ptYCMirrorArray, label='xMir', linewidth=9, color='red',
         marker='o', markerfacecolor='blue', markersize=4)
         
# 切变
ptXShearArray.append(ptXShearArray[0])
ptYShearArray.append(ptYShearArray[0])
plt.plot(ptXShearArray, ptYShearArray, label='Shearing', linewidth=1, color='red',
         marker='o', markerfacecolor='red', markersize=4)

# 切变逆
print(ptXInvShearArray)
print(ptYInvShearArray)

ptXInvShearArray.append(float(ptXInvShearArray[0]))
ptYInvShearArray.append(float(ptYInvShearArray[0]))
plt.plot(ptXInvShearArray, ptYInvShearArray, label='InvShearing', linewidth=1, color='blue',
         marker='o', markerfacecolor='red', markersize=4)

# 投影
# ptXProjArray.append(ptXProjArray[0])
# ptYProjArray.append(ptYProjArray[0])
# plt.plot(ptXProjArray, ptYProjArray, label='proj', linewidth=1, color='red',
#          marker='o', markerfacecolor='red', markersize=4)

plt.show()
