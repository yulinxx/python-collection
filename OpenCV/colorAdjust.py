# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1


import numpy as np
import cv2


def main():
    # 加载图片 读取彩色图像
    image = cv2.imread('E:/img/p1.jfif', cv2.IMREAD_COLOR)
    # print(image)
    # cv2.imshow("image", image)

    # 图像归一化，且转换为浮点型
    fImg = image.astype(np.float32)
    fImg = fImg / 255.0
    # 颜色空间转换 BGR转为HLS
    hlsImg = cv2.cvtColor(fImg, cv2.COLOR_BGR2HLS)

    l = 100
    s = 100

    MAX_VALUE = 100

    # 调节饱和度和亮度的窗口
    cv2.namedWindow("l and s", cv2.WINDOW_AUTOSIZE)

    def nothing(*arg):
        pass

    # 滑动块
    cv2.createTrackbar("l", "l and s", l, MAX_VALUE, nothing)
    cv2.createTrackbar("s", "l and s", s, MAX_VALUE, nothing)

    # 调整饱和度和亮度后的效果
    lsImg = np.zeros(image.shape, np.float32)
    # 调整饱和度和亮度
    while True:
        # 复制
        hlsCopy = np.copy(hlsImg)
        # 得到 l 和 s 的值
        l = cv2.getTrackbarPos('l', 'l and s')
        s = cv2.getTrackbarPos('s', 'l and s')

        # 1.调整亮度（线性变换) , 2.将hlsCopy[:, :, 1]和hlsCopy[:, :, 2]中大于1的全部截取
        hlsCopy[:, :, 1] = (1.0 + l / float(MAX_VALUE)) * hlsCopy[:, :, 1]
        hlsCopy[:, :, 1][hlsCopy[:, :, 1] > 1] = 1

        # 饱和度
        hlsCopy[:, :, 2] = (1.0 + s / float(MAX_VALUE)) * hlsCopy[:, :, 2]
        hlsCopy[:, :, 2][hlsCopy[:, :, 2] > 1] = 1

        # HLS2BGR
        lsImg = cv2.cvtColor(hlsCopy, cv2.COLOR_HLS2BGR)

        # 显示调整后的效果
        cv2.imshow("l and s", lsImg)

        ch = cv2.waitKey(5)
        # 按 ESC 键退出
        if ch == 27:
            break
        elif ch == ord('s'):
            # 按 s 键保存并退出
            # 保存结果
            lsImg = lsImg * 255
            lsImg = lsImg.astype(np.uint8)
            cv2.imwrite("lsImg.jpg", lsImg)
            break

    # 关闭所有的窗口
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
