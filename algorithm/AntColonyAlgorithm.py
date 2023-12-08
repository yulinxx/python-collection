# 蚁群优化算法(Ant Colony Optimization, ACO)
# 蚁群算法（Ant Colony Optimization，ACO）来解决旅行商问题（Traveling Salesman Problem，TSP）
# 自然界蚂蚁群体在寻找食物的过程中，通过一种被称为信息素（Pheromone）的物质实现相互的间接通信，从而能够合作发现从蚁穴到食物源的最短路径。
# 通过对这种群体智能行为的抽象建模，研究者提出了蚁群优化算法（Ant Colony Optimization, ACO），为最优化问题、尤其是组合优化问题的求解提供了一强有力的手段。

# 蚂蚁在寻找食物的过程中往往是随机选择路径的，但它们能感知当前地面上的信息素浓度，并倾向于往信息素浓度高的方向行进。信息素由蚂蚁自身释放，是实现蚁群内间接通信的物质。
# 由于较短路径上蚂蚁的往返时间比较短，单位时间内经过该路径的蚂蚁多，所以信息素的积累速度比较长路径快。
# 因此，当后续蚂蚁在路口时，就能感知先前蚂蚁留下的信息，并倾向于选择一条较短的路径前行。
# 这种正反馈机制使得越来越多的蚂蚁在巢穴与食物之间的最短路径上行进。由于其他路径上的信息素会随着时间蒸发，最终所有的蚂蚁都在最优路径上行进。


import numpy as np
import matplotlib.pyplot as plt

class AntColonyTSP:
    def __init__(self, coordinates, num_ant=45, alpha=1, beta=5, rho=0.1, Q=1, iter_max=200):
        self.m_coordinates = coordinates          # 城市坐标
        self.m_num_ant = num_ant                  # 蚂蚁个数
        self.m_num_city = coordinates.shape[0]    # 城市个数
        self.m_alpha = alpha                      # 信息素重要程度因子
        self.m_beta = beta                        # 启发函数重要程度因子
        self.m_rho = rho                          # 信息素的挥发速度
        self.m_Q = Q                              # 信息素释放总量
        self.m_iter_max = iter_max                # 循环最大值
        self.m_dist_mat = self.get_distmat()

        # 初始化信息素矩阵,所有城市之间的信息素初始值都为1
        self.m_pheromone_table = np.ones((self.m_num_city, self.m_num_city))
        self.m_patht_able = np.zeros((self.m_num_ant, self.m_num_city)).astype(int)

        # 统计信息
        self.m_length_aver = np.zeros(iter_max)     # 各代路径的平均长度
        self.m_length_best = np.zeros(iter_max)     # 各代及其之前遇到的最佳路径长度
        self.m_path_best = np.zeros((iter_max, self.m_num_city))

    def get_distmat(self):
        """
        计算了城市之间的距离矩阵 dist_mat，其中 m_dist_mat[i][j] 表示城市 i 到城市 j 的距离。
        最终的矩阵类似如下(i j k 代表三个城市, 数字为其距离):
        i  j  k
        i  0  5  3
        j  5  0  9
        k  3  9  0
        """
        num = self.m_num_city
        dist_mat = np.zeros((num, num))
        for i in range(num):
            for j in range(i, num):
                # np.linalg.norm 用于计算城市之间的欧几里德距离
                dist_mat[i][j] = dist_mat[j][i] = np.linalg.norm(self.m_coordinates[i] - self.m_coordinates[j])
        return dist_mat

    def run(self):
        '''执行算法'''
        iter = 0
        while iter < self.m_iter_max:
            self.generate_ant_paths(iter)
            self.update_statistics(iter)
            self.update_pheromones()

            if iter % 30 == 0:
                print("iter number:", iter)
            iter += 1

        self.plot_results()

    def generate_ant_paths(self, iter):
        '''随机产生各个蚂蚁的起点城市'''
        if self.m_num_ant <= self.m_num_city:   # 城市数比蚂蚁数多
            # 随机产生各个蚂蚁的起点城市
            self.m_patht_able[:, 0] = np.random.permutation(range(0, self.m_num_city))[:self.m_num_ant]
        else:   # 蚂蚁数比城市数多，需要补足
            self.m_patht_able[:self.m_num_city, 0] = np.random.permutation(range(0, self.m_num_city))[:]
            self.m_patht_able[self.m_num_city:, 0] = np.random.permutation(range(0, self.m_num_city))[
                :self.m_num_ant - self.m_num_city]    

    def update_statistics(self, iter):
        '''做出平均路径长度和最优路径长度'''
        length = np.zeros(self.m_num_ant)   # 计算各个蚂蚁的路径距离

         # 启发函数矩阵，表示蚂蚁从城市i转移到矩阵j的期望程度
        etatable = 1.0 / (self.m_dist_mat + np.diag([1e10] * self.m_num_city))

        for i in range(self.m_num_ant):
            visiting = self.m_patht_able[i, 0]      # 当前所在的城市
            unvisited = set(range(self.m_num_city)) # 未访问的城市,以集合的形式存储{}
            unvisited.remove(visiting)              # 删除元素；利用集合的remove方法删除存储的数据内容

            for j in range(1, self.m_num_city):  # 循环num_city-1次，访问剩余的num_city-1个城市
                # 轮盘法选择下一个要访问的城市
                listunvisited = list(unvisited)
                probtrans = np.zeros(len(listunvisited))

                for k in range(len(listunvisited)):
                    probtrans[k] = np.power(self.m_pheromone_table[visiting][listunvisited[k]], self.m_alpha) \
                        * np.power(etatable[visiting][listunvisited[k]], self.m_beta)

                cumsumprobtrans = (probtrans / sum(probtrans)).cumsum()
                cumsumprobtrans -= np.random.rand()
                k = listunvisited[(np.where(cumsumprobtrans > 0)[0])[0]]

                 # 元素的提取（也就是下一轮选的城市）
                self.m_patht_able[i, j] = k     # 添加到路径表中（也就是蚂蚁走过的路径)
                unvisited.remove(k)             # 然后在为访问城市set中remove（）删除掉该城市
                length[i] += self.m_dist_mat[visiting][k]
                visiting = k

            # 蚂蚁的路径距离包括最后一个城市和第一个城市的距离
            length[i] += self.m_dist_mat[visiting][self.m_patht_able[i, 0]]

        # 记录每次迭代的平均路径长度、最佳路径长度以及最佳路径。
        self.m_length_aver[iter] = length.mean()

        if iter == 0:
            self.m_length_best[iter] = length.min()
            self.m_path_best[iter] = self.m_patht_able[length.argmin()].copy()
        else:
            if length.min() > self.m_length_best[iter - 1]:
                self.m_length_best[iter] = self.m_length_best[iter - 1]
                self.m_path_best[iter] = self.m_path_best[iter - 1].copy()
            else:
                self.m_length_best[iter] = length.min()
                self.m_path_best[iter] = self.m_patht_able[length.argmin()].copy()

    def update_pheromones(self):
        '''更新信息素,为每只蚂蚁在路径上留下的信息素增量'''
        changepheromonetable = np.zeros((self.m_num_city, self.m_num_city))

        for i in range(self.m_num_ant):
            for j in range(self.m_num_city - 1):    # 计算信息素增量
                changepheromonetable[self.m_patht_able[i, j]][self.m_patht_able[i, j + 1]] += \
                    self.m_Q / self.m_dist_mat[self.m_patht_able[i, j]][self.m_patht_able[i, j + 1]]

            changepheromonetable[self.m_patht_able[i, j + 1]][self.m_patht_able[i, 0]] += \
                self.m_Q / self.m_dist_mat[self.m_patht_able[i, j + 1]][self.m_patht_able[i, 0]]

        # 计算信息素公式
        self.m_pheromone_table = (1 - self.m_rho) * self.m_pheromone_table + changepheromonetable

    def plot_results(self):
        # 做出平均路径长度和最优路径长度
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))
        axes[0].plot(self.m_length_aver, 'k', marker=u'')
        axes[0].set_title('Average Length')
        axes[0].set_xlabel(u'iteration')

        axes[1].plot(self.m_length_best, 'k', marker=u'')
        axes[1].set_title('Best Length')
        axes[1].set_xlabel(u'iteration')

        fig.savefig('average_best.png', dpi=500, bbox_inches='tight')
        plt.show()

        # 作出找到的最优路径图
        bestpath = self.m_path_best[-1]
        plt.plot(self.m_coordinates[:, 0], self.m_coordinates[:, 1], 'r.', marker=u'$\cdot$')
        plt.xlim([-100, 2000])
        plt.ylim([-100, 1500])

        for i in range(self.m_num_city - 1):
            m = int(bestpath[i])
            n = int(bestpath[i + 1])
            plt.plot([self.m_coordinates[m][0], self.m_coordinates[n][0]], [
                    self.m_coordinates[m][1], self.m_coordinates[n][1]], 'k')

        plt.plot([self.m_coordinates[int(bestpath[0])][0], self.m_coordinates[int(n)][0]],
                [self.m_coordinates[int(bestpath[0])][1], self.m_coordinates[int(n)][1]], 'b')

        ax = plt.gca()
        ax.set_title("Best Path")
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y_axis')

        plt.savefig('best path.png', dpi=500, bbox_inches='tight')
        plt.show()

if __name__ == '__main__':
    # 城市坐标(52个城市 4 * 13)
    m_coordinates = np.array([
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

    ant_colony = AntColonyTSP(m_coordinates)
    ant_colony.run()
