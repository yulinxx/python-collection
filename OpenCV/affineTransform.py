



# https://zhuanlan.zhihu.com/p/36980767

# coding by 刘云飞
# email: liuyunfei.1314@163.com
# date: 2018-5-17

import cv2
import numpy as np

# 读取名称为 p18.png的图片
filePath = "E:/t.jpg"
img = cv2.imread(filePath, 1)
# img_org = cv2.imread(filePath, 1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

# 得到图片的高和宽
imgH, imgW = img.shape[:2]

# 定义对应的点
posOri = np.float32([
    [0, 0],
    [1024, 0],
    [1024, 700]
])
# posRes = np.float32([
#     [219, 0],
#     [1192, 323],
#     [975, 987]
# ])

# 切变
posRes = np.float32([
    [0, 0],
    [1024, 0],
    [1024 + 100, 700]
])

# X翻转
posRes = np.float32([
    [0, 700],
    [1024, 700],
    [1024, 0]
])
# Y翻转
posRes = np.float32([
    [1024, 0],
    [0, 0],
    [0, 700]
])

# Y翻转
posRes = np.float32([
    [1024, 0],
    [0, 0],
    [-443, 303]
])

posRes = np.float32([
    [1345, 497],
    [0, 0],
    [54, 560]
])
#
# cv2.circle(img_org, [0, 0], 15, (0, 0, 255), 4)
# cv2.circle(img_org, [1024, 0], 15, (0, 255, 0), 4)
# cv2.circle(img_org, [1024, 700], 15, (255, 0, 0), 4)

cv2.circle(img, [0, 0], 15, (0, 0, 255), 4)
cv2.circle(img, [1024, 0], 15, (0, 255, 0), 4)
cv2.circle(img, [1024, 700], 15, (255, 0, 0), 4)

# 变换矩阵M
M = cv2.getAffineTransform(posOri, posRes)

# 变换后的图像
# imgRes = cv2.warpAffine(img, M, (imgW * 2, imgH * 2), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
#                            borderValue=(255, 255, 255, 0))

imgRes = cv2.warpAffine(img, M, (imgW * 2, imgH * 2), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT,
                           borderValue=(0, 255, 255, 0.5))

cv2.rectangle(imgRes, [0, 0], [1024, 700], (255, 0, 255), 2, 8)

cv2.imwrite("D:/xx.png", imgRes)
# 显示原图和处理后的图像
# cv2.imshow("org", img_org)
cv2.imshow("imgRes", imgRes)

cv2.waitKey(0)
