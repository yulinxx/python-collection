# 蚁群优化算法(Ant Colony Optimization, ACO)
# 使用 ACO 来解决旅行商问题（Traveling Salesman Problem，TSP）
# 自然界蚂蚁群体在寻找食物的过程中，通过一种被称为信息素（Pheromone）的物质实现相互的间接通信，从而能够合作发现从蚁穴到食物源的最短路径。
# 通过对这种群体智能行为的抽象建模，研究者提出了蚁群优化算法（ACO），为最优化问题、尤其是组合优化问题的求解提供了一强有力的手段。

# 蚂蚁在寻找食物的过程中往往是随机选择路径的，但它们能感知当前地面上的信息素浓度，并倾向于往信息素浓度高的方向行进。信息素由蚂蚁自身释放，是实现蚁群内间接通信的物质。
# 由于较短路径上蚂蚁的往返时间比较短，单位时间内经过该路径的蚂蚁多，所以信息素的积累速度比较长路径快。
# 因此，当后续蚂蚁在路口时，就能感知先前蚂蚁留下的信息，并倾向于选择一条较短的路径前行。
# 这种正反馈机制使得越来越多的蚂蚁在巢穴与食物之间的最短路径上行进。由于其他路径上的信息素会随着时间蒸发，最终所有的蚂蚁都在最优路径上行进。


import numpy as np
import matplotlib.pyplot as plt

class AntColonyTSP:
    def __init__(self, coordinates, num_ant=65, alpha=1, beta=5, rho=0.1, Q=1, iter_max=200):
        self.m_city_coordinates = coordinates     # 城市坐标
        self.m_num_ant = num_ant                  # 蚂蚁个数
        self.m_num_cities = coordinates.shape[0]  # 城市个数
        self.m_alpha = alpha                      # 信息素重要程度因子
        self.m_beta = beta                        # 启发函数重要程度因子
        self.m_rho = rho                          # 信息素的挥发速度
        self.m_Q = Q                              # 信息素释放总量
        self.m_iter_max = iter_max                # 循环最大值
        self.m_dist_table = self.get_distmat()    # 城市间距离矩阵

        # 初始化信息素矩阵,所有城市之间的信息素初始值都为1
        self.m_pheromone_table = np.ones((self.m_num_cities, self.m_num_cities))
        # 蚂蚁的路径，其中每一行代表一只蚂蚁的路径，每一列代表一个城市。
        self.m_ant_path_table = np.zeros((self.m_num_ant, self.m_num_cities)).astype(int)

        # 统计信息
        self.m_aver_len_array = np.zeros(iter_max)     # 存储每次迭代的路径的平均长度
        self.m_best_len_array = np.zeros(iter_max)     # 存储每次迭代中找到的最佳路径长度
        self.m_best_path_table = np.zeros((iter_max, self.m_num_cities))   # 存储每次迭代中找到的最佳路径

        # 设置打印选项，显示小数点后三位
        np.set_printoptions(precision=3, suppress=True)

    def get_distmat(self):
        """
        计算了城市之间的距离矩阵 dist_mat，其中 m_dist_table[i][j] 表示城市 i 到城市 j 的距离。
        最终的矩阵类似如下(i j k 代表三个城市, 数字为其距离):
           i  j  k
        i  0  5  3
        j  5  0  9
        k  3  9  0
        """
        num = self.m_num_cities
        dist_mat = np.zeros((num, num))
        for i in range(num):
            for j in range(i, num):
                # np.linalg.norm 用于计算城市之间的欧几里德距离
                dist_mat[i][j] = dist_mat[j][i] = np.linalg.norm(self.m_city_coordinates[i] - self.m_city_coordinates[j])

        # print("Distance Matrix:")
        # for row in dist_mat:
        #     print(row)

        return dist_mat

    def run(self):
        '''执行算法'''
        iter = 0
        while iter < self.m_iter_max:
            self.generate_ant_paths(iter)
            self.update_statistics(iter)
            self.update_pheromones()

            if iter % 50 == 0:
                print("iter number: ", iter)
                print(f"--- len: \n{self.m_aver_len_array[iter]}")
                print(f"--- best len:\n{self.m_best_len_array[:iter]}")
                print(f"--- best path:\n{self.m_best_path_table[iter]}")
                print('-----------------------------------------\n')

            iter += 1

        self.plot_results()

    def generate_ant_paths(self, iter):
        """
        随机产生各个蚂蚁的起点城市 m_ant_path_table 大致如下:
            城市a(起始城市)  b   c
         蚂蚁i  3           0   0
            j  1           0   0
            k  2           0   0
            l  3           0   0
            m  1           0   0
        """
        cities_array = range(0, self.m_num_cities)          # 创建一个包含 0 到 self.m_num_cities - 1 的整数的序列
        cities_array = np.random.permutation(cities_array)  # 随机打乱  permutation 置换/组合

        # 将打乱的城市序号数,放至table中的第一列
        if self.m_num_ant <= self.m_num_cities:   # 蚂蚁数 小于 城市数
            # 取 cities_array 前 self.m_num_ant 个元素(城市)，每个蚂蚁有不同的起始点
            self.m_ant_path_table[:, 0] = cities_array[:self.m_num_ant]
        else:   # 蚂蚁数 大于 城市数多，需要补足
            # 先将 m_ant_path_table 的前 m_num_cities 行的第一个元素设为 cities_array 的随机排列。
            # 然后，将多余的蚂蚁的起始城市 从 cities_array 中选择,此时会重复起始城市

            # [:self.m_num_cities]: 表示选择数组的前 self.m_num_cities 行。这是第一个维度的切片。
            # [:, 0]: 表示选择每一行的第一个元素，即第一列。这是第二个维度的切片。
            # 即将此表的第一行设置为城市路径
            self.m_ant_path_table[:self.m_num_cities, 0] = cities_array[:]

            # 剩余的蚂蚁从城市列表中选择 (可能有bug,右侧数据长度不够,左侧无法填满)
            self.m_ant_path_table[self.m_num_cities:, 0] = cities_array[:self.m_num_ant - self.m_num_cities]


        # print("Ant Path Table:")
        # chunk_size = 10  # 设置每次输出的行数
        # for i in range(0, self.m_num_ant, chunk_size):
        #     print(self.m_ant_path_table[i:i+chunk_size])

        # print("Ant Path Table First:")
        # print(self.m_ant_path_table[:, 0])

    def update_statistics(self, iter):
        '''计算各个蚂蚁的路径长度。更新平均路径长度、最优路径长度以及最优路径。 statistics/统计学'''
        # 启发函数矩阵，表示蚂蚁从城市i转移到矩阵j的期望程度
        # np.diag(v, k=0)，用于创建一个对角矩阵或从对角线元素中提取对角线。
        # 参数 v 是一个一维数组，表示对角线元素。
        # print(np.diag([1e10] * self.m_num_cities))

        # 在Python中，np.diag([1e10] * 52) 是NumPy库的用法，用于创建一个对角矩阵。解释如下：
        # 1e10：这是一个科学记数法表示的数字，10,000,000,000。
        # [1e10] * 52：这是一个Python列表操作，它将创建一个包含52个元素的列表，每个元素都是 1e10。
        # np.diag(...)：这是NumPy库的一个函数，用于从给定的对角线元素创建一个对角矩阵。
        # 所以，当你传入一个由52个 1e10 元素组成的列表时，它会返回一个52x52的对角矩阵，其中对角线上的每个元素都是 1e10，而矩阵的其他部分都是零。
        # 即np.diag([1e10] * 52) 会生成一个52x52的对角矩阵，其对角线上的值为10,000,000,000，其余部分的值都是0。
        # 对角线上的距离，即同一个城市，用一个很大的值表示
        diag_matrix = np.diag([1e10] * self.m_num_cities) # 创建对角矩阵 52 * 52,对角线上的数据为10的10次方,表示这些城市之间的距离非常远。

        # print("diag_matrix:")
        # for row in diag_matrix:
        #     print(row)

        # 计算城市间的启发函数矩阵，即城市间距离取倒数  两个输入矩阵中相同位置的元素相加，并将结果取倒数
        inspiration_matrix = 1.0 / (self.m_dist_table + diag_matrix)

        # print("inspiration_matrix:")
        # for row in inspiration_matrix:
        #     print(row)

        # print("\n\nPheromone Table:")
        # for row in self.m_pheromone_table:
        #     print(row)

        ant_path_len = np.zeros(self.m_num_ant)   # 保存每只蚂蚁的路径长度

        # 计算每个蚂蚁的路径
        for i in range(self.m_num_ant):             

            visiting = self.m_ant_path_table[i, 0]      # 当前蚂蚁的起始城市
            unvisited = set(range(self.m_num_cities)) # 所有城市列表 0 - 51
            unvisited.remove(visiting)              # 删除所在的起始城市，剩余的即为未访问的城市

            # 访问剩余的城市  从未访问的城市A 到其它未访问的所有城市
            for j in range(1, self.m_num_cities):   # 0 为起始城市,所以从1开始 
                list_unvisited = list(unvisited)    # 数据类型转换

                trans_prob  = np.zeros(len(list_unvisited))   # 全零数组，存储每个未访问城市的概率转移值

                # 对于每个未访问城市，计算概率转移值  即从一个未访问的城市到另一个未访问的城市间的转移概率值
                for k in range(len(list_unvisited)): 
                    # 计算概率转移值，其中包括信息素浓度和启发函数的影响。
                    un = list_unvisited[k]
                    p = self.m_pheromone_table[visiting][un] # 起点城市 到 未访问城市 的信息素浓度(1)
                    e = inspiration_matrix[visiting][un]     # 起点城市 到 未访问城市 的启发矩阵值(1/距离  距离越小值越大)
                    a = np.power(p, self.m_alpha)            # p 的 self.m_alpha (1)次方
                    b = np.power(e, self.m_beta)             # beta(5)

                    trans_prob[k] =  a * b    # 计算信息素和启发函数的乘积得到的概率转移值。距离越小值越大

                # 计算概率转移值的累积和，以便后续用于轮盘赌选择。 每个概率转移值 除以 总和，得到相对概率。这确保了所有概率值的总和为1，使其成为概率分布。

                # print('trans_prob')
                # print(trans_prob)

                cum_prob = (trans_prob  / sum(trans_prob)).cumsum()     # cumsum() 计算数组元素的累积和。

                # print('cum_prob a')
                # print(cum_prob)

                cum_prob -= np.random.rand()  # 为了进行轮盘赌选择，从随机值中减去一个随机数 [0.0, 1.0)。距离越小值越大,越容易被选择

                # np.where(cum_prob > 0)：找到累积概率大于0的位置
                # 从未访问城市列表中选择第一个满足条件的城市。
                # 整个过程的目的是通过轮盘赌算法选择下一个城市。cum_prob > 0 用于排除概率小于等于0的城市，然后选择第一个满足条件的城市。
                # 这种方式确保了每个城市被选择的概率与其对应的概率转移值成正比，实现了轮盘赌的效果。

                # print('cum_prob b')
                # print(cum_prob)
                # temp = np.where(cum_prob > 0)  # 返回一个大于0的索引的数组。
                sel = (np.where(cum_prob > 0)[0])[0] # 取出大于零的元素的索引,
                next = list_unvisited[sel]   # 通过轮盘法选择下一个要访问的城市。

                # 元素的提取（也就是下一轮选的城市）
                self.m_ant_path_table[i, j] = next # 将选择的城市添加到路径表中，表示蚂蚁走过的路径。
                unvisited.remove(next)             # 从未访问城市的集合中移除已经访问的城市。

                ant_path_len[i] += self.m_dist_table[visiting][next]   # 更新路径长度，将蚂蚁从当前城市移动到新城市的距离添加到路径长度中。
                visiting = next        # 更新当前所在的城市，以便下一步计算。

            # 蚂蚁的路径距离包括最后一个城市和第一个城市的距离
            ant_path_len[i] += self.m_dist_table[visiting][self.m_ant_path_table[i, 0]]

        # 记录每次迭代的平均路径长度、最佳路径长度以及最佳路径。
        # mean(): 是 NumPy 数组的方法，用于计算数组中所有元素的平均值。
        self.m_aver_len_array[iter] = ant_path_len.mean()

        if iter == 0:
            self.m_best_len_array[iter] = ant_path_len.min()
            self.m_best_path_table[iter] = self.m_ant_path_table[ant_path_len.argmin()].copy()
        else:
            if ant_path_len.min() > self.m_best_len_array[iter - 1]:
                self.m_best_len_array[iter] = self.m_best_len_array[iter - 1]
                self.m_best_path_table[iter] = self.m_best_path_table[iter - 1].copy()
            else:
                self.m_best_len_array[iter] = ant_path_len.min()
                self.m_best_path_table[iter] = self.m_ant_path_table[ant_path_len.argmin()].copy()

    def update_pheromones(self):
        '''更新信息素,为每只蚂蚁在路径上留下的信息素增量'''
        pheromone_increment = np.zeros((self.m_num_cities, self.m_num_cities))  # 存储每只蚂蚁在其路径上留下的信息素增量。

        for i in range(self.m_num_ant):
            for j in range(self.m_num_cities - 1):    # 计算信息素增量
                cur_city = self.m_ant_path_table[i, j]
                next_city = self.m_ant_path_table[i, j + 1]

                pheromone_increment[cur_city][next_city] += self.m_Q / self.m_dist_table[cur_city][next_city]
        
            # 保留最后一个城市
            start_city = self.m_ant_path_table[i, 0]
            pheromone_increment[next_city][start_city] += self.m_Q / self.m_dist_table[next_city][start_city]

        # 计算信息素公式    新信息素= (1 − 0.1) × 旧信息素 + 信息素增量  () m_rho 信息素的挥发速度 0-1)
        self.m_pheromone_table = (1 - self.m_rho) * self.m_pheromone_table + pheromone_increment 

    def plot_results(self):
        '''绘制平均路径长度和最优路径长度的图表。绘制找到的最优路径图。'''
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))
        axes[0].plot(self.m_aver_len_array, 'k', marker=u'')
        axes[0].set_title('Average Length')
        axes[0].set_xlabel(u'iteration')

        axes[1].plot(self.m_best_len_array, 'k', marker=u'')
        axes[1].set_title('Best Length')
        axes[1].set_xlabel(u'iteration')

        fig.savefig('average_best.png', dpi=500, bbox_inches='tight')
        plt.show()

        # 作出找到的最优路径图
        bestpath = self.m_best_path_table[-1]
        plt.plot(self.m_city_coordinates[:, 0], self.m_city_coordinates[:, 1], 'r.', marker=u'$\cdot$')
        plt.xlim([-100, 2000])
        plt.ylim([-100, 1500])

        for i in range(self.m_num_cities - 1):
            m = int(bestpath[i])
            n = int(bestpath[i + 1])
            plt.plot([self.m_city_coordinates[m][0], self.m_city_coordinates[n][0]], [
                    self.m_city_coordinates[m][1], self.m_city_coordinates[n][1]], 'k')

        plt.plot([self.m_city_coordinates[int(bestpath[0])][0], self.m_city_coordinates[int(n)][0]],
                [self.m_city_coordinates[int(bestpath[0])][1], self.m_city_coordinates[int(n)][1]], 'b')

        ax = plt.gca()
        ax.set_title("Best Path")
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y_axis')

        plt.savefig('best path.png', dpi=500, bbox_inches='tight')
        plt.show()

if __name__ == '__main__':
    # 城市坐标(52个城市 4 * 13)
    m_city_coordinates = np.array([
        [565.0, 575.0], [25.0, 185.0], [345.0, 750.0], [945.0, 685.0],
        [845.0, 655.0], [880.0, 660.0], [25.0, 230.0], [525.0, 1000.0],
        [580.0, 1175.0], [650.0, 1130.0], [1605.0, 620.0], [1220.0, 580.0],
        [1465.0, 200.0], [1530.0, 5.0], [845.0, 680.0], [725.0, 370.0],
        [145.0, 665.0], [415.0, 635.0], [510.0, 875.0], [560.0, 365.0],
        [300.0, 465.0], [520.0, 585.0], [480.0, 415.0], [835.0, 625.0],
        [975.0, 580.0], [1215.0, 245.0], [1320.0, 315.0], [1250.0, 400.0],
        [660.0, 180.0], [410.0, 250.0], [420.0, 555.0], [575.0, 665.0],
        [1150.0, 1160.0], [700.0, 580.0], [685.0, 595.0], [685.0, 610.0],
        [770.0, 610.0], [795.0, 645.0], [720.0, 635.0], [760.0, 650.0],
        [475.0, 960.0], [95.0, 260.0], [875.0, 920.0], [700.0, 500.0],
        [555.0, 815.0], [830.0, 485.0], [1170.0, 65.0], [830.0, 610.0],
        [605.0, 625.0], [595.0, 360.0], [1340.0, 725.0], [1740.0, 245.0]
    ])

    ant_colony = AntColonyTSP(m_city_coordinates)
    ant_colony.run()
