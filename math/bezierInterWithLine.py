
#   计算贝塞尔曲线和直线的交点


import numpy as np

def intersect_bezier_line(pS, pCtrl1, pCtrl2, pE, pLineA, pLineB):
    """
    计算贝塞尔曲线和直线的交点。

    Args:
        pS: 贝塞尔曲线的起始控制点。
        pCtrl1: 贝塞尔曲线的第一个控制点。
        pCtrl2: 贝塞尔曲线的第二个控制点。
        pE: 贝塞尔曲线的终止控制点。
        pLineA: 直线的起始端点。
        pLineB: 直线的终止端点。

    Returns:
        交点的坐标。
    """

    # 将贝塞尔曲线参数化

    def f(t):
        return (1 - t)**3 * pS + 3 * (1 - t)**2 * t * pCtrl1 + 3 * (1 - t) * t**2 * pCtrl2 + t**3 * pE

    # 将直线参数化

    def g(t):
        return pLineA + t * (pLineB - pLineA)

    # 初始化交点的估计值

    t0 = 0.5

    # 迭代计算交点

    for _ in range(100):
        df = 3 * (1 - t0)**2 * (pCtrl1 - pS) + 6 * (1 - t0) * t0 * (pCtrl2 - pCtrl1) + 3 * t0**2 * (pE - pCtrl2)
        t1 = t0 - np.dot(f(t0) - g(t0), df) / np.linalg.norm(df)**2
        if abs(t1 - t0) < 1e-6:
            break
        t0 = t1

    # 计算交点的坐标

    x = f(t1)[0]
    y = f(t1)[1]

    return x, y

if __name__ == "__main__":
    # 定义贝塞尔曲线控制点和直线端点
    pS = np.array([0.0, 0.0])
    pCtrl1 = np.array([0.0, 0.0])
    pCtrl2 = np.array([50.0, 25.0])
    pE = np.array([50.0, 50.0])
    pLineA = np.array([0.0, 50.0])
    pLineB = np.array([50.0, 0.0])

    # 计算交点
    x, y = intersect_bezier_line(pS, pCtrl1, pCtrl2, pE, pLineA, pLineB)
    
    #  30.05288789017335 19.602556549487936
    print("交点的坐标为：", x, y)
