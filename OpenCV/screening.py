########################################################################
# ### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 12
K = 12
L = 12
N = 144

# L: 8位像素，黑白 每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
im = Image.open('F:/img/test.png').convert('L')

im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))

Mask = [144, 140, 132, 122, 107, 63, 54, 93, 106, 123, 133, 142,
        143, 137, 128, 104, 94, 41, 31, 65, 98, 116, 120, 139,
        135, 131, 114, 97, 61, 35, 24, 55, 80, 103, 113, 125,
        126, 117, 88, 83, 56, 29, 15, 51, 68, 90, 99, 111,
        109, 100, 81, 77, 48, 22, 8, 28, 47, 76, 85, 96,
        91, 44, 16, 12, 9, 3, 5, 21, 25, 33, 37, 73,
        59, 58, 30, 18, 10, 1, 2, 4, 11, 19, 34, 42,
        92, 64, 57, 52, 26, 6, 7, 14, 32, 46, 53, 74,
        101, 95, 70, 67, 38, 13, 20, 36, 50, 75, 82, 108,
        121, 110, 86, 78, 45, 17, 27, 39, 69, 79, 102, 119,
        134, 129, 112, 89, 49, 23, 43, 60, 71, 87, 115, 127,
        141, 138, 124, 118, 66, 40, 62, 72, 84, 105, 130, 136]

for m in range(im2.size[1]):
    k = m % K
    for n in range(im2.size[0]):
        l = n % L
        a = m / time
        b = n / time
        try:
            pix = int(im.getpixel((m / time, n / time)) / 255.0 * N + 0.5)
        except:
            continue

        if pix > Mask[k * L + l]:
            im2.putpixel((m, n), 1)
        else:
            im2.putpixel((m, n), 0)
im2.save("AM0.bmp")

########################################################################
# 15度加网算法
### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 12
K = 3
L = 51
N = 153
q = 4
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))

Mask = [153, 148, 120, 77, 53, 28, 26, 60, 87, 122, 131, 135, 132, 124, 116, 104, 73, 47, 23, 6, 56, 66, 85, 57, 51, 39,
        19, 8, 15, 2, 7, 17, 55, 79, 83, 99, 102, 109, 112, 117, 105, 74, 54, 14, 24, 64, 84, 121, 137, 142, 150,
        145, 139, 101, 69, 48, 11, 34, 68, 100, 128, 138, 143, 147, 141, 125, 97, 71, 43, 13, 30, 62, 90, 107, 110, 96,
        91,
        76, 52, 27, 20, 5, 4, 21, 25, 37, 45, 82, 92, 94, 95, 98, 63, 41, 1, 38, 67, 89, 127, 134, 140, 149,
        136, 126, 88, 59, 31, 12, 46, 75, 114, 130, 146, 151, 152, 144, 136, 86, 61, 40, 18, 49, 70, 103, 119, 123, 115,
        111,
        108, 93, 80, 65, 36, 3, 22, 50, 35, 9, 16, 32, 44, 81, 78, 58, 29, 10, 42, 72, 106, 113, 118, 129, 133]

for m in range(im2.size[1]):
    k = m % K
    t = L - (q * K * (m / K)) % L
    for n in range(im2.size[0]):
        l = (n % L + t) % L
        pix = int(im.getpixel((m / time, n / time)) / 255.0 * N + 0.5)
        if pix > Mask[k * L + l]:
            im2.putpixel((m, n), 1)
        else:
            im2.putpixel((m, n), 0)
im2.save("AM15.bmp")

########################################################################

# 45度加网算法

### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 12
K = 8
L = 16
N = 128
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))

Mask = [128, 120, 109, 92, 74, 66, 46, 8, 15, 10, 64, 79, 97, 111, 122, 127,
        123, 116, 87, 69, 62, 38, 6, 39, 42, 3, 19, 55, 86, 105, 115, 119,
        107, 96, 71, 59, 24, 12, 28, 52, 63, 47, 20, 1, 58, 95, 108, 112,
        84, 73, 56, 2, 18, 23, 48, 78, 82, 67, 35, 5, 31, 61, 91, 101,
        77, 53, 32, 4, 25, 43, 75, 85, 100, 89, 60, 30, 9, 34, 68, 80,
        51, 41, 21, 27, 40, 70, 94, 102, 110, 103, 93, 57, 26, 11, 37, 65,
        44, 29, 33, 45, 72, 90, 104, 121, 117, 114, 106, 88, 54, 17, 13, 16,
        14, 36, 49, 76, 83, 98, 118, 126, 125, 124, 113, 99, 81, 50, 22, 7]

for m in range(im2.size[1]):
    k = m % K
    if m / K % 2 == 0:
        t = 0
    else:
        t = K
    for n in range(im2.size[0]):
        l = (n % L + t) % L
        pix = int(im.getpixel((m / time, n / time)) / 255.0 * N + 0.5)
        if pix > Mask[k * L + l]:
            im2.putpixel((m, n), 1)
        else:
            im2.putpixel((m, n), 0)
im2.save("AM45.bmp")

########################################################################
# 75度加网算法
### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 12
K = 3
L = 51
N = 153
q = 4
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))

Mask = [153, 145, 136, 117, 95, 81, 8, 52, 93, 104, 97, 86, 77, 69, 59, 54, 41, 29, 7, 5, 36, 23, 13, 18, 26, 34,
        46, 64, 67, 72, 79, 25, 50, 66, 90, 103, 122, 128, 130, 137, 134, 118, 102, 82, 16, 51, 96, 115, 132, 147, 152,
        148, 139, 126, 105, 98, 78, 15, 27, 80, 73, 71, 61, 53, 48, 31, 14, 1, 10, 17, 4, 3, 6, 30, 49, 60, 68,
        75, 84, 89, 106, 83, 37, 35, 85, 107, 119, 131, 138, 146, 142, 140, 129, 109, 92, 32, 39, 91, 111, 124, 141,
        144,
        120, 101, 88, 74, 63, 58, 2, 20, 65, 47, 43, 40, 28, 11, 12, 24, 38, 42, 55, 21, 22, 56, 62, 70, 87, 100,
        114, 121, 127, 113, 99, 45, 9, 57, 110, 123, 135, 143, 151, 150, 149, 133, 112, 94, 44, 19, 76, 108, 116, 125,
        136]

for m in range(im2.size[1]):
    k = m % K
    t = q * K * (m / K) % L;
    for n in range(im2.size[0]):
        l = (n % L + t) % L
        pix = int(im.getpixel((m / time, n / time)) / 255.0 * N + 0.5)
        if pix > Mask[k * L + l]:
            im2.putpixel((m, n), 1)
        else:
            im2.putpixel((m, n), 0)
im2.save("AM75.bmp")

########################################################################


########################################################################


########################################################################
# Bayer抖动算法

# Digital Screening
# Author: Sin_Geek
# Date: 2015-05-17

from PIL import Image

time = 8
K = 8
L = 8
N = 63
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))

# Bayer Ordered Dithering
Mask = [0, 32, 8, 40, 2, 34, 10, 42,
        48, 16, 56, 42, 50, 18, 58, 26,
        12, 44, 4, 36, 14, 46, 6, 38,
        60, 28, 52, 20, 62, 30, 54, 22,
        3, 35, 11, 43, 1, 33, 9, 41,
        51, 19, 59, 27, 49, 17, 57, 25,
        15, 47, 7, 39, 13, 45, 5, 37,
        63, 31, 55, 23, 61, 29, 53, 21]

for m in range(im2.size[1]):
    k = m % K
    for n in range(im2.size[0]):
        l = n % L
        pix = int(im.getpixel((m / time, n / time)) / 255.0 * N + 0.5)
        if pix > Mask[k * L + l]:
            im2.putpixel((m, n), 1)
        else:
            im2.putpixel((m, n), 0)
im2.save("F:/img/out/FM_Bayer.bmp")

########################################################################
# Halftone抖动算法
### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 8
K = 8
L = 8
N = 63
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))

# Halftone Ordered Dithering
Mask = [28, 10, 18, 26, 36, 44, 52, 34,
        22, 2, 4, 12, 48, 58, 60, 42,
        14, 6, 0, 20, 40, 56, 62, 50,
        24, 16, 8, 30, 32, 54, 46, 38,
        37, 45, 53, 35, 29, 11, 19, 27,
        49, 59, 61, 43, 23, 3, 5, 13,
        41, 57, 63, 51, 15, 7, 1, 21,
        33, 55, 47, 39, 25, 17, 9, 31]

for m in range(im2.size[1]):
    k = m % K
    for n in range(im2.size[0]):
        l = n % L
        pix = int(im.getpixel((m / time, n / time)) / 255.0 * N + 0.5)
        if pix > Mask[k * L + l]:
            im2.putpixel((m, n), 1)
        else:
            im2.putpixel((m, n), 0)
im2.save("F:/img/outFM_Halftone.bmp")

########################################################################
# Screw抖动算法
### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 8
K = 8
L = 8
N = 63
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))

# Screw Ordered Dithering
Mask = [64, 53, 42, 26, 27, 43, 54, 61,
        60, 41, 25, 14, 15, 28, 44, 55,
        52, 40, 13, 5, 6, 16, 29, 45,
        39, 24, 12, 1, 2, 7, 17, 30,
        38, 23, 11, 4, 3, 8, 18, 31,
        51, 37, 22, 10, 9, 19, 32, 41,
        59, 50, 36, 21, 20, 33, 47, 56,
        63, 58, 49, 35, 34, 48, 57, 62]

for m in range(im2.size[1]):
    k = m % K
    for n in range(im2.size[0]):
        l = n % L
        pix = int(im.getpixel((m / time, n / time)) / 255.0 * N + 0.5)
        if pix > Mask[k * L + l]:
            im2.putpixel((m, n), 1)
        else:
            im2.putpixel((m, n), 0)
im2.save("F:/img/out/FM_Screw.bmp")

########################################################################
# CoarseFatting抖动算法
### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 8
K = 8
L = 8
N = 63
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))

# CoarseFatting Ordered Dithering
Mask = [4, 14, 52, 58, 56, 45, 20, 6,
        16, 26, 38, 50, 48, 36, 28, 18,
        43, 35, 31, 9, 11, 25, 33, 41,
        61, 46, 23, 1, 3, 13, 55, 60,
        57, 47, 21, 7, 5, 15, 53, 59,
        49, 37, 29, 19, 17, 27, 39, 51,
        10, 24, 32, 40, 42, 34, 30, 8,
        2, 12, 54, 60, 51, 44, 22, 0]

for m in range(im2.size[1]):
    k = m % K
    for n in range(im2.size[0]):
        l = n % L
        pix = int(im.getpixel((m / time, n / time)) / 255.0 * N + 0.5)
        if pix > Mask[k * L + l]:
            im2.putpixel((m, n), 1)
        else:
            im2.putpixel((m, n), 0)
im2.save("F:/img/out/FM_CoarseFatting.bmp")

########################################################################
# 无序抖动算法
# 全局伪随机抖动算法
### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image
import random

time = 8
K = 8
L = 8
N = 63
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))

for m in range(im2.size[1]):
    k = m % K
    for n in range(im2.size[0]):
        l = n % L
        pix = int(im.getpixel((m / time, n / time)) / 255.0 * N + 0.5)
        if pix > random.randint(0, 64):
            im2.putpixel((m, n), 1)
        else:
            im2.putpixel((m, n), 0)
im2.save("F:/img/out/FM_Random.bmp")

########################################################################
# 局部伪随机抖动算法
### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image
import random

time = 8
K = 8
L = 8
N = 63
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))
Mask = [0] * im.size[0] * time * im.size[1] * time
for i in range(63):
    Mask[i] = random.randint(0, 64)

for m in range(im2.size[1]):
    k = m % K
    for n in range(im2.size[0]):
        l = n % L
        pix = int(im.getpixel((m / time, n / time)) / 255.0 * N + 0.5)
        if pix > Mask[k * L + l]:
            im2.putpixel((m, n), 1)
        else:
            im2.putpixel((m, n), 0)
im2.save("F:/img/out/FM_Random_1.bmp")

########################################################################
# Floyd-Steinberg算法
# 误差扩散方式

### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 8
N = 144
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))
pix = [0.0] * im2.size[0] * im2.size[1]

for m in range(im2.size[1]):
    for n in range(im2.size[0]):
        pix[m * im2.size[0] + n] = im.getpixel((m / time, n / time)) * N / 255.0 + 0.5

for m in range(im2.size[1] - 1):
    for n in range(1, im2.size[0] - 1):
        if pix[m * im2.size[0] + n] <= 72:
            nError = pix[m * im2.size[0] + n]
            im2.putpixel((m, n), 0)
        else:
            nError = pix[m * im2.size[0] + n] - N
            im2.putpixel((m, n), 1)
        pix[m * im2.size[0] + n + 1] += nError * 7 / 16.0
        pix[(m + 1) * im2.size[0] + n - 1] += nError * 3 / 16.0
        pix[(m + 1) * im2.size[0] + n] += nError * 5 / 16.0
        pix[(m + 1) * im2.size[0] + n + 1] += nError * 1 / 16.0

im2.save("FM_Floyd_Steinberg.bmp")

########################################################################
# 蛇形Floyd-Steinberg算法
# 算法公式
# 扩散方式与Floyd-Steinberg算法一样，但扫描方式不同，Floyd-Steinberg算法是遵循从左到右，从上到下。换一种扫描方式就得到了蛇形Floyd-Steinberg算法，扫描的方式是类似蛇形，从左到右再从右到左，再从左道右循环下去

### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 8
N = 144
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))
pix = [0.0] * im2.size[0] * im2.size[1]

for m in range(im2.size[1]):
    for n in range(im2.size[0]):
        pix[m * im2.size[0] + n] = im.getpixel((m / time, n / time)) * N / 255.0 + 0.5

for m in range(im2.size[1] - 1):
    if m % 2 == 1:
        for n in range(1, im2.size[0] - 1):
            if pix[m * im2.size[0] + n] <= 72:
                nError = pix[m * im2.size[0] + n]
                im2.putpixel((m, n), 0)
            else:
                nError = pix[m * im2.size[0] + n] - N
                im2.putpixel((m, n), 1)
            pix[m * im2.size[0] + n + 1] += nError * 7 / 16.0
            pix[(m + 1) * im2.size[0] + n - 1] += nError * 3 / 16.0
            pix[(m + 1) * im2.size[0] + n] += nError * 5 / 16.0
            pix[(m + 1) * im2.size[0] + n + 1] += nError * 1 / 16.0
    else:
        for n in range(im2.size[0] - 2, 0, -1):
            if pix[m * im2.size[0] + n] <= 72:
                nError = pix[m * im2.size[0] + n]
                im2.putpixel((m, n), 0)
            else:
                nError = pix[m * im2.size[0] + n] - N
                im2.putpixel((m, n), 1)
            pix[m * im2.size[0] + n - 1] += nError * 7 / 16.0
            pix[(m + 1) * im2.size[0] + n + 1] += nError * 3 / 16.0
            pix[(m + 1) * im2.size[0] + n] += nError * 5 / 16.0
            pix[(m + 1) * im2.size[0] + n - 1] += nError * 1 / 16.0
im2.save("FM_Floyd_Steinberg_Snake.bmp")

########################################################################

# Burkes算法

### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 8
N = 144
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))
pix = [0.0] * im2.size[0] * im2.size[1]

for m in range(im2.size[1]):
    for n in range(im2.size[0]):
        pix[m * im2.size[0] + n] = im.getpixel((m / time, n / time)) * N / 255.0 + 0.5

for m in range(1, im2.size[1] - 1):
    for n in range(2, im2.size[0] - 2):
        if pix[m * im2.size[0] + n] <= 72:
            nError = pix[m * im2.size[0] + n]
            im2.putpixel((m, n), 0)
        else:
            nError = pix[m * im2.size[0] + n] - N
            im2.putpixel((m, n), 1)
        pix[m * im2.size[0] + n + 1] += nError * 8 / 32.0
        pix[m * im2.size[0] + n + 2] += nError * 4 / 32.0
        pix[(m + 1) * im2.size[0] + n - 2] += nError * 2 / 32.0
        pix[(m + 1) * im2.size[0] + n - 1] += nError * 4 / 32.0
        pix[(m + 1) * im2.size[0] + n] += nError * 8 / 32.0
        pix[(m + 1) * im2.size[0] + n + 1] += nError * 4 / 32.0
        pix[(m + 1) * im2.size[0] + n + 2] += nError * 2 / 32.0

im2.save("FM_Burkes.bmp")

########################################################################

# Jarris-Judice-Ninke算法

### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 8
N = 144
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))
pix = [0.0] * im2.size[0] * im2.size[1]

for m in range(im2.size[1]):
    for n in range(im2.size[0]):
        pix[m * im2.size[0] + n] = im.getpixel((m / time, n / time)) * N / 255.0 + 0.5

for m in range(im2.size[1] - 2):
    for n in range(2, im2.size[0] - 2):
        if pix[m * im2.size[0] + n] <= 72:
            nError = pix[m * im2.size[0] + n]
            im2.putpixel((m, n), 0)
        else:
            nError = pix[m * im2.size[0] + n] - N
            im2.putpixel((m, n), 1)
        pix[m * im2.size[0] + n + 1] += nError * 7 / 48.0
        pix[m * im2.size[0] + n + 2] += nError * 5 / 48.0
        pix[(m + 1) * im2.size[0] + n - 2] += nError * 3 / 48.0
        pix[(m + 1) * im2.size[0] + n - 1] += nError * 5 / 48.0
        pix[(m + 1) * im2.size[0] + n] += nError * 7 / 48.0
        pix[(m + 1) * im2.size[0] + n + 1] += nError * 5 / 48.0
        pix[(m + 1) * im2.size[0] + n + 2] += nError * 3 / 48.0
        pix[(m + 2) * im2.size[0] + n - 2] += nError * 1 / 48.0
        pix[(m + 2) * im2.size[0] + n - 1] += nError * 3 / 48.0
        pix[(m + 2) * im2.size[0] + n] += nError * 5 / 48.0
        pix[(m + 2) * im2.size[0] + n + 1] += nError * 3 / 48.0
        pix[(m + 2) * im2.size[0] + n + 2] += nError * 1 / 48.0

im2.save("FM_Jarris_Judice_Ninke.bmp")

########################################################################
# Stucki算法
### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 8
N = 144
im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))
pix = [0.0] * im2.size[0] * im2.size[1]

for m in range(im2.size[1]):
    for n in range(im2.size[0]):
        pix[m * im2.size[0] + n] = im.getpixel((m / time, n / time)) * N / 255.0 + 0.5

for m in range(im2.size[1] - 2):
    for n in range(2, im2.size[0] - 2):
        if pix[m * im2.size[0] + n] <= 72:
            nError = pix[m * im2.size[0] + n]
            im2.putpixel((m, n), 0)
        else:
            nError = pix[m * im2.size[0] + n] - N
            im2.putpixel((m, n), 1)
        pix[m * im2.size[0] + n + 1] += nError * 8 / 42.0
        pix[m * im2.size[0] + n + 2] += nError * 4 / 42.0
        pix[(m + 1) * im2.size[0] + n - 2] += nError * 2 / 42.0
        pix[(m + 1) * im2.size[0] + n - 1] += nError * 4 / 42.0
        pix[(m + 1) * im2.size[0] + n] += nError * 8 / 42.0
        pix[(m + 1) * im2.size[0] + n + 1] += nError * 4 / 42.0
        pix[(m + 1) * im2.size[0] + n + 2] += nError * 2 / 42.0
        pix[(m + 2) * im2.size[0] + n - 2] += nError * 1 / 42.0
        pix[(m + 2) * im2.size[0] + n - 1] += nError * 2 / 42.0
        pix[(m + 2) * im2.size[0] + n] += nError * 4 / 42.0
        pix[(m + 2) * im2.size[0] + n + 1] += nError * 2 / 42.0
        pix[(m + 2) * im2.size[0] + n + 2] += nError * 1 / 42.0

im2.save("F:/img/out/FM_Stucki.bmp")

########################################################################

# 多位误差扩散算法
# 以Floyd-Steinberg算法为例，都是两位0和1，非黑即白。但是市场上出现了多位的打印机，于是随之而出的是多位的算法。即存在0，0.5，1。
#
# 算法公式
# 根据分为几位，划分区域，分别进行误差扩散，考虑到规律性条纹等问题，可以对划分区域进行一个随机值的添加，使得分割点不再是一个像素值，而是动态范围内的一个值，降低规律性。本示例中没有添加，读者可自行改进~~~

### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image
import random

time = 8
N = 144
R = 2
M = R * 2

im = Image.open('F:/img/test.png').convert('L')
im2 = Image.new("L", (im.size[0] * time, im.size[1] * time))
pix = [0.0] * im2.size[0] * im2.size[1]

for m in range(im2.size[1]):
    for n in range(im2.size[0]):
        pix[m * im2.size[0] + n] = im.getpixel((m / time, n / time)) * N / 255.0 + 0.5

for m in range(1, im2.size[1] - 1):
    for n in range(1, im2.size[0] - 1):
        if pix[m * im2.size[0] + n] <= N / M:
            nError = pix[m * im2.size[0] + n]
            im2.putpixel((m, n), 0)
        elif pix[m * im2.size[0] + n] <= 3 * N / M:
            nError = pix[m * im2.size[0] + n] - 2 * N / M
            im2.putpixel((m, n), 255 / R)
        else:
            nError = pix[m * im2.size[0] + n] - 144
            im2.putpixel((m, n), 255)
        pix[m * im2.size[0] + n + 1] += nError * 7 / 16.0
        pix[(m + 1) * im2.size[0] + n - 1] += nError * 3 / 16.0
        pix[(m + 1) * im2.size[0] + n] += nError * 5 / 16.0
        pix[(m + 1) * im2.size[0] + n + 1] += nError * 1 / 16.0

im2.save("F:/img/out/FM_Floyd_Steinberg_Multi_Threshold.bmp")
