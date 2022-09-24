# import cv2 as cv
# https://zhuanlan.zhihu.com/p/113397988
# #Scharr算子(Sobel算子的增强版，效果更突出)
#
# def Scharr_demo(image):
#     grad_x = cv.Scharr(image, cv.CV_32F, 1, 0)   #对x求一阶导
#     grad_y = cv.Scharr(image, cv.CV_32F, 0, 1)   #对y求一阶导
#     gradx = cv.convertScaleAbs(grad_x)  #用convertScaleAbs()函数将其转回原来的uint8形式
#     grady = cv.convertScaleAbs(grad_y)
#     cv.imshow("gradient_x", gradx)  #x方向上的梯度
#     cv.imshow("gradient_y", grady)  #y方向上的梯度
#     gradxy = cv.addWeighted(gradx, 0.5, grady, 0.5, 0)
#     cv.imshow("gradient", gradxy)
#
# src = cv.imread('F:/img/test.png')
# cv.namedWindow('input_image', cv.WINDOW_NORMAL) #设置为WINDOW_NORMAL可以任意缩放
# cv.imshow('input_image', src)
# Scharr_demo(src)
# cv.waitKey(0)
# cv.destroyAllWindows()
#


# import cv2 as cv
#
# #拉普拉斯算子
# def Laplace_demo(image):
#     dst = cv.Laplacian(image, cv.CV_32F)
#     lpls = cv.convertScaleAbs(dst)
#     cv.imshow("Laplace_demo", lpls)
# src = cv.imread('F:/img/test.png')
#
# cv.namedWindow('input_image', cv.WINDOW_NORMAL) #设置为WINDOW_NORMAL可以任意缩放
# cv.imshow('input_image', src)
# Laplace_demo(src)
# cv.waitKey(0)
# cv.destroyAllWindows()


### edge.py
import numpy as np
import math


def conv(image, kernel):
    """卷积的一个实现.

    对于任意一个像素点，该本版采用了点积运算以及 np.sum()来进行快速的加权求和

    Args:
        图像: 尺寸为(Hi, Wi)的numpy数组.
        卷积核(kernel): 尺寸为(Hk, Wk)的numpy数组.

    Returns:
        out: 尺寸为(Hi, Wi)的numpy数组.
    """
    Hi, Wi = image.shape
    Hk, Wk = kernel.shape
    out = np.zeros((Hi, Wi))

    # 对于本次作业, 我们将使用边界值来对图像进行填充.
    # 这是因为，如果使用0进行填充，会使得在图像边界上的导数非常大,
    # 但通常而言，我们希望忽略图像边界上的边缘（图像边界永远不会被认为是边缘）.
    pad_width0 = Hk // 2
    pad_width1 = Wk // 2
    pad_width = ((pad_width0, pad_width0), (pad_width1, pad_width1))
    padded = np.pad(image, pad_width, mode='edge')

    ### YOUR CODE HERE
    for i in range(Hi):
        for j in range(Wi):
            out[i][j] = (padded[i:i + Hk, j:j + Wk] * kernel).sum()
    ### END YOUR CODE

    return out


def gaussian_kernel(size, sigma):
    """ 生成高斯卷积核.

    该函数按照高斯核的公式，生成了一个卷积核矩阵。

    提示:
    - 利用 np.pi 以及 np.exp 当计算 pi 以及 exp()函数.

    参数:
        size: 一个整数，表示输出的kernel的尺寸.
        sigma: 一个float，对应于高斯公式中的sigma，用来控制权重的分配.

    返回值:
        kernel: 尺寸为(size, size)的numpy数组.
    """

    kernel = np.zeros((size, size))

    ### YOUR CODE HERE
    k = (size - 1) / 2
    for i in range(size):
        for j in range(size):
            kernel[i][j] = 1 / (2 * np.pi * sigma ** 2) * np.exp(((i - k) ** 2 + (j - k) ** 2) / (-2 * sigma ** 2))
            # kenel[i][j]=1/(2*np.pi*power(sigma,2))*np.exp(((power(i-k,2)+(power(j-k,2))/(-2*power(sigma,2)))
    ### END YOUR CODE

    return kernel


def partial_x(img):
    """ 计算输入图像水平方向的偏导.

    提示:
        - 你可以利用你在前面完成的conv函数.

    参数:
        img: 尺寸为(Hi, Wi)的numpy数组.
    输出:
        out: 水平方向的梯度图像
    """

    Hi, Wi = img.shape
    out = None
    padded = np.pad(img, 1, mode='edge')
    padded1 = np.zeros(padded.shape)
    ### YOUR CODE HERE
    for i in range(1, Hi + 1):
        for j in range(1, Wi + 1):
            padded1[i][j] = (padded[i][j + 1] - padded[i][j - 1]) / 2
    ### END YOUR CODE
    out = padded1[1:Hi + 1, 1:Wi + 1]
    return out


def partial_y(img):
    """ 计算输入图像竖直方向的偏导.

    提示:
        - 你可以利用你在前面完成的conv函数/或者用前面刚开发的partial_x函数.

    参数:
        img: 尺寸为(Hi, Wi)的numpy数组.
    输出:
        out: 竖直方向的梯度图像
    """
    Hi, Wi = img.shape
    out = None
    padded = np.pad(img, 1, mode='edge')
    padded1 = np.zeros(padded.shape)
    ### YOUR CODE HERE
    for i in range(1, Hi + 1):
        for j in range(1, Wi + 1):
            padded1[i][j] = (padded[i + 1][j] - padded[i - 1][j]) / 2
    ### END YOUR CODE
    out = padded1[1:Hi + 1, 1:Wi + 1]
    return out


def gradient(img):
    """ 计算输入图像的梯度大小和方向.

    参数:
        img: 灰度图. 尺寸为 (H, W) 的Numpy数组.

    返回值:
        G: 输入图像的梯度值图像。它的每个像素点值都是该像素点的梯度值.
            尺寸为 (H, W) 的Numpy数组.
        theta: 输入图像的梯度方向图像(角度, 0 <= theta < 360)，每个像素点都代表该像素点的梯度方向.
            尺寸为 (H, W) 的Numpy数组.

    提示:
        - 可以使用 np.sqrt 以及 np.arctan2 来计算平方根以及反正切值
    """
    Hi, Wi = img.shape
    G = np.zeros(img.shape)
    theta = np.zeros(img.shape)
    outx = partial_x(img)
    outy = partial_y(img)
    ### YOUR CODE HERE
    for i in range(Hi):
        for j in range(Wi):
            G[i][j] = np.sqrt(outx[i][j] ** 2 + outy[i][j] ** 2)
    for i in range(Hi):
        for j in range(Wi):
            theta[i][j] = np.arctan2(outy[i][j], outx[i][j]) * 180 / np.pi
            if theta[i][j] < 0:
                theta[i][j] = theta[i][j] + 360
            if theta[i][j] > 360:
                theta[i][j] = theta[i][j] - 360
    ### END YOUR CODE

    return G, theta


def non_maximum_suppression(G, theta):
    """ 实现非极大值抑制

    对于任意一个像素点，该函数都完成了在梯度方向上(theta)的非极大值抑制

    参数:
        G: 梯度幅值图像，尺寸为 (H, W)的Numpy数组.
        theta: 梯度方向图像，尺寸为 (H, W)的Numpy数组.

    Returns:
        out: 非极大值抑制以后的图像。如果像素点不是局部极大值点，则置0，否则保留原梯度幅值.
    """
    padded = np.pad(G, 1, mode='edge')
    H, W = G.shape
    out = np.zeros((H, W))

    # 将梯度方向round到最近的45°上来
    theta = np.floor((theta + 22.5) / 45) * 45
    ### BEGIN YOUR CODE
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            thetaij = theta[i - 1][j - 1]
            if thetaij == 45:
                if padded[i][j] > padded[i + 1][j + 1] and padded[i][j] > padded[i - 1][j - 1]:
                    out[i - 1][j - 1] = padded[i][j]
                else:
                    out[i - 1][j - 1] = 0
            if thetaij == 225:
                if padded[i][j] > padded[i + 1][j + 1] and padded[i][j] > padded[i - 1][j - 1]:
                    out[i - 1][j - 1] = padded[i][j]
                else:
                    out[i - 1][j - 1] = 0

            if thetaij == 90:
                if padded[i][j] > padded[i + 1][j] and padded[i][j] > padded[i - 1][j]:
                    out[i - 1][j - 1] = padded[i][j]
                else:
                    out[i - 1][j - 1] = 0
            if thetaij == 270:
                if padded[i][j] > padded[i + 1][j] and padded[i][j] > padded[i - 1][j]:
                    out[i - 1][j - 1] = padded[i][j]
                else:
                    out[i - 1][j - 1] = 0

            if thetaij == 135:
                if padded[i][j] > padded[i - 1][j + 1] and padded[i][j] > padded[i + 1][j - 1]:
                    out[i - 1][j - 1] = padded[i][j]
                else:
                    out[i - 1][j - 1] = 0
            if thetaij == 315:
                if padded[i][j] > padded[i - 1][j + 1] and padded[i][j] > padded[i + 1][j - 1]:
                    out[i - 1][j - 1] = padded[i][j]
                else:
                    out[i - 1][j - 1] = 0

            if thetaij == 0:
                if padded[i][j] > padded[i][j - 1] and padded[i][j] > padded[i][j + 1]:
                    out[i - 1][j - 1] = padded[i][j]
                else:
                    out[i - 1][j - 1] = 0
            if thetaij == 180:
                if padded[i][j] > padded[i][j - 1] and padded[i][j] > padded[i][j + 1]:
                    out[i - 1][j - 1] = padded[i][j]
                else:
                    out[i - 1][j - 1] = 0
            if thetaij == 360:
                if padded[i][j] > padded[i][j - 1] and padded[i][j] > padded[i][j + 1]:
                    out[i - 1][j - 1] = padded[i][j]
                else:
                    out[i - 1][j - 1] = 0
    ### END YOUR CODE

    return out


def double_thresholding(img, high, low):
    """
    参数:
        img: 非极大值抑制以后的梯度幅值图像.
        high: 对于强边缘(strong edge)而言的高阈值.
        low: 对于弱边缘(strong edge)而言的高阈值.

    返回值:
        strong_edges: 布尔类型的数组，代表强边缘。
            强边缘指的是梯度的幅值大于高阈值的像素点
        弱边缘: 布尔类型的数组，代表弱边缘。
            强边缘指的是梯度的幅值小于或者等于高阈值，并且大于低阈值的像素点。
    """

    strong_edges = np.zeros(img.shape, dtype=np.bool)
    weak_edges = np.zeros(img.shape, dtype=np.bool)
    H, W = img.shape
    ### YOUR CODE HERE
    for i in range(H):
        for j in range(W):
            if img[i][j] > high:
                strong_edges[i][j] = img[i][j]
            if img[i][j] <= high and img[i][j] > low:
                weak_edges[i][j] = img[i][j]

    ### END YOUR CODE

    return strong_edges, weak_edges


def get_neighbors(y, x, H, W):
    """ 返回坐标为 (y, x) 的像素点点的邻居(neighbor).

    对于一幅尺寸为(H, W)的图像，返回像素点 (y, x) 的邻居的所有有效索引.
    一个有效的索引 (i, j) 应该满足:
        1. i >= 0 and i < H
        2. j >= 0 and j < W
        3. (i, j) != (y, x)

    参数:
        y, x: 像素点的位置
        H, W: 图像的尺寸
    返回值:
        neighbors: 该像素点的邻居的索引值[(i, j)]所组成的list .
    """
    neighbors = []

    for i in (y - 1, y, y + 1):
        for j in (x - 1, x, x + 1):
            if i >= 0 and i < H and j >= 0 and j < W:
                if (i == y and j == x):
                    continue
                neighbors.append((i, j))

    return neighbors


def link_edges(strong_edges, weak_edges):
    """ 找出与真实的边缘相连接的弱边缘，并将它们连接到一起.

    对于每个强边缘点，它们都是真实的边缘。
    我们需要遍历每个真实的边缘点，然后在弱边缘中找出与之相邻的像素点，并把他们连接起来。
    在这里，我们认为如果像素点(a, b)与像素点(c, d)相连，只要(a, b)位于(c, d)的八邻域内。

    Args:
        strong_edges: 尺寸为 (H, W)的二值图像.
        weak_edges: 尺寸为 (H, W)的二值图像.

    Returns:
        edges: 尺寸为 (H, W)的二值图像.

    提示：
        弱边缘一旦与强边缘相连，那它就是真实的边缘，与强边缘的地位一样。
        这句话的意思是，一旦一个弱边缘像素点被检测成为了一个真实的边缘点，所有与它相连的其它弱边缘也应该被归为真实的边缘。
        所以在编程的时候，你只遍历一遍强边缘是不够的，因为此时可能有新的弱边缘点被标记为真实的边缘点。
    """

    H, W = strong_edges.shape
    indices = np.stack(np.nonzero(strong_edges)).T
    edges = np.zeros((H, W), dtype=np.bool)

    # 生成新的拷贝
    weak_edges = np.copy(weak_edges)
    edges = np.copy(strong_edges)
    g = 0;
    padded_weak = np.pad(weak_edges, 1, mode='edge')
    edges1 = np.pad(strong_edges, 1, mode='edge')
    ### YOUR CODE HERE
    while (g != -1):
        g = 0;
        k = 0;
        for i in range(H):
            for j in range(W):
                # if strong_edges[i][j]!=0:
                if edges1[i + 1][j + 1] != 0:
                    if padded_weak[i][j] != 0 and edges1[i][j] != padded_weak[i][j]:
                        edges1[i][j] = padded_weak[i][j]
                        k = k + 1
                    if padded_weak[i][j + 1] != 0 and edges1[i][j + 1] != padded_weak[i][j + 1]:
                        edges1[i][j + 1] = padded_weak[i][j + 1]
                        k = k + 1
                    if padded_weak[i][j + 2] != 0 and edges1[i][j + 2] != padded_weak[i][j + 2]:
                        edges1[i][j + 2] = padded_weak[i][j + 2]
                        k = k + 1

                    if padded_weak[i + 1][j] != 0 and edges1[i + 1][j] != padded_weak[i + 1][j]:
                        edges1[i + 1][j] = padded_weak[i + 1][j]
                        k = k + 1
                    if padded_weak[i + 1][j + 2] != 0 and edges1[i + 1][j + 2] != padded_weak[i + 1][j + 2]:
                        edges1[i + 1][j + 2] = padded_weak[i + 1][j + 2]
                        k = k + 1

                    if padded_weak[i + 2][j] != 0 and edges1[i + 2][j] != padded_weak[i + 2][j]:
                        edges1[i + 2][j] = padded_weak[i + 2][j]
                        k = k + 1
                    if padded_weak[i + 2][j + 1] != 0 and edges1[i + 2][j + 1] != padded_weak[i + 2][j + 1]:
                        edges1[i + 2][j + 1] = padded_weak[i + 2][j + 1]
                        k = k + 1
                    if padded_weak[i + 2][j + 2] != 0 and edges1[i + 2][j + 2] != padded_weak[i + 2][j + 2]:
                        edges1[i + 2][j + 2] = padded_weak[i + 2][j + 2]
                        k = k + 1
        if k == 0:
            g = -1;
        else:
            strong_egdes = np.copy(edges1[1:H + 1, 1:W + 1])

    edges = edges1[1:H + 1, 1:W + 1]

    ### END YOUR CODE

    return edges


def canny(img, kernel_size=5, sigma=1.4, high=20, low=15):
    """ 将上面所完成的函数组合到一起，完成canny边缘检测器.

    Args:
        img: 输入图像
        kernel_size: int， 表示kernel的大小
        sigma: float, 用来计算kernel.
        high: 为强边缘而设的高阈值.
        low: 为弱边缘而设的低阈值.
    Returns:
        edge: 输出的边缘图像
    """
    ### YOUR CODE HERE

    kernel = gaussian_kernel(kernel_size, sigma)
    smoothed = conv(img, kernel)
    G, theta = gradient(smoothed)
    nms = non_maximum_suppression(G, theta)
    strong_edges, weak_edges = double_thresholding(nms, high, low)
    edge = link_edges(strong_edges, weak_edges)

    ### END YOUR CODE

    return edge


