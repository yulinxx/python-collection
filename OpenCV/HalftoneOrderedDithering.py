
### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 8
K = 8
L = 8
N = 63

im = Image.open('E:/img/p1.jfif').convert('L')

im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))

print(im.size)
print(im2.size)
print('-----------')

# Halftone Ordered Dithering
Mask = [28, 10, 18, 26, 36, 44, 52, 34,
        22, 2, 4, 12, 48, 58, 60, 42,
        14, 6, 0, 20, 40, 56, 62, 50,
        24, 16, 8, 30, 32, 54, 46, 38,
        37, 45, 53, 35, 29, 11, 19, 27,
        49, 59, 61, 43, 23, 3, 5, 13,
        41, 57, 63, 51, 15, 7, 1, 21,
        33, 55, 47, 39, 25, 17, 9, 31]

for y in range(im2.size[1]):  # 532
    k = y % K

    for x in range(im2.size[0]):  # 800
        l = x % L
        try:
            pix = int(im.getpixel((x / time, y / time)) / 255.0 * N + 0.5)
        except:
            print('Error')
        if pix > Mask[k * L + l]:
            im2.putpixel((x, y), 1)
        else:
            im2.putpixel((x, y), 0)

im2.save("E:/img/Dithering--HalftoneOrdered.png")
print('Halftone Ordered Dithering End')









