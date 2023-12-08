# 规划算法专栏之随机快速搜索树（RRT）_快速搜索随机树算法-CSDN博客  https://blog.csdn.net/weixin_43890711/article/details/107120451
# 规划一条从起点到终点的无碰撞的路径
# 规划算法种类有很多，比如基于图的搜索算法、人工势场法、基于采样的规划方法等。
# 下面示例就是一种典型的基于采样的规划方法：随机快速搜索树（RRT）。

# RRT是一种在完全已知的环境中通过采样扩展搜索的算法，相比较于基于图的搜索算法，最主要的优点就是快，
# 因此在多自由度机器人的规划问题中发挥着较大的作用，比如机械臂的规划算法基本都是以RRT为基础的。

# 但同时他也有比较明显的缺点，比如通常不最优、规划的路径非常不平滑等。
# 但这些缺点的存在使得后面还有很多对RRT算法的改进，毕竟人无完人，也不能使用一个RRT就能应对所有规划问题。
# RRT算法是概率完备的，就是说如果规划时间足够长，如果确实存在一条可行路径，RRT是可以找出这条路径的。
# 但这里存在限制条件，如果规划时间不够长，迭代次数较少，有可能不能找出实际存在的路径。
# 从名字来看，RRT，全名Rapid-exploration Random Tree。
# Rapid-exploration指的是RRT的效果，可以快速进行搜索，Random指的是搜索的方式，通过在环境中随机采样的方式探索整个环境。
# Tree指的是已搜索的位置通过一棵树来存储，每个位置都有自己的父节点和子节点。搜索完成的路径通常是从树的根节点到一个叶节点的路径。
# 如下图所示，蓝色圆圈为障碍，起点为0，0，终点为6，10。使用RRT来规划一条无碰撞路径，绿色为规划时维护的树。

import math
import random
import matplotlib.pyplot as plt
import numpy as np

show_animation = True

class RRT:

    class Node:
        # Node 类表示树中的节点。每个节点包含位置 (x, y)、路径信息 path_x 和 path_y，以及一个指向父节点的指针 parent。
        def __init__(self, x, y):
            self.x = x
            self.y = y
            # self.path_x = [] # to define the path from parent to current---
            # self.path_y = [] # the purpose is to check collision of the path
            self.path_x = []  # 保存从父节点到当前节点的路径
            self.path_y = []  # 用于检查路径的碰撞

            self.parent = None

    def __init__(self, start, goal, obstacle_list, rand_area,
                 expand_dis=5, path_resolution=0.5, goal_sample_rate=5, max_iter=500):
        """
        Setting Parameter
        start:Start Position [x,y]
        goal:Goal Position [x,y]
        obstacleList:obstacle Positions [[x,y,size],...]
        randArea:Random Sampling Area [min,max]

        start: 起始位置 [x, y]
        goal: 目标位置 [x, y]
        obstacle_list: 障碍物的位置和大小的列表 [[x, y, size], ...]
        rand_area: 随机采样区域的范围 [min, max]
        expand_dis: 扩展距离,该距离决定了新节点与当前节点之间的步进长度。
        path_resolution: 路径分辨率，用于控制在沿着两个节点之间创建路径时的离散程度。决定了路径上的点的间隔。
        goal_sample_rate: 目标点采样率，用于控制在树的生长过程中，采样目标点的频率。决定了算法在搜索空间中寻找目标的方式。
        max_iter: 最大迭代次数

        扩展距离（expand_dis），用于控制每次从当前节点扩展的距离。该距离决定了新节点与当前节点之间的步进长度。
        在RRT算法中，每次迭代都会选择一个随机点，并尝试沿着从最近节点到该随机点的方向扩展一定距离。这个扩展距离是算法的一个关键参数，它影响了树的生长方式。
        较大的扩展距离可能导致树生长得更快，但也可能增加碰撞的风险，因为新节点可能会更快地穿过潜在的障碍物。相反，较小的扩展距离可以更好地细致搜索，但也可能导致树生长缓慢。
        在实际应用中，通过调整扩展距离可以平衡路径规划的速度和质量。通常，需要根据具体问题的要求进行调整，以获得满意的路径规划结果。
                
        路径分辨率（path_resolution），用于控制在沿着两个节点之间创建路径时的离散程度。这个参数决定了路径上的点的间隔。
        具体来说，路径分辨率定义了沿着两个节点之间生成路径时，路径上相邻两点之间的最小距离。在RRT中，路径是通过从一个节点向着另一个节点沿着方向逐步扩展而生成的，而路径分辨率就是控制这个扩展过程中每一步的距离。
        较小的路径分辨率会导致生成的路径更加细致，但也会增加计算的复杂性。相反，较大的路径分辨率会生成较为简化的路径，但可能会错过一些细节。
        在实际应用中，通过调整路径分辨率可以平衡路径规划的准确性和计算效率。选择适当的路径分辨率有助于生成满足问题要求的路径，并在计算成本和路径质量之间取得平衡。

        目标点采样率（goal_sample_rate），用于控制在树的生长过程中，采样目标点的频率。这个参数影响了算法在搜索空间中寻找目标的方式。
        在RRT算法中，除了随机采样新的随机点，还会以一定的概率采样目标点。这是为了增加找到目标的机会，尤其是当搜索空间较大时。目标点采样率即控制了采样目标点的概率。
        如果目标点采样率较低，算法更倾向于朝着随机方向生长，从而覆盖整个搜索空间。如果目标点采样率较高，算法更倾向于朝着目标方向生长，以更快地找到目标。
        在实际应用中，通过调整目标点采样率可以平衡算法的探索性和收敛性。选择适当的目标点采样率有助于在搜索空间中高效地找到从起点到目标的路径。

        """
        self.start = self.Node(start[0], start[1])
        self.end = self.Node(goal[0], goal[1])
        self.min_rand = rand_area[0]
        self.max_rand = rand_area[1]
        self.expand_dis = expand_dis
        self.path_resolution = path_resolution
        self.goal_sample_rate = goal_sample_rate
        self.max_iter = max_iter
        self.obstacle_list = obstacle_list
        self.node_list = []

    def planning(self, animation=True):
        """
        RRT路径规划
        rrt path planning
        animation: flag for animation on or off
        根据设定的最大迭代次数进行RRT路径规划。
        在每次迭代中，随机采样一个节点，找到树中距离最近的节点，并尝试沿着这个方向扩展新节点。
        检查新节点是否与障碍物发生碰撞，如果没有碰撞则将新节点添加到树中。
        如果启用了动画 (animation=True)，则每隔一段时间绘制一次当前的RRT树。
        """
        self.node_list = [self.start]
        for i in range(self.max_iter):  # 迭代
            rnd_node = self.get_random_node()
            nearest_ind = self.get_nearest_node_index(self.node_list, rnd_node)
            nearest_node = self.node_list[nearest_ind]

            new_node = self.steer(nearest_node, rnd_node, self.expand_dis)

            if self.check_collision_is_safe(new_node, self.obstacle_list):
                self.node_list.append(new_node)

            #if animation and i % 5 == 0:
            if animation:
                self.draw_graph(rnd_node)

            # 检查是否已经接近目标点，并尝试从最后一个节点到目标点进行扩展
            if self.calc_dist_to_goal(self.node_list[-1].x, self.node_list[-1].y) <= self.expand_dis:
                final_node = self.steer(self.node_list[-1], self.end, self.expand_dis)  # 若已经足够接近目标点，尝试从最后一个节点向目标点扩展
                if self.check_collision_is_safe(final_node, self.obstacle_list):
                    self.node_list.append(final_node)
                    return self.generate_final_course(len(self.node_list)-1)

        return None 

    def steer(self, from_node, to_node, extend_length=float("inf")):
        """
        extend the node list 扩展节点列表 / steer 驾驶(船、汽车等)；操纵；控制；引导；行驶
        从一个节点 (from_node) 开始，沿着方向指向另一个节点 (to_node) 进行扩展。
        扩展的长度受到限制，以防止超出指定的扩展距离。
        返回新的节点。
        """
        new_node = self.Node(from_node.x, from_node.y)
        # 计算起始节点到目标节点的距离和角度
        dis, theta = self.calc_distance_and_angle(new_node, to_node)

        new_node.path_x = [new_node.x]
        new_node.path_y = [new_node.y]

        # 如果指定的扩展长度大于节点间的距离，将扩展长度设为节点间的距离
        if extend_length > dis:
            extend_length = dis

        # 计算需要进行扩展的步数
        n_expand = math.floor(extend_length / self.path_resolution)

        # 通过一系列步进，将新节点沿着方向扩展
        # 通过这个循环，新节点在路径上沿着指定的方向逐步扩展，直到达到指定的扩展步数 n_expand。这样就生成了一系列节点，形成了路径的一部分
        for _ in range(n_expand):
            new_node.x += self.path_resolution * math.cos(theta)    # x 方向的增量
            new_node.y += self.path_resolution * math.sin(theta)
            new_node.path_x.append(new_node.x)  # 将新节点的 x 坐标加入路径 path_x 中，用于记录路径的 x 坐标
            new_node.path_y.append(new_node.y)

        # 检查是否距离目标节点小于等于路径分辨率
        d, _ = self.calc_distance_and_angle(new_node, to_node)
        if d <= self.path_resolution:
            # 如果是，将目标节点作为路径的一部分
            new_node.path_x.append(to_node.x)
            new_node.path_y.append(to_node.y)

        # 将起始节点设为新节点的父节点
        new_node.parent = from_node

        return new_node

    def generate_final_course(self, goal_ind):
        """
        生成最终路径
        从树中的最后一个节点开始，沿着父节点指针生成最终路径。  
        """
        path = [[self.end.x, self.end.y]]
        node = self.node_list[goal_ind]
        while node.parent is not None:
            path.append([node.x, node.y])
            node = node.parent
        path.append([node.x, node.y])

        return path

    def calc_dist_to_goal(self, x, y):
        """
        计算当前位置到目标的距离
        """
        dx = x - self.end.x
        dy = y - self.end.y
        return math.hypot(dx, dy)

    def get_random_node(self):
        """
        在搜索空间中获取随机节点 随机采样一个节点
        """
        if random.randint(0, 100) > self.goal_sample_rate:  # 采样一个普通的节点
            rnd = self.Node(random.uniform(self.min_rand, self.max_rand),
                            random.uniform(self.min_rand, self.max_rand))
        else:  # goal point sampling   采样目标点。
            rnd = self.Node(self.end.x, self.end.y)
        return rnd  # 返回生成的随机节点 rnd。这个节点将被用于扩展当前树的节点，从而构建RRT树。
    
    def draw_graph(self, rnd=None):
        """
        绘制RRT图形
        清空图形，连接esc键以停止模拟。
        如果提供了随机节点 (rnd)，则绘制该节点。
        遍历树中的节点，绘制父节点到当前节点的路径。
        绘制障碍物。
        绘制起点和终点。
        设置坐标轴的纵横比和刻度。
        暂停一段时间以允许图形显示。
        """
        plt.clf()
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect('key_release_event',
                                     lambda event: [exit(0) if event.key == 'escape' else None])
        if rnd is not None:
            plt.plot(rnd.x, rnd.y, "^k")

        # for node in self.node_list:
        #     if node.parent:
        #         plt.plot(node.path_x, node.path_y, "-g")

        # 通过使用 enumerate 函数遍历节点列表，并根据索引生成颜色，使得不同的路径具有不同的颜色
        for i, node in enumerate(self.node_list):
            if node.parent:
                color = (i / len(self.node_list), 1 - i / len(self.node_list), 0)  # 使用RGB颜色表示，根据节点索引生成不同的颜色
                plt.plot(node.path_x, node.path_y, color=color)

        for (ox, oy, size) in self.obstacle_list:
            self.plot_circle(ox, oy, size)

        plt.plot(self.start.x, self.start.y, "xr")  # "x" 表示使用 x 形状的标记，而 "r" 表示标记的颜色为红色（red）
        plt.plot(self.end.x, self.end.y, "xr")
        plt.axis("equal")   # 设置纵横比相等
        plt.axis([-20, 30, -20, 30]) # 图表XY轴的显示范围

        # 设置x轴和y轴上的刻度
        plt.xticks(np.arange(-10, 30, 2))  # x轴上的刻度。从-10开始，以步长2递增，不包括30
        plt.yticks(np.arange(-10, 30, 2))

        plt.grid(True)
        plt.pause(1.2) # 每次绘制图形后短暂地停顿

    @staticmethod
    def plot_circle(x, y, size, color="-b"):  # pragma: no cover
        deg = list(range(0, 360, 5))
        deg.append(0)
        xl = [x + size * math.cos(np.deg2rad(d)) for d in deg]
        yl = [y + size * math.sin(np.deg2rad(d)) for d in deg]
        plt.plot(xl, yl, color)

    @staticmethod
    def get_nearest_node_index(node_list, rnd_node):
        """
        找到在节点列表 node_list 中与随机节点 rnd_node 距离最近的节点，并返回该节点的索引。
        """
        dlist = [(node.x - rnd_node.x) ** 2 + (node.y - rnd_node.y)
                 ** 2 for node in node_list]
        minind = dlist.index(min(dlist))

        return minind

    @staticmethod
    def check_collision_is_safe(node, obstacleList):
        """用于检查给定节点的路径是否与障碍物发生碰撞。"""
        if node is None:
            return False

        for (ox, oy, sz) in obstacleList:
            dx_list = [ox - x for x in node.path_x] # 每个路径点与障碍物中心的 x 距离
            dy_list = [oy - y for y in node.path_y]
            d_list = [dx * dx + dy * dy for (dx, dy) in zip(dx_list, dy_list)]  # 每个路径点与障碍物中心的欧氏距离的平方

            if min(d_list) <= sz ** 2:
                return False  # collision

        return True  # safe 没有碰撞

    @staticmethod
    def calc_distance_and_angle(from_node, to_node):
        """
        计算两个节点之间的距离和角度的方法 
        """
        dx = to_node.x - from_node.x
        dy = to_node.y - from_node.y
        d = math.hypot(dx, dy)      # 两个节点之间的欧氏距离
        theta = math.atan2(dy, dx)  # 两个坐标之间的角度
        return d, theta


def main(gx=6.0, gy=10.0):
    # 阻碍物列表
    obstacleList = [
        (5, 5, 1),
        (3, 6, 2),
        (3, 8, 2),
        (3, 10, 2),
        (7, 5, 2),
        (9, 5, 2),
        (8, 10, 1),
        (16, 0, 3)
    ]  # [x, y, radius]

    rrt = RRT(start=[0, 0],
              goal=[gx, gy],
              rand_area=[-10, 30],
              obstacle_list=obstacleList)
    
    path = rrt.planning(animation=show_animation)

    if path is None:
        print("Cannot find path")
    else:
        print("found path!!")

        if show_animation:
            rrt.draw_graph()
            plt.plot([x for (x, y) in path], [y for (x, y) in path], '-r')
            plt.grid(True)
            plt.show()

# 主函数创建了一个 RRT 实例，并进行了路径规划。如果找到路径，则打印 "found path!!"，并在 Matplotlib 中显示路径和 RRT 树。            
if __name__ == '__main__':
    main()

