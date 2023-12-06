# 遗传算法解决旅行商问题_叶月月的博客-CSDN博客  https://blog.csdn.net/weixin_43550619/article/details/127738728

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import time
import random

# 读取城市数据
def read_data():
    data = pd.read_csv('city.csv')
    city_name = data['city'].values
    city_pos_x = data['x'].values
    city_pos_y = data['y'].values
    # 原始问题图
    plt.scatter(city_pos_x, city_pos_y)
    for i in range(len(city_pos_x)):
        plt.annotate(city_name[i], xy=(city_pos_x[i], city_pos_y[i]), xytext=(city_pos_x[i] + 0.1, city_pos_y[i] + 0.1))  # xy是需要标记的坐标，xytext是对应的标签坐标
    plt.show()
    return city_name, city_pos_x, city_pos_y

# 读取城市数据
def read_data_from_txt():
    file_path = 'E:/pyProj/python-collection/algorithm/data.txt'

    city_name = []
    city_pos_x = []
    city_pos_y = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i in range(0, len(lines), 3):
        current_city_name = lines[i].strip()
        current_city_position_x = float(lines[i + 1].strip())
        current_city_position_y = float(lines[i + 2].strip())

        city_name.append(current_city_name)
        city_pos_x.append(current_city_position_x)
        city_pos_y.append(current_city_position_y)

    # 原始问题图
    plt.scatter(city_pos_x, city_pos_y)
    for i in range(len(city_pos_x)):
        plt.annotate(city_name[i], xy=(city_pos_x[i], city_pos_y[i]), xytext=(city_pos_x[i] + 0.1, city_pos_y[i] + 0.1))

    plt.show()

    return city_name, city_pos_x, city_pos_y

# 计算不同城市间距离矩阵
def distances(city_name, city_pos_x, city_pos_y):
    global g_city_count, g_city_distance

    # 城市总数量
    g_city_count = len(city_name)

    # 城市距离矩阵初始化
    g_city_distance = np.zeros([g_city_count, g_city_count])
    for i in range(g_city_count):
        for j in range(g_city_count):
            g_city_distance[i][j] = math.sqrt((city_pos_x[i] - city_pos_x[j]) ** 2 + (city_pos_y[i] - city_pos_y[j]) ** 2)

    return g_city_count, g_city_distance

# 计算一条路径的总长度
def path_length(path, origin):   # 具体路径，出发源点
    distance = 0
    distance += g_city_distance[origin][path[0]]    # 初始化距离为从源点到路径的第一个城市的距离

    for i in range(len(path)):  # 开始循环遍历路径中的城市。
        if i == len(path) - 1:  # 如果当前城市是路径中的最后一个城市
            distance += g_city_distance[origin][path[i]]   # 添加从最后一个城市回到源点的距离
        else:
            distance += g_city_distance[path[i]][path[i + 1]]   # 添加从当前城市到下一个城市的距离

    return distance # 返回总距离

# 改良
def improve(path, improve_count, origin):    # 具体路径，改良迭代次数
    distance = path_length(path, origin)

    for i in range(improve_count):
        # 随机选择两个城市
        u = random.randint(0, len(path) - 1)
        v = u

        while u == v:
            v = random.randint(0, len(path) - 1)

        new_path = path.copy()      # 复制当前路径，以便进行修改

        t = new_path[u]             # 交换两个城市的位置
        new_path[u] = new_path[v]   # 将城市 v 移动到位置 u
        new_path[v] = t             # 将城市 u 移动到位置 v

        new_distance = path_length(new_path, origin)    # 计算修改后的路径的总长度。

        if new_distance < distance:  # 如果修改后的路径比当前路径更短,保留更优解
            distance = new_distance  # 更新当前路径的总长度。
            path = new_path.copy()   # 更新当前路径

    return path

# 环境选择父代种群
# 这个函数的目的是在种群中选择适应性较强的路径，确保它们在下一代中有更高的概率被选择作为父代。
def selection(population, retain_rate, live_rate, origin):    # 种群，适者比例, 生命强度
    # 对总距离进行从小到大排序
    graded = [[path_length(path, origin), path] for path in population] # graded 列表包含了种群中每个路径的长度和路径
    graded = [path[1] for path in sorted(graded)]   # 按照路径长度从小到大的顺序排列。然后，只保留路径本身，形成一个新的列表。

    # 选出适应性强的一部分染色体
    retain_length = int(len(graded) * retain_rate)

    # 从排序后的路径列表中取前 retain_length 个路径，这些路径具有较强的适应性，将其作为父代。
    parents = graded[: retain_length]   # 保留适应性强的染色体

    # 保留一定存活程度强的个体
    for weak in graded[retain_length:]: # 遍历排名在 retain_length 之后的路径，即适应性较弱的路径
        if random.random() < live_rate: # 对于每个适应性较弱的路径，以 live_rate 的概率决定是否保留。
            parents.append(weak)        # 如果保留，则将其添加到父代中

    return parents     # 返回父代种群 parents，其中包含了适应性较强的路径和一定程度上适应性较弱的路径

# 使用常规匹配交叉获得子代
# 实现了基于父代种群生成子代种群的操作，使用的是一种基本的交叉繁殖（crossover）策略
# 随机选取一个交配位，子代1交配位之前的基因选自父代1交配位之前，交配位之后按父代2顺序选择没有在子代1中出现的基因
# 子代2交配位之前的基因选自父代2交配位之前，交配位之后按父代1顺序选择没有在子代2中出现的基因
# 通过随机选择父母、交叉繁殖生成一定数量的子代，以增加种群的多样性。这里使用的是一种简单的交叉繁殖策略，即在路径的某个位置进行交叉。

def crossover(parents, population_num):    # 存活的父代种群，种群总数
    # 生成子代的个数，即总种群数量减去当前父代的数量。
    children_count = population_num - len(parents)

    # 用于存储生成的子代的列表
    children = []

    while len(children) < children_count:  # 生成子代
        # 在父母种群中随机选择父母代
        male_index = random.randint(0, len(parents) - 1)
        female_index = male_index
        while female_index == male_index:
            female_index = random.randint(0, len(parents) - 1)

        male = parents[male_index]
        female = parents[female_index]

        position = random.randint(0, len(male) - 1) # 随机产生一个交配位
        child1 = male[:position]   # 子代1取父亲的一部分路径
        child2 = female[:position] # 子代2取母亲的一部分路径

        # 将母亲中没有在子代1中出现的城市添加到子代1中。检查城市是否已经存在于子代1中.
        # 如果城市不在子代1中，将其添加到子代
        for i in female:
            if i not in child1:
                child1.append(i)

        for i in male:
            if i not in child2:
                child2.append(i)

        children.append(child1)
        children.append(child2)

    return children

# 变异：随机交换路径中两个城市位置
# 函数的目的是在一定的变异率下，对子代中的染色体（路径）进行随机的变异操作。变异是为了引入新的遗传信息，增加种群的多样性。
def mutation(children, mutation_rate):       # 孩子种群，变异率
    # 对每个子代进行遍历
    for i in range(len(children)):
        if random.random() < mutation_rate:  # 变异,以给定的变异率决定是否对当前子代进行变异
            child = children[i]
            u = random.randint(0, len(child) - 2)       # 随机选择一个城市的索引作为变异的起始位置
            v = random.randint(u + 1, len(child) - 1)

            tmp = child[u]
            child[u] = child[v]
            child[v] = tmp

            children[i]=child   # 更新当前子代

    return children

# 得到当前代种群最优个体
def get_result(population, origin):
    # graded列表中，每个元素是一个包含两个值的子列表。
    # 第一个值是通过调用 path_length 函数计算得到的路径长度，第二个值是种群中的路径。
    # 这样，graded 列表包含了种群中每个路径的长度 和 路径本身的信息。
    graded = [[path_length(path, origin), path] for path in population]

    # 对 graded 列表进行排序，按照路径长度从小到大的顺序排列。这样，graded 中的第一个元素就是最短路径及其长度。
    graded = sorted(graded)

    # 返回最短路径的 长度 和 路径本身
    return graded[0][0], graded[0][1]  # 返回种群的最优解

# 结果可视化
def plt_magin(iters, distance, result_path, origin, city_name, city_pos_x, city_pos_y):
    print("进化次数为", iters, "时的最佳路径长度为：", distance)
    result_path = [origin] + result_path + [origin]
    # print("最佳路线为：")
    # for i, index in enumerate(result_path):
    #     print(city_name[index] + "(" + str(index) + ")", end=' ')
    #     if i % 9 == 0:
    #         print()
    X = []
    Y = []
    for i in result_path:
        X.append(city_pos_x[i])
        Y.append(city_pos_y[i])

    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.plot(X, Y, '-o')
    plt.xlabel('经度')
    plt.ylabel('纬度')
    plt.title("GA_TSP")

    for i in range(len(X)):
        # xy是需要标记的坐标，xytext是对应的标签坐标
        plt.annotate(city_name[result_path[i]], xy=(X[i], Y[i]), xytext=(X[i] + 0.1, Y[i] + 0.1))

    plt.show()

# 遗传算法总流程
def GA_TSP(origin, population_num, improve_count, iter_count, retain_rate, live_rate, mutation_rate):
    # 源点，种群个体数，改良迭代数, 进化次数，适者概率，生命强度，变异率
    # city_name, city_pos_x, city_pos_y = read_data()
    city_name, city_pos_x, city_pos_y = read_data_from_txt()

    g_city_count, g_city_distance = distances(city_name, city_pos_x, city_pos_y)
    print('\n----------------------\n')
    print(g_city_distance)
    print('\n----------------------\n')

    list_city = [i for i in range(g_city_count)]    # 列表包含了所有城市的索引

    # 因为 TSP 问题通常规定从某个城市出发，经过所有其他城市，最终回到起始城市。因此，为了保证算法能够正常工作，需要从城市列表中排除起始城市。k
    list_city.remove(origin)    # 将起始城市排除在遍历的城市之外

    population = []

    for i in range(population_num): #  population_num == 300
        # 随机生成个体
        path = list_city.copy() # 0 - 33
        random.shuffle(path)    # 随机打乱  0 - 33 乱序

        # 使用改良方案尽量提高初始化种群多样性
        path = improve(path, improve_count, origin)

        population.append(path)

    every_gen_best = []  # 存储每一代最好的
    distance, result_path = get_result(population, origin)

    for i in range(iter_count):
        # 选择繁殖个体群
        parents = selection(population, retain_rate, live_rate, origin)
        # 交叉繁殖
        children = crossover(parents, population_num)
        # 变异
        children = mutation(children, mutation_rate)

        # 更新种群，采用杰出选择
        population = parents + children
        distance, result_path = get_result(population, origin)
        every_gen_best.append(distance)

        if(i % 500 == 0):
            plt_magin(i, distance, result_path, origin, city_name, city_pos_x, city_pos_y)

    plt_magin(i, distance, result_path, origin, city_name, city_pos_x, city_pos_y)
    plt.plot(range(len(every_gen_best)), every_gen_best)
    plt.show()


if __name__ == '__main__':
    start_time = time.time()

    GA_TSP(10, 300, 200, 10000, 0.3, 0.5, 0.01)  # 源点，种群个数，改良次数，进化次数，适者概率，生命强度，变异率

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"GA_TSP execution time: {execution_time} seconds")




""" txt信息
北京
116.46
39.92
天津
117.2
39.13
上海
121.48
31.22
重庆
106.54
29.59
拉萨
91.11
29.97
乌鲁木齐
87.68
43.77
银川
106.27
38.47
呼和浩特
111.65
40.82
南宁
108.33
22.84
哈尔滨
126.63
45.75
长春
125.35
43.88
沈阳
123.38
41.8
石家庄
114.48
38.03
太原
112.53
37.87
西宁
101.74
36.56
济南
117
36.65
郑州
113.6
34.76
南京
118.78
32.04
合肥
117.27
31.86
杭州
120.19
30.26
福州
119.3
26.08
南昌
115.89
28.68
长沙
113
28.21
武汉
114.31
30.52
广州
113.23
23.16
台北
121.5
25.05
海口
110.35
20.02
兰州
103.73
36.03
西安
108.95
34.27
成都
104.06
30.67
贵阳
106.71
26.57
昆明
102.73
25.04
香港
114.1
22.2
澳门
113.33
22.13

"""