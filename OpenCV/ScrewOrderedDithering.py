### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 2
K = 8
L = 8
N = 63
im = Image.open('E:/img/p1.jfif').convert('L')
imGray = Image.new("1", (im.size[0] * time, im.size[1] * time))

imGray.show('imGray')

# Screw Ordered Dithering
Mask = [64, 53, 42, 26, 27, 43, 54, 61,
        60, 41, 25, 14, 15, 28, 44, 55,
        52, 40, 13, 5, 6, 16, 29, 45,
        39, 24, 12, 1, 2, 7, 17, 30,
        38, 23, 11, 4, 3, 8, 18, 31,
        51, 37, 22, 10, 9, 19, 32, 41,
        59, 50, 36, 21, 20, 33, 47, 56,
        63, 58, 49, 35, 34, 48, 57, 62]

for y in range(imGray.size[1]):
    k = y % K

    for x in range(imGray.size[0]):
        l = x % L

        tmpA = im.getpixel((x / time, y / time))

        pix = int(im.getpixel((x / time, y / time)) / 255.0 * N + 0.5)
        if pix > Mask[(k * L + l) % 64]:
            imGray.putpixel((x, y), 1)
        else:
            imGray.putpixel((x, y), 0)

imGray.show('res')
imGray.save("E:/img/Dithering--ScrewOrdered1.png")
print('Screw Ordered Dithering / End')
