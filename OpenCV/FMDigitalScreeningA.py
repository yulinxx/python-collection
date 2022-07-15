### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17
# 无序抖动算法
# 所谓的无序抖动，指的就是生成抖动矩阵的过程是无序随机的，
# 但是在计算机里一般使用的是伪随机的方法，
# 一般有平方取中法、乘同余发生器、素数模乘同余法、组合乘同余法等，但是都不能取得满意的效果，
# 其原因是无论怎样产生随机数，由于最大点距和最小点距不受控制，都有不规则聚集现象。
# 所以，纯理论的随机加网算法是行不通的。下面只展示两种伪随机的方法，仅仅只为看看效果~
#
# 全局伪随机抖动算法
# 算法公式
# 即抖动矩阵为图像大小，矩阵里的值全部使用伪随机生成。
# https://blog.csdn.net/sin_geek/article/details/45932145

from PIL import Image
import random

time = 8
K = 8
L = 8
N = 63
im = Image.open('E:/img/p1.jfif').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))

for y in range(im2.size[1]):
    k = y % K
    for x in range(im2.size[0]):
        l = x % L
        pix = int(im.getpixel((x / time, y / time)) / 255.0 * N + 0.5)
        if pix > random.randint(0, 64):
            im2.putpixel((x, y), 1)
        else:
            im2.putpixel((x, y), 0)
im2.save("E:/img/Dithering--FM_Random.png")
print('FM_Random End')
