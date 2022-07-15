import cv2


def set_pixel(im, x, y, new):
    im[x, y] = new


def quantize(im):
    for y in range(0, height - 1):
        for x in range(1, width - 1):
            old_pixel = im[x, y]
            if old_pixel < 127:
                new_pixel = 0
            else:
                new_pixel = 255
            set_pixel(im, x, y, new_pixel)
            quant_err = old_pixel - new_pixel
            set_pixel(im, x + 1, y, im[x + 1, y] + quant_err * w1)
            set_pixel(im, x - 1, y + 1, im[x - 1, y + 1] + quant_err * w2)
            set_pixel(im, x, y + 1, im[x, y + 1] + quant_err * w3)
            set_pixel(im, x + 1, y + 1, im[x + 1, y + 1] + quant_err * w4)

    return im


if __name__ == "main":
    img = cv2.imread("F:/ori.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = img.copy()
    width, height, z = img.shape
    w1 = 7 / 16.0
    # print w1
    w2 = 3 / 16.0
    w3 = 5 / 16.0
    w4 = 1 / 16.0
    blue = img[:, :, 0]
    blue = quantize(blue)
    green = img[:, :, 1]
    green = quantize(green)
    red = img[:, :, 2]
    red = quantize(red)
    gray1 = quantize(gray)

    image = cv2.merge((blue, green, red))
    cv2.imshow('original', img2)
    cv2.imshow('merged', image)
    cv2.imshow('gray', gray1)
    cv2.waitKey(0)
