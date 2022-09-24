import math
import numpy as np
import cv2


#
# # 数字图像处理-python基于opencv代码实现 反转变换、对数变换和幂律(伽马)变换_心是蓝图的博客-CSDN博客_对数变换
# # https://blog.csdn.net/qq_42505705/article/details/86759446
#
# def gammaTranform(c, gamma, image):
#     h, w, d = image.shape[0], image.shape[1], image.shape[2]
#     new_img = np.zeros((h, w, d), dtype=np.float32)
#     for i in range(h):
#         for j in range(w):
#             new_img[i, j, 0] = c * math.pow(image[i, j, 0], gamma)
#             new_img[i, j, 1] = c * math.pow(image[i, j, 1], gamma)
#             new_img[i, j, 2] = c * math.pow(image[i, j, 2], gamma)
#     cv2.normalize(new_img, new_img, 0, 255, cv2.NORM_MINMAX)
#     new_img = cv2.convertScaleAbs(new_img)
#
#     return new_img
#
#
# img = cv2.imread(r'F:/img/a.jpg', 1)
#
# new_img = gammaTranform(1, 0.5, img)
#
# cv2.imshow('x', new_img)
# cv2.waitKey(0)



# OpenCV-对比度增强（伽马变换）-python黑洞网 C++ PY
# https://www.pythonheidong.com/blog/article/277217/c3026e392b3652ea2aab/

import cv2 as cv
import numpy as np

#
# ##读取图像
# img = cv.imread('F:/img/a.jpg')
# cv.imshow("original image",img)
# ##读取图像高宽和通道数
# height,width,channel=img.shape
# ##初始化空白图像和系数
# gamma_image=np.zeros(img.shape,dtype=np.float64)
# #图像归一化和伽马系数
# src=img/255.0
# gamma=0.5
#
#
# for r in range(height):
#     for c in range(width):
#         B = src[r, c][0]
#         G = src[r, c][1]
#         R = src[r, c][2]
#         gamma_image[r ,c][0] = np.power(B,gamma)
#         gamma_image[r, c][1] = np.power(G,gamma)
#         gamma_image[r, c][2] = np.power(R,gamma)
#
#
# cv.imshow("gamma image",gamma_image)
# cv.waitKey(0)
# cv.destroyAllWindows()



# Apply Gamma Correction to an Image using OpenCV | Lindevs
# https://lindevs.com/apply-gamma-correction-to-an-image-using-opencv/

import cv2
import numpy as np


def gammaCorrection(src, gamma):
    invGamma = 1 / gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(src, table)


img = cv2.imread('F:/img/a.jpg')
gammaImg = gammaCorrection(img, 2.2)

cv2.imshow('Original image', img)
cv2.imshow('Gamma corrected image', gammaImg)
cv2.waitKey(0)
cv2.destroyAllWindows()