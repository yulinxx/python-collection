"""
Author: xx xx@ubuntu.com
Date: 2022-05-29 17:56:54
LastEditors: xx xx@ubuntu.com
LastEditTime: 2022-05-29 22:53:07
FilePath: /python-collection/math/numpyMatrix.py
Description: 点通过矩阵进行旋转, 并绘制出旋转前后的点 
"""

# pip install numpy


import matplotlib.pyplot as plt
import matplotlib.patches as mpathes

import numpy as np
import math

PI = 3.1415926

# 要进行操作的三角形
# ptXArray = [0, 100, 100, 0]
# ptYArray = [0, 0, 60, 0]

# 要进行操作的矩形
ptXArray = [0, 100, 100, 0, 0]
ptYArray = [0, 0, 60, 60, 0]


###########################################
"""构建旋转矩阵"""
def rotateMatrix(angle):
    radian = angle * 3.1415926 / 180 
    sinValue = math.sin(radian)
    cosValue = math.cos(radian)
    matrix = np.array([
    [cosValue, -sinValue, 0, 0],
    [sinValue, cosValue, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])
    return matrix
   
###########################################
"""构建绕指定点旋转矩阵"""
def rotatePtMatrix(angle, xPt, yPt):
    matMoveA = moveMatrix(-xPt, -yPt)   # 移至中心
    
    print('\n\n ------------------ moveMatrix(-xPt, -yPt)   # 移至中心 ')
    print(matMoveA)


    matRotate = rotateMatrix(angle)        # 旋转
    
    print('\n\n ------------------ matRotate = rotateMatrix(angle)        # 旋转 ')
    print(matRotate)

    matMoveB = moveMatrix(xPt, yPt)     # 移至原位


    print('\n\n ------------------ matMoveB = moveMatrix(xPt, yPt)     # 移至原位 ')
    print(matMoveB)

    mat = matMoveB.dot(matRotate).dot(matMoveA)

    print('\n\n ------------------ mat = matMoveB.dot(matRotate).dot(matMoveA) ')
    print(mat)

    return mat
    #return matMoveA.dot(matRotate).dot(matMoveB)

###########################################
"""构建平移矩阵"""
def moveMatrix(xMov, yMov):
    matrix = np.array([
    [1, 0, 0, xMov],
    [0, 1, 0, yMov],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])

    return matrix
    
###########################################
"""缩放矩阵"""
def scaleMatrix(scale):
    matrix = np.array([
        [scale, 0, 0, 0],
        [0, scale, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])
    return matrix

###########################################
"""中心X轴镜像"""
def mirrorMatrix(scale):
    matrix = np.array([
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])
    return matrix

###########################################
def ptDotMatrix(m, ptsX, ptsY):
    ptX = []
    ptY = []
    for i in range(len(ptsX)):
        pt = np.array([[ptsX[i]], [ptsY[i]], [0], [1]])
        ptRes = m.dot(pt)
        ptX.append(ptRes[0][0])
        ptY.append(ptRes[1][0])
    
    return ptX, ptY

###########################################
matMoveA = moveMatrix(-50, -30)   # 移至中心
matRotate = rotateMatrix(90)        # 旋转
matMoveB = moveMatrix(50, 30)     # 移至原位

# 组合矩阵
#matX = matMoveA.dot(matRotate).dot(matMoveB)
matX = matMoveB.dot(matRotate).dot(matMoveA)

print('\n\n ------------------ moveMatrix(-50, -30) ')
# print(matMoveA)
print(np.array_str(matMoveA, suppress_small=True))


print('\n\n ------------------ rotateMatrix(90) ')
print(matRotate)

print('\n\n ------------------ moveMatrix(50, 30) ')
print(matMoveB)

print('\n\n ------------------ matX = matMoveA.dot(matRotate).dot(matMoveB) ')
print(matX)
print(' ------------------ \n\n')



moveXPtsa, moveYPtsa = ptDotMatrix(matMoveA, ptXArray, ptYArray)
rotateXPts, rotateYPts = ptDotMatrix(matRotate, moveXPts, moveYPts)
moveXPtsb, moveYPtsb = ptDotMatrix(matMoveB, rotateXPts, rotateYPts)
# ptsX = ptDotMatrix(matX, movePtsB[0], movePtsB[1])

ptsX, ptsY = ptDotMatrix(matX, ptXArray, ptYArray)

######################################################
def drawData(xPts, yPts, c='blue'):
    plt.plot(xPts, yPts, label='rotate', linewidth=1, color=c,
            marker='o', markerfacecolor='blue', markersize=4)


# 绘图
# 设置横纵坐标比例相同
ax = plt.gca()
ax.set_aspect(1)

plt.plot(ptXArray, ptYArray, label='origin', linewidth=5, color='green',
         marker='o', markerfacecolor='green', markersize=4)

# drawData(moveXPtsa, moveYPtsa, 'blue')
# drawData(rotateXPts, rotateYPts, 'black')
# drawData(moveXPtsb, moveYPtsb, 'red')
drawData(ptsX, ptsY, 'green')

plt.show()
