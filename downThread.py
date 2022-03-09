import os
from datetime import time

import wget

import sccnnDownload
from PyQt6.QtCore import QThread, pyqtSignal


class DownThread(QThread):
    def __init__(self, keyWord, savePath):
        super(DownThread, self).__init__()
        self.__strSearchWord = keyWord
        self.__strSavePath = savePath

        self.__stop = False     # 停止
        self.tipSignal = pyqtSignal(str)
        self.endSignal = pyqtSignal()

    def run(self):
        self.__listName = []
        start = time.time()
        self.__process()

        end = time.time()
        # self.__funcTip("结束...%s 耗时" % (end - start))
        tmDuration = ('%.2f' % (end - start))
        self.tipSignal.emit("结束, 共耗时:%s " % tmDuration)
        # self.__funcTip("---------------------------------------------\n")
        self.tipSignal.emit("---------------------------------------------\n")

        # self.__funcEnd()
        self.endSignal.emit()

        self.__stop = False

    def stop(self):
        self.__stop = True


    def __process(self):
        isExists = os.path.exists(self.__strSavePath)
        if not isExists:
            os.makedirs(self.__strSavePath)

        baseUrl = f'http://so.sccnn.com/search/{self.__strSearchWord}/{str(1)}.html'
        webInfo = sccnnDownload.getURLInfo(baseUrl)
        pageCount = sccnnDownload.getSearchPage(webInfo)

        print(f'搜索到 {pageCount} 页')

        downCount = 0
        for pageNum in range(1, int(pageCount)):
            print(f'处理第 {pageNum} 页')
            baseUrl = f'http://so.sccnn.com/search/{self.__strSearchWord}/{str(pageNum)}.html'
            webInfo = sccnnDownload.getURLInfo(baseUrl)

            if self.__stop:
                return

            if webInfo is not None:
                mapList = sccnnDownload.getPageLinks(webInfo)

                for key in mapList.keys():
                    resInfos = sccnnDownload.getDownLink(mapList[key])
                    if resInfos is not None:
                        name = key + resInfos[0]
                        urlDownload = resInfos[1]

                        dotIndex = urlDownload.rfind('.')
                        surf = urlDownload[dotIndex:]
                        path = f'F:/{name}{surf}'  # 保存的路径

                        print(f' {downCount} 即将下载: {urlDownload} \n\t 保存至: {path}')

                        wget.download(urlDownload, path)  # 下载
                        downCount += 1
                        if self.__stop:
                            return

        print(f'下载完成,共下载{downCount}个')