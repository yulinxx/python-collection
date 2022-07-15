### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17
# https://blog.csdn.net/sin_geek/article/details/45932145

from PIL import Image

time = 8
K = 8
L = 8
N = 63
im = Image.open('E:/img/p1.jfif').convert('L')
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

for y in range(im2.size[1]):
    k = y % K
    for x in range(im2.size[0]):
        l = x % L
        pix = int(im.getpixel((x / time, y / time)) / 255.0 * N + 0.5)
        if pix > Mask[k * L + l]:
            im2.putpixel((x, y), 1)
        else:
            im2.putpixel((x, y), 0)

im2.save("E:/img/Dithering--BayerOrdered.png")
print('Bayer Ordered Dithering End')
