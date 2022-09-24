import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


# 封装图片显示函数
def image_show(image):
    if image.ndim == 2:
        plt.imshow(image, cmap='gray')
    else:
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        plt.imshow(image)
    plt.show()


if __name__ == '__main__':
    # 读取图像
    img = cv.imread('D:/april/Pictures/ab.jpg')

    # 定义错切变换矩阵
    para1 = -0.2  # 横坐标错切量
    para2 = -0.2  # 纵坐标错切量
    M = np.array([[1, para1, 0], [para2, 1, 0]], dtype=np.float32)

    # 图像的错切变换
    img_size = [1000, 1000]  # 输出图的范围
    img_cuts = cv.warpAffine(img, M, img_size)
    image_show(img_cuts)