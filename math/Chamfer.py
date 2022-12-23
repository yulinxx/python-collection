# 已知AB， BC两条线段，且交于B点，求倒角半径为 L，AB，BC的倒角
# 以最短边（假定为AB）长 LAB，
# 在BC中，以B为起点，找出与LAB同长度的点D，
# 即BD的长度等于AB的长度
#
# (或 以B为圆心，LAB为半径， 绘制一个圆，
# 圆与AB交于A点， 于BC交于D点)
#
# 连接AD， 找出AD的中点P，
#
# 连接BP，
# 则BP为ABC夹角的角平分线
#
# 此时构成的 ABD,为一个等腰三角形
# 可轻松得出 垂直于BP的线， 到AB与BD的距离相等，即AP = PD
# 可样可用直角三角形法则得出 BP上的任意点，到AB的垂线，与到BC的垂线相等
# 即 XM = XN = L 圆弧半径
#
# 以X点作圆心，XM作半径，绘制圆，
# 该圆与AB， BC分别相切，
#
# 则圆弧 MN 则为AB与BC的倒角，倒角半径为L = XM
# ————————————————
# 版权声明：本文为CSDN博主「yulinxx」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/yulinxx/article/details/128415839

import numpy as np
import math

# 求单位向量
def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


# 角度
def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


# 点乘
def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))


# 叉乘

# 向量的长度
def length(v):
    return math.sqrt(dotproduct(v, v))


# 向量角度
def angle(v1, v2):
    return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


def funcChamfer(ptA, ptB, ptC, lR):
    # ABC点 组成的部分向量
    vBA = [ptA[0] - ptB[0], ptA[1] - ptB[1]]
    vBC = [ptC[0] - ptB[0], ptC[1] - ptB[1]]

    # 求ABC的夹角 (均当锐角处理)
    aABC = angle_between(vBA, vBC)
    # cABC = np.cross(vBA, vBC)
    # if(cABC < 0):   # 钝角
    #     aABC = math.pi * 2.0 - aABC
    print(f'ABC的夹角 Radius {aABC}, Angle:{180.0 / math.pi * aABC}')

    # 向量 BA BC的长度
    lBA = length(vBA)
    lBC = length(vBC)
    print(f'向量 BA BC的长度  lBA:{lBA}, lBC:{lBC}')

    # 获得 BA BC 最短边边长 lShort
    # 以及需要长边的端点 ptLast， 用于计算D点
    lShort = 0  # 存储 AB BC中， 短边的边长
    ptShortS = None  # 存储短边的起始点
    vShort = None  # 存储短边的向量
    vLong = None  # 存储长边的向量

    if lBA <= lBC:
        lShort = lBA
        ptShortS = ptA
        vShort = vBA
        vLong = vBC
    else:
        lShort = lBC
        ptShortS = ptC
        vShort = vBC
        vLong = lBA

    # --------------------求D点方式1(三角函数,复杂，仅做示范)：
    # 长轴和X轴的夹角
    vXAxis = [1, 0]
    vYAxis = [0, 1]

    aShort = angle_between(vXAxis, vShort)
    aLong = angle_between(vXAxis, vLong)
    print(f'短边和X轴的夹角: Radius: {aShort}, Angle:{180.0 / math.pi * aShort}')
    print(f'长边和X轴的夹角: Radius: {aLong}, Angle:{180.0 / math.pi * aLong}')

    testA = dotproduct(vLong, vXAxis)
    testB = dotproduct(vXAxis, vLong)

    testC = np.cross(vLong, vXAxis)
    testD = np.cross(vXAxis, vLong)

    testE = np.cross(vXAxis, vYAxis)
    testF = np.cross(vYAxis, vXAxis)
    print(f'-------Test {testA}, {testB}, {testC}, {testD}, {testE}, {testF}')

    ptD = []

    crossRes = np.cross(vXAxis, vLong)
    if crossRes < 0:
        aLong -= math.pi * 2

    ptD.append(ptB[0] + lShort * math.cos(aLong))
    ptD.append(ptB[1] + lShort * math.sin(aLong))
    print(f'point D:({ptD[0]}, {ptD[1]})')

    # --------------------求D点方式2(向量法）：
    # BC (长边）转单位向量：
    vNLong = unit_vector(vLong)
    x = [ptB[0], ptB[1]] + (vNLong * lShort)
    print(f'{vNLong}, ptD: {x}')

    # --------------------
    # AD点的中点P
    ptP = []
    ptP.append((ptD[0] + ptShortS[0]) * 0.5)
    ptP.append((ptD[1] + ptShortS[1]) * 0.5)
    print(f'point P:({ptP[0]}, {ptP[1]})')

    # BP向量
    vBP = [ptP[0] - ptB[0], ptP[1] - ptB[1]]

    # 假定点为 X， X到AB的垂线为 XM，且XM = lR
    # 角ABP度数为 ABC的一半， 已知角度与XM的长度，
    # 则可求出 BX 长度 lBX
    lBX = lR / math.sin(aABC * 0.5)

    ptX = ptB + unit_vector(vBP) * lBX
    print(f'ptX: {ptX}')
    return ptX


if __name__ == '__main__':
    # AB，BC两线段交于B点  A,B,C如下
    ptA = [707, 181]
    ptB = [850, 640]  # 公共点
    ptC = [1578, 167]

    lR = 130.0  # 倒角圆半径

    ptX = funcChamfer(ptA, ptB, ptC, lR)

    print(f'以此点: {ptX} 为圆心,绘制圆弧')

    # ----------------------------
    # 向量测试
    # 判断向量与X轴的夹角关系

    # 长轴和X轴的夹角

    # X Y 轴上的单位向量
    vX = [1, 0]
    vY = [0, 1]

    vA = [6, 6]
    vB = [-6, 6]
    vC = [-6, -6]
    vD = [6, -6]

    c1 = np.cross(vX, vA)  # 逆时针 45 度
    c2 = np.cross(vX, vB)  # 逆时针 90 + 45 度
    c3 = np.cross(vX, vC)  # 逆时针 180 + 45 度
    c4 = np.cross(vX, vD)  # 逆时针 270 + 45 度
    print(f'c1 {c1} c2 {c2}  c3 {c3} c4 {c4}')
    #       c1 6    c2 6     c3 -6    c4 -6

    d1 = np.dot(vX, vA)  # 逆时针 45 度
    d2 = np.dot(vX, vB)  # 逆时针 90 + 45 度
    d3 = np.dot(vX, vC)  # 逆时针 180 + 45 度
    d4 = np.dot(vX, vD)  # 逆时针 270 + 45 度
    print(f'd1 {d1} d2 {d2}  d3 {d3} d4 {d4}')
    #       d1  6   d2  -6   d3  -6  d4  6

    c5 = np.cross(vX, vY)  # X与Y垂直
    c6 = np.cross(vA, vD)  # 垂直
    c7 = np.cross(vA, vC)  # 共线，方向相反
    c8 = np.cross(vB, vD)  # 共线，方向相反
    print(f'c5 {c5} c6 {c6}  c7 {c7} c8 {c8}')
    #       c5  1   c6 -72   c7  0   c8  0

    d5 = np.dot(vX, vY)  # X与Y垂直
    d6 = np.dot(vA, vD)  # 垂直
    d7 = np.dot(vA, vC)  # 共线，方向相反
    d8 = np.dot(vB, vD)  # 共线，方向相反
    print(f'd5 {d5} d6 {d6}  d7 {d7} d8 {d8}')
    #       d5 0    d6   0   d7  -72 d8 -72

    dAD = np.dot(vA, vD)
    dDA = np.dot(vD, vA)
    print(f'dAD: {dAD}, dDA:{dDA}')

    cAD = np.cross(vA, vD)
    cDA = np.cross(vD, vA)
    print(f'cAD: {cAD}, cDA: {cDA}')
