# Python数模笔记-模拟退火算法（4）旅行商问题_旅行商问题模拟退火算法python-CSDN博客  
# https://blog.csdn.net/youcans/article/details/116396137

# 模拟退火算法求解旅行商问题 Python程序
# Program: SimulatedAnnealing_v6.py
# Purpose: Simulated annealing algorithm for traveling salesman problem
# v1.0: = 关注 Youcans，分享原创系列 https://blog.csdn.net/youcans =
#   模拟退火求解旅行商问题（TSP）基本算法
# Copyright 2021 YouCans, XUPT
# Crated：2021-05-01

#  -*- coding: utf-8 -*-
import math                         # 导入模块 math
import random                       # 导入模块 random
import pandas as pd                 # 导入模块 pandas 并简写成 pd
import numpy as np                  # 导入模块 numpy 并简写成 np YouCans
import matplotlib.pyplot as plt     # 导入模块 matplotlib.pyplot 并简写成 plt

np.set_printoptions(precision=4)
pd.set_option('display.max_rows', 20)
pd.set_option('expand_frame_repr', False)
pd.options.display.float_format = '{:,.2f}'.format

# 子程序：初始化模拟退火算法的控制参数
def initParameter():
    # custom function initParameter():
    # Initial parameter for simulated annealing algorithm
    tInitial = 100.0                # 设定初始退火温度(initial temperature)
    tFinal  = 1                     # 设定终止退火温度(stop temperature)
    nMarkov = 1000                  # Markov链长度，也即内循环运行次数
    alfa    = 0.98                  # 设定降温参数，T(k)=alfa*T(k-1)
    return tInitial,tFinal,alfa,nMarkov

# 子程序：读取TSPLib数据
def read_TSPLib(fileName):
    # custom function read_TSPLib(fileName)
    # Read datafile *.dat from TSPlib
    # return coordinates of each city by YouCans, XUPT

    res = []
    with open(fileName, 'r') as fid:
        for item in fid:
            if len(item.strip())!=0:
                res.append(item.split())

    loadData = np.array(res).astype('int')      # 数据格式：i Xi Yi
    coordinates = loadData[:,1::]
    return coordinates


# 子程序：计算各城市间的距离，得到距离矩阵
def getDistMat(nCities, coordinates):
    # custom function getDistMat(nCities, coordinates):
    # computer distance between each 2 Cities
    distMat = np.zeros((nCities,nCities))       # 初始化距离矩阵
    for i in range(nCities):
        for j in range(i,nCities):
            # np.linalg.norm 求向量的范数（默认求 二范数），得到 i、j 间的距离
            distMat[i][j] = distMat[j][i] = round(np.linalg.norm(coordinates[i]-coordinates[j]))
    return distMat                              # 城市间距离取整（四舍五入）


# 子程序：计算 TSP 路径长度
def calTourMileage(tourGiven, nCities, distMat):
    # custom function caltourMileage(nCities, tour, distMat):
    # to compute mileage of the given tour
    mileageTour = distMat[tourGiven[nCities-1], tourGiven[0]]   # dist((n-1),0)
    for i in range(nCities-1):                                  # dist(0,1),...dist((n-2)(n-1))
        mileageTour += distMat[tourGiven[i], tourGiven[i+1]]
    return round(mileageTour)                     # 路径总长度取整（四舍五入）


# 子程序：绘制 TSP 路径图
def plot_tour(tour, value, coordinates):
    # custom function plot_tour(tour, nCities, coordinates)

    num = len(tour)
    x0, y0 = coordinates[tour[num - 1]]
    x1, y1 = coordinates[tour[0]]
    plt.scatter(int(x0), int(y0), s=15, c='r')      # 绘制城市坐标点 C(n-1)
    plt.plot([x1, x0], [y1, y0], c='b')             # 绘制旅行路径 C(n-1)~C(0)
    for i in range(num - 1):
        x0, y0 = coordinates[tour[i]]
        x1, y1 = coordinates[tour[i + 1]]
        plt.scatter(int(x0), int(y0), s=15, c='r')  # 绘制城市坐标点 C(i)
        plt.plot([x1, x0], [y1, y0], c='b')         # 绘制旅行路径 C(i)~C(i+1)

    plt.xlabel("Total mileage of the tour:{:.1f}".format(value))
    plt.title("Optimization tour of TSP{:d}".format(num))  # 设置图形标题
    plt.show()


# 子程序：交换操作算子
def mutateSwap(tourGiven, nCities):
    # custom function mutateSwap(nCities, tourNow)
    # produce a mutation tour with 2-Swap operator
    # swap the position of two Cities in the given tour

    # 在 [0,n) 产生 2个不相等的随机整数 i,j
    i = np.random.randint(nCities)          # 产生第一个 [0,n) 区间内的随机整数
    while True:
        j = np.random.randint(nCities)      # 产生一个 [0,n) 区间内的随机整数
        if i!=j: break                      # 保证 i, j 不相等

    tourSwap = tourGiven.copy()             # 将给定路径复制给新路径 tourSwap
    tourSwap[i],tourSwap[j] = tourGiven[j],tourGiven[i] # 交换 城市 i 和 j 的位置————简洁的实现方法

    return tourSwap

def main():
    # # 读取旅行城市位置的坐标
    coordinates = np.array([[565.0, 575.0], [25.0, 185.0], [345.0, 750.0], [945.0, 685.0], [845.0, 655.0],
                            [880.0, 660.0], [25.0, 230.0], [525.0, 1000.0], [580.0, 1175.0], [650.0, 1130.0],
                            [1605.0, 620.0], [1220.0, 580.0], [1465.0, 200.0], [1530.0, 5.0], [845.0, 680.0],
                            [725.0, 370.0], [145.0, 665.0], [415.0, 635.0], [510.0, 875.0], [560.0, 365.0],
                            [300.0, 465.0], [520.0, 585.0], [480.0, 415.0], [835.0, 625.0], [975.0, 580.0],
                            [1215.0, 245.0], [1320.0, 315.0], [1250.0, 400.0], [660.0, 180.0], [410.0, 250.0],
                            [420.0, 555.0], [575.0, 665.0], [1150.0, 1160.0], [700.0, 580.0], [685.0, 595.0],
                            [685.0, 610.0], [770.0, 610.0], [795.0, 645.0], [720.0, 635.0], [760.0, 650.0],
                            [475.0, 960.0], [95.0, 260.0], [875.0, 920.0], [700.0, 500.0], [555.0, 815.0],
                            [830.0, 485.0], [1170.0, 65.0], [830.0, 610.0], [605.0, 625.0], [595.0, 360.0],
                            [1340.0, 725.0], [1740.0, 245.0]])
    
    # fileName = "../data/eil76.dat"                      # 数据文件的地址和文件名
    # coordinates = read_TSPLib(fileName)                 # 调用子程序，读取城市坐标数据文件

    # 模拟退火算法参数设置
    tInitial,tFinal,alfa,nMarkov = initParameter()      # 调用子程序，获得设置参数

    nCities = coordinates.shape[0]              # 根据输入的城市坐标 获得城市数量 nCities
    distMat = getDistMat(nCities, coordinates)  # 调用子程序，计算城市间距离矩阵
    nMarkov = nCities                           # Markov链 的初值设置
    tNow    = tInitial                          # 初始化 当前温度(current temperature)

    # 初始化准备
    tourNow   = np.arange(nCities)   # 产生初始路径，返回一个初值为0、步长为1、长度为n 的排列
    valueNow  = calTourMileage(tourNow,nCities,distMat) # 计算当前路径的总长度 valueNow
    tourBest  = tourNow.copy()                          # 初始化最优路径，复制 tourNow
    valueBest = valueNow                                # 初始化最优路径的总长度，复制 valueNow
    recordBest = []                                     # 初始化 最优路径记录表
    recordNow  = []                                     # 初始化 最优路径记录表

    # 开始模拟退火优化过程
    iter = 0                        # 外循环迭代次数计数器
    while tNow >= tFinal:           # 外循环，直到当前温度达到终止温度时结束
        # 在当前温度下，进行充分次数(nMarkov)的状态转移以达到热平衡

        for k in range(nMarkov):    # 内循环，循环次数为Markov链长度
            # 产生新解：
            tourNew = mutateSwap(tourNow, nCities)      # 通过 交换操作 产生新路径
            valueNew = calTourMileage(tourNew,nCities,distMat) # 计算当前路径的总长度
            deltaE = valueNew - valueNow

            # 接受判别：按照 Metropolis 准则决定是否接受新解
            if deltaE < 0:                          # 更优解：如果新解的目标函数好于当前解，则接受新解
                accept = True
                if valueNew < valueBest:            # 如果新解的目标函数好于最优解，则将新解保存为最优解
                    tourBest[:] = tourNew[:]
                    valueBest = valueNew
            else:                                   # 容忍解：如果新解的目标函数比当前解差，则以一定概率接受新解
                pAccept = math.exp(-deltaE/tNow)    # 计算容忍解的状态迁移概率
                if pAccept > random.random():
                    accept = True
                else:
                    accept = False

            # 保存新解
            if accept == True:                      # 如果接受新解，则将新解保存为当前解
                tourNow[:] = tourNew[:]
                valueNow = valueNew

        # 平移当前路径，以解决变换操作避开 0,（n-1）所带来的问题，并未实质性改变当前路径。
        tourNow = np.roll(tourNow,2)                # 循环移位函数，沿指定轴滚动数组元素

        # 完成当前温度的搜索，保存数据和输出
        recordBest.append(valueBest)                # 将本次温度下的最优路径长度追加到 最优路径记录表
        recordNow.append(valueNow)                  # 将当前路径长度追加到 当前路径记录表
        print('i:{}, t(i):{:.2f}, valueNow:{:.1f}, valueBest:{:.1f}'.format(iter,tNow,valueNow,valueBest))

        # 缓慢降温至新的温度，
        iter = iter + 1
        tNow = tNow * alfa                              # 指数降温曲线：T(k)=alfa*T(k-1)

    # 结束模拟退火过程

    # 图形化显示优化结果
    figure1 = plt.figure()     # 创建图形窗口 1
    plot_tour(tourBest, valueBest, coordinates)
    figure2 = plt.figure()     # 创建图形窗口 2
    plt.title("Optimization result of TSP{:d}".format(nCities)) # 设置图形标题
    plt.plot(np.array(recordBest),'b-', label='Best')           # 绘制 recordBest曲线
    plt.plot(np.array(recordNow),'g-', label='Now')             # 绘制 recordNow曲线
    plt.xlabel("iter")                                          # 设置 x轴标注
    plt.ylabel("mileage of tour")                               # 设置 y轴标注
    plt.legend()                                                # 显示图例
    plt.show()

    print("----------------------------")
    print("Tour verification successful!")
    print("Best tour: \n", tourBest)
    print("Best value: {:.1f}".format(valueBest))

    exit()

if __name__ == '__main__':
    main()

