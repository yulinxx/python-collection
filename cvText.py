# -*- coding: utf-8 -*-
import cv2
import numpy
import datetime
from PIL import Image, ImageDraw, ImageFont


def putText(img, strTxt, pos, ft, color):
    draw = ImageDraw.Draw(img)
    draw.text(pos, strTxt, font=ft, fill=fillColor)


if __name__ == '__main__':

    style = 1  # 0 公交上班 1 公交下班 2 地铁上班 3 地铁下班 4 公司打卡
    img_OpenCV = cv2.imread('F:/template24.jpg')  # 模板图

    img_PIL = Image.fromarray(cv2.cvtColor(img_OpenCV, cv2.COLOR_BGR2RGB))
    fontPath = 'C:/Windows/Fonts/msyh.ttc'  # 微软雅黑

    strData = '2022-03-10'
    # 系统时间
    font = ImageFont.truetype(fontPath, 32)  # 字体及大小
    fillColor = (255, 255, 255)  # 白
    position = (10, 10)  # 位置
    if style == 0:  # 0 公交上班
        strTimeSys = '07:47'  # 时间
        strTimeNow = strData + ' ' + strTimeSys  # 实时时间
        strPlace = '巴士集团-粤B04502D'
    elif style == 1:  # 1 公交下班
        strTimeSys = '18:47'  # 时间
        strPlace = '巴士集团-粤B54502D'
        strTimeNow = strData + ' ' + strTimeSys  # 实时时间
    elif style == 2:  # 2 地铁上班
        strTimeSys = '07:47'  # 时间
        strTimeNow = strData + ' ' + strTimeSys  # 实时时间
        strPlace = '5号线翻身地铁站'  # 打卡地点
    elif style == 3:  # 3 地铁下班
        strTimeSys = '18:47'  # 时间
        strTimeNow = strData + ' ' + strTimeSys  # 实时时间
        strPlace = '2号线水湾站'  # 打卡地点
    elif style == 4:  # 4 公司打卡
        strTimeSys = '08:42'  # 时间
        strTimeNow = strData + ' ' + strTimeSys  # 实时时间
        strPlace = '科技大厦二期'

    strTextCheck = strData + ' 03:51'  # 检查时间

    # strTimeNow = datetime.datetime.now().strftime('%H:%M')
    putText(img_PIL, strTimeSys, position, font, fillColor)

    # 地点
    font = ImageFont.truetype(fontPath, 65)
    fillColor = (0, 0, 0)  # 黑
    w, h = font.getsize(strPlace)
    width = int(img_OpenCV.shape[1])  # 获取图片的宽
    heigh = int(img_OpenCV.shape[0])  # 获取图片的高
    position = ((width - w) * 0.5, 550)  # X方向进行居中显示
    putText(img_PIL, strPlace, position, font, fillColor)

    # 姓名
    strName = '李*林'
    font = ImageFont.truetype(fontPath, 38)
    fillColor = (125, 125, 125)  # 灰

    # strTimeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    #

    strText = strName + ' ' + strTimeNow
    w, h = font.getsize(strText)

    position = ((width - w) * 0.5, 640)  # X方向进行居中显示
    putText(img_PIL, strText, position, font, fillColor)

    # 检测时间
    position = (190, 1540)
    fillColor = (255, 255, 255)  # 白
    # strTextCheck = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d") + (' 03:52')

    putText(img_PIL, strTextCheck, position, font, fillColor)

    # 图片处理
    img_OpenCV = cv2.cvtColor(numpy.asarray(img_PIL), cv2.COLOR_RGB2BGR)

    scale_percent = 60  # percent of original size
    width = int(width * scale_percent / 100)
    height = int(heigh * scale_percent / 100)
    dim = (width, height)
    img_OpenCVResize = cv2.resize(img_OpenCV, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow("print chinese to image", img_OpenCVResize)

    cv2.waitKey()
    strFileName = 'F:/' + strPlace + '.jpg'
    # cv2.imwrite(strFileName, img_OpenCV)
    cv2.imencode('.jpg', img_OpenCV)[1].tofile(strFileName)  # 保存
