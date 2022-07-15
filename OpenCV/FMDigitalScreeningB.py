### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image
import random

time = 8
K = 8
L = 8
N = 63
im = Image.open('E:/img/p1.jfif').convert('L')
im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))
Mask = [0] * im.size[0] * time * im.size[1] * time
for i in range(63):
    Mask[i] = random.randint(0, 64)

for y in range(im2.size[1]):
    k = y % K
    for x in range(im2.size[0]):
        l = x % L
        pix = int(im.getpixel((x / time, y / time)) / 255.0 * N + 0.5)
        if pix > Mask[k * L + l]:
            im2.putpixel((x, y), 1)
        else:
            im2.putpixel((x, y), 0)
im2.save("E:/img/Dithering--FM_RandomB.png")
print('FM_RandomB End')