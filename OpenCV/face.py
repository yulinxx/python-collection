import cv2

filepath = "F:/p4.webp"
img = cv2.imread(filepath)  # 读取图片
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 1 加载分类器OpenCV人脸识别分类器
# xml的结构
# 训练得到的分类器以xml形式保存，整体上它包括stageType、featureType、height、width、stageParams、featureParams、stages、features几个节点。
classifier = cv2.CascadeClassifier(
    "C:/Users/niesi/AppData/Local/Programs/Python/Python38/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml"
)
color = (0, 255, 0)  # 定义绘制颜色

# 2 调用识别人脸 调用detectMultiScale()函数检测
# 1.image表示的是要检测的输入图像
# 2.objects表示检测到的人脸目标序列
# 3.scaleFactor表示每次图像尺寸减小的比例
# 4. minNeighbors表示每一个目标至少要被检测到3次才算是真的目标(因为周围的像素和不同的窗口大小都可以检测到人脸),
# 5.minSize为目标的最小尺寸
# 6.minSize为目标的最大尺寸
faceRects = classifier.detectMultiScale(
    gray, scaleFactor=1.2, minNeighbors=10, minSize=(12, 12))

# 3 把检测到的人脸等用矩形（或者圆形等其他图形）画出来
if len(faceRects):  # 大于0则检测到人脸
    for faceRect in faceRects:  # 单独框出每一张人脸
        x, y, w, h = faceRect
        # 框出人脸
        cv2.rectangle(img, (x, y), (x + h, y + w), color, 1)
        # cropped = img[y:y+w, x:x+h] # 裁剪坐标为[y0:y1, x0:x1]

        # 左眼
        cv2.circle(img, (x + w // 4, y + h // 4 + 30), min(w // 8, h // 8),
                   color)
        #右眼
        cv2.circle(img, (x + 3 * w // 4, y + h // 4 + 30), min(w // 8, h // 8),
                   color)
        #嘴巴
        cv2.rectangle(img, (x + 3 * w // 8, y + 3 * h // 4),
                      (x + 5 * w // 8, y + 7 * h // 8), color)


cv2.imshow("image", img)  # 显示图像
k = cv2.waitKey(0)
if k == ord("s"):
    cv2.imwrite("F:/out.jpg", img)
cv2.destroyAllWindows()