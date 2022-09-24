# import cv2
#
# image = cv2.imread("F:/img/test.png")
# gaussian_3 = cv2.GaussianBlur(image, (0, 0), 2.0)
# unsharp_image = cv2.addWeighted(image, 2.0, gaussian_3, -1.0, 0)
# cv2.imshow("example_unsharp.jpg", unsharp_image)
#
# cv2.waitKey(0)


import cv2
from matplotlib import pyplot as plt

im = cv2.imread("F:/img/test.png", 0)

#im_blurred = cv2.GaussianBlur(im, (11,11), 10)
im_blurred = cv2.GaussianBlur(im, (49, 49), 26)

im1 = cv2.addWeighted(im, 1.0 + 3.0, im_blurred, -3.0, 0) # im1 = im + 3.0*(im - im_blurred)
cv2.imwrite('F:/img/out/xxxx.png', im1)

#plt.figure(figsize=(20,10))
#plt.subplot(121),plt.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)), plt.axis('off'), plt.title('Original Image', size=20)
#plt.subplot(122),plt.imshow(cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)), plt.axis('off'), plt.title('Sharpened Image', size=20)
#plt.show()