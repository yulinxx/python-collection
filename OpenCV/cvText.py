# -*- coding: utf-8 -*-
import cv2
import numpy
import datetime
from PIL import Image, ImageDraw, ImageFont


def putText(img, strTxt, pos, ft):
    draw = ImageDraw.Draw(img)
    draw.text(pos, strTxt, font=ft, fill=fillColor)


if __name__ == '__main__':
    img_OpenCV = cv2.imread('F:/template.jpg')  # 模板图

    img_PIL = Image.fromarray(cv2.cvtColor(img_OpenCV, cv2.COLOR_BGR2RGB))
    fontPath = 'C:/Windows/Fonts/msyh.ttc'  # 微软雅黑

    font = ImageFont.truetype(fontPath, 32)  # 字体及大小
    fillColor = (255, 255, 255)  # 白
    position = (10, 10)  # 位置
    strTimeNow = '18:57'  # 时间
    # strTimeNow = datetime.datetime.now().strftime('%H:%M')
    putText(img_PIL, strTimeNow, position, font)

    font = ImageFont.truetype(fontPath, 38)
    fillColor = (0, 0, 0)
    position = (838, 330)

    strName = '李雨林'  # 姓名
    putText(img_PIL, strName, position, font)

    font = ImageFont.truetype(fontPath, 38)
    fillColor = (0, 0, 0)
    position = (670, 390)
    strTimeNow = '2022-03-07 18:57' # 实时时间
    # strTimeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    putText(img_PIL, strTimeNow, position, font)

    font = ImageFont.truetype(fontPath, 46)
    strPlace = '5号线翻身地铁站' # 打卡地点
    # strPlace = '2号线水湾站'
    strPlace = '巴士集团-粤B04502D'
    # strPlace = '科技大厦二期'

    w, html = font.getsize(strPlace)
    width = int(img_OpenCV.shape[1])  # 获取图片的宽
    heigh = int(img_OpenCV.shape[0])  # 获取图片的高
    fontScale = 0.5
    thickness = 2
    txtSize = cv2.getTextSize(strTimeNow, cv2.FONT_HERSHEY_SIMPLEX, fontScale, thickness)  # 文字的尺寸
    # position = ((width * 0.5 - txtSize[0][0]) * 1, 580)  # X方向进行居中显示
    position = ((width - w) * 0.5, 580)  # X方向进行居中显示
    putText(img_PIL, strPlace, position, font)

    # font = ImageFont.truetype(fontPath, 36)
    # fillColor = (255, 255, 255)
    # position = (150, 1600)
    # strTextCheck = '2022-03-07 01:52'
    # strTextCheck = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d") + (' 01:52')
    # putText(img_PIL, strTextCheck, position, font)

    # 图片处理
    img_OpenCV = cv2.cvtColor(numpy.asarray(img_PIL), cv2.COLOR_RGB2BGR)

    scale_percent = 60  # percent of original size
    width = int(width * scale_percent / 100)
    height = int(heigh * scale_percent / 100)
    dim = (width, height)
    img_OpenCVResize = cv2.resize(img_OpenCV, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow("print chinese to image", img_OpenCVResize)

    cv2.waitKey()
    strFileName = 'F:/' + strName + '_' + strPlace + '.jpg'
    cv2.imwrite(strFileName, img_OpenCV)
    cv2.imencode('.jpg', img_OpenCV)[1].tofile(strFileName)  # 保存
