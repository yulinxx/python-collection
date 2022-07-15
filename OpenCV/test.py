# 数据增强（噪声，模糊，缩放，色域变换，均衡化，色彩抖动）_小谭爱学习的博客-CSDN博客_数据增强 色彩抖动
# https://blog.csdn.net/qq_52050692/article/details/119698239
# 已有：翻转，色域变换，噪声，大小改变，模糊，色彩抖动，均衡化
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
import os
import random


# 限制对比度自适应直方图均衡
def clahe(image):
    b, g, r = cv2.split(image)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    b = clahe.apply(b)
    g = clahe.apply(g)
    r = clahe.apply(r)
    image_clahe = cv2.merge([b, g, r])
    return image_clahe


# 伽马变换
def gamma(image):
    fgamma = 2
    image_gamma = np.uint8(np.power((np.array(image) / 255.0), fgamma) * 255.0)
    cv2.normalize(image_gamma, image_gamma, 0, 255, cv2.NORM_MINMAX)
    cv2.convertScaleAbs(image_gamma, image_gamma)
    return image_gamma


# 直方图均衡
def hist(image):
    r, g, b = cv2.split(image)
    r1 = cv2.equalizeHist(r)
    g1 = cv2.equalizeHist(g)
    b1 = cv2.equalizeHist(b)
    image_equal_clo = cv2.merge([r1, g1, b1])
    return image_equal_clo


# 噪声在图像上常表现为一引起较强视觉效果的孤立像素点或像素块。一般，噪声信号与要研究的对象不相关，它以无用的信息形式出现，扰乱图像的可观测信息。通俗的说就是噪声让图像不清楚。
# 椒盐噪声，也称为脉冲噪声，成因可能是影像讯号受到突如其来的强烈干扰而产生、类比数位转换器或位元传输错误等。例如失效的感应器导致像素值为最小值，饱和的感应器导致像素值为最大值
# 噪声来源—两个方面
# （1）图像获取过程中
# 两种常用类型的图像传感器CCD和CMOS采集图像过程中，由于受传感器材料属性、工作环境、电子元器件和电路结构等影响，会引入各种噪声，如电阻引起的热噪声、场效应管的沟道热噪声、光子噪声、暗电流噪声、光响应非均匀性噪声。
#
# （2）图像信号传输过程中
# 由于传输介质和记录设备等的不完善，数字图像在其传输记录过程中往往会受到多种噪声的污染。另外，在图像处理的某些环节当输入的对象并不如预想时也会在结果图像中引入噪声。

# 椒盐噪声
# 椒盐噪声英文名叫salt and pepper noise，也就是盐和胡椒噪声。在分类上分为盐噪声和胡椒噪声。其实就是图像中随机的一些像素为黑色（0）或者白色（255）。
# 其中盐噪声又称白噪声，是在图像中添加一些随机的白色像素点（255），想象一下盐的白色。
# 胡椒噪声则是在图像中添加一些随机的黑色像素点（0），想象一下胡椒的黑色。

def sp_noise(image):
    output = np.zeros(image.shape, np.uint8)
    prob = rand(0.0005, 0.001)
    thres = 1 - prob

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0  # 椒噪声
            elif rdn > thres:
                output[i][j] = 255  # 盐噪声
            else:
                output[i][j] = image[i][j]
    return output


def gasuss_noise(image, mean=0, var=0.001):
    """
        添加高斯噪声
        image:原始图像
        mean : 均值
        var : 方差,越大，噪声越大
    """
    image = np.array(image / 255, dtype=float)  # 将原始图像的像素值进行归一化，除以255使得像素值在0-1之间
    noise = np.random.normal(mean, var ** 0.5, image.shape)  # 创建一个均值为mean，方差为var呈高斯分布的图像矩阵
    out = image + noise  # 将噪声和原始图像进行相加得到加噪后的图像
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)  # clip函数将元素的大小限制在了low_clip和1之间了，小于的用low_clip代替，大于1的用1代替
    out = np.uint8(out * 255)  # 解除归一化，乘以255将加噪后的图像的像素值恢复
    noise = noise * 255
    return [noise, out]


def random_noise(image, noise_num):
    """
    添加随机噪点（实际上就是随机在图像上将像素点的灰度值变为255即白色）
    :param image: 需要加噪的图片
    :param noise_num: 添加的噪音点数目，一般是上千级别的
    :return: img_noise
    """
    #
    # 参数image：，noise_num：
    img_noise = image
    # cv2.imshow("src", img)
    rows, cols, chn = img_noise.shape
    # 加噪声
    for i in range(noise_num):
        x = np.random.randint(0, rows)  # 随机生成指定范围的整数
        y = np.random.randint(0, cols)
        img_noise[x, y, :] = 255
    return img_noise


# 色彩抖动
def randomColor(image):
    saturation = random.randint(0, 1)
    brightness = random.randint(0, 1)
    contrast = random.randint(0, 1)
    sharpness = random.randint(0, 1)

    if random.random() < saturation:
        random_factor = np.random.randint(0, 31) / 10.  # 随机因子
        image = ImageEnhance.Color(image).enhance(random_factor)  # 调整图像的饱和度

    if random.random() < brightness:
        random_factor = np.random.randint(10, 21) / 10.  # 随机因子
        image = ImageEnhance.Brightness(image).enhance(random_factor)  # 调整图像的亮度

    if random.random() < contrast:
        random_factor = np.random.randint(10, 21) / 10.  # 随机因1子
        image = ImageEnhance.Contrast(image).enhance(random_factor)  # 调整图像对比度

    if random.random() < sharpness:
        random_factor = np.random.randint(0, 31) / 10.  # 随机因子
        ImageEnhance.Sharpness(image).enhance(random_factor)  # 调整图像锐度

    return image


def rand(a=0, b=1):
    return np.random.rand() * (b - a) + a


def get_data(image, input_shape=[200, 200], random=True, jitter=.5, hue=.1, sat=1.5, val=1.5, proc_img=True):
    iw, ih = image.size
    h, w = input_shape

    # 对图像进行缩放并且进行长和宽的扭曲
    # new_ar = w / h * rand(1 - jitter, 1 + jitter) / rand(1 - jitter, 1 + jitter)
    # scale = rand(.15, 2.5)
    # if new_ar < 1:
    #     nh = int(scale * h)
    #     nw = int(nh * new_ar)
    # else:
    #     nw = int(scale * w)
    #     nh = int(nw / new_ar)
    #     image = image.resize((nw, nh), Image.BICUBIC)

    # 翻转图像
    flip = rand() < .5
    if flip:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)

    # 噪声或者虚化，二选一
    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    a1 = np.random.randint(0, 3)
    if a1 == 0:
        image = sp_noise(image)
    elif a1 == 1:
        image = cv2.GaussianBlur(image, (5, 5), 0)
    else:
        image = image
    # 均衡化
    index_noise = np.random.randint(0, 10)
    print(index_noise)
    if index_noise == 0:
        image = hist(image)
        print('hist,done')
    elif index_noise == 1:
        image = clahe(image)
        print('clahe,done')
    elif index_noise == 2:
        image = gamma(image)
        print('gamma,done')
    else:
        image = image

    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # 色彩抖动
    image = randomColor(image)
    print(image.size)
    # 色域扭曲
    hue = rand(-hue, hue)
    sat = rand(1, sat) if rand() < .5 else 1 / rand(1, sat)
    val = rand(1, val) if rand() < .5 else 1 / rand(1, val)
    x = rgb_to_hsv(np.array(image) / 255.)
    x[..., 0] += hue
    x[..., 0][x[..., 0] > 1] -= 1
    x[..., 0][x[..., 0] < 0] += 1
    x[..., 1] *= sat
    x[..., 2] *= val
    x[x > 1] = 1
    x[x < 0] = 0
    image_data = hsv_to_rgb(x)

    image_data = np.array(image)
    return image_data


if __name__ == "__main__":
    # 图像批量处理
    # dirs = 'F:/ 3/'  # 原始图像所在的文件夹
    # dets = './class_pic3/dets/407_3/'  # 图像增强后存放的文件夹
    # mylist = os.listdir(dirs)
    # l = len(mylist)  # 文件夹图片的数量
    # for j in range(0, l):
    #     image = cv2.imread(dirs + mylist[j])
    #     img = Image.fromarray(np.uint8(image))
    #     for i in range(0, 2):  # 自定义增强的张数
    #         img_ret = get_data(img)
    #         # imwrite(存入图片路径+图片名称+‘.jpg’,img)
    #         # 注意：名称应该是变化的，不然会覆盖原来的图片
    #         cv2.imwrite(dets + '1' + str(j) + '0' + str(i) + '.jpg', img_ret)
    #         print('done')

    # 单个图像处理

    image = cv2.imread("F:/a.jpg")
    # matRest = randomColor(image)
    # matRest = random_noise(image, 123)
    noise, matRest = gasuss_noise(image)
    cv2.imshow('noise', noise)
    cv2.imshow('res', matRest)

    cv2.waitKey()
    # img = Image.fromarray(np.uint8(image))
    # for i in range(0,4):
    #   img_ret=get_data(img)
    #   cv2.imwrite('F:/111.jpg', img_ret)
    #   print('done')
