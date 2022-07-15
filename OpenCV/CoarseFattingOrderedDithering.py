### Digital Screening
### Author: Sin_Geek
### Date: 2015-05-17

from PIL import Image

time = 8
K = 8
L = 8
N = 63
im = Image.open('E:/img/p1.jfif').convert('L')
im2 = Image.new("1",(im.size[0]*time,im.size[1]*time))

#CoarseFatting Ordered Dithering
Mask=[4,14,52,58,56,45,20,6,
      16,26,38,50,48,36,28,18,
      43,35,31,9,11,25,33,41,
      61,46,23,1,3,13,55,60,
      57,47,21,7,5,15,53,59,
      49,37,29,19,17,27,39,51,
      10,24,32,40,42,34,30,8,
      2,12,54,60,51,44,22,0]

for y in range(im2.size[1]):
    k = y % K
    for x in range(im2.size[0]):
        l = x % L
        pix = int(im.getpixel((x / time, y / time)) / 255.0 * N + 0.5)
        if pix > Mask[k*L+l]:
            im2.putpixel((x, y), 1)
        else:
            im2.putpixel((x, y), 0)

im2.save("E:/img/Dithering--CoarseFattingOrdered.png")
print('CoarseFatting Ordered Dithering End')