import os
import wget
import urllib
import time
from bs4 import BeautifulSoup
from PyQt6.QtCore import QThread, pyqtSignal


class DownThread(QThread):
    tipSignal = pyqtSignal(str)
    endSignal = pyqtSignal()

    def __init__(self):
        super(DownThread, self).__init__()
        self.__strSearchWord = '节日'
        self.__strSavePath = os.getcwd()

        self.__pageCount = 1
        self.__formatIndex = 0    # 0/所有格式 1/PSD+AI 2/PSD 3/AI 4/EPS
        self.__downCount = 99999  # 下载个数
        self.__stop = False  # 停止

    def getPages(self):
        baseUrl = f'http://so.sccnn.com/search/{self.__strSearchWord}/{str(1)}.html'
        webInfo = self.getURLInfo(baseUrl)
        pageCount = self.getSearchPage(webInfo)

        strTip = f'搜索到 {pageCount} 页'
        self.tipSignal.emit(strTip)
        self.__pageCount = int(pageCount)
        return self.__pageCount

    def setDownKeyword(self, keyWord):
        """搜索关键字"""
        self.__strSearchWord = urllib.request.quote(keyWord)

    def setSavePath(self, savePath):
        """保存路径"""
        self.__strSavePath = savePath + '/'

    def setDownFormat(self, formatIndex):
        """下载格式"""
        self.__formatIndex = formatIndex

    def setDownCount(self, downCount):
        """下载数量"""
        self.__downCount = downCount

    def run(self):
        """线程入口函数"""
        start = time.time()

        self.__process()

        end = time.time()
        duration = ('%.2f' % (end - start))
        self.tipSignal.emit(f'结束, 共耗时:{str(duration)}')
        self.tipSignal.emit("---------------------------------------------\n")
        self.endSignal.emit()

        self.__stop = False

    def stop(self):
        self.__stop = True

    def __process(self):
        """线程运行程序"""
        isExists = os.path.exists(self.__strSavePath)  # 创建目录
        if not isExists:
            os.makedirs(self.__strSavePath)

        isExists = os.path.exists(self.__strSavePath)  # 再次检查目录
        if not isExists:
            return

        baseUrl = f'http://so.sccnn.com/search/{self.__strSearchWord}/{str(1)}.html'
        webInfo = self.getURLInfo(baseUrl)

        downCount = 0
        for pageNum in range(1, self.__pageCount):
            strTip = f'处理第 {pageNum} 页'
            # print(strTip)
            self.tipSignal.emit(strTip)

            baseUrl = f'http://so.sccnn.com/search/{self.__strSearchWord}/{str(pageNum)}.html'
            webInfo = self.getURLInfo(baseUrl)

            if self.__stop:
                self.tipSignal.emit('已停止下载')
                return

            if webInfo is not None:
                mapList = self.getPageLinks(webInfo)

                for key in mapList.keys():
                    resInfo = self.getDownLink(mapList[key])
                    if resInfo is not None:
                        name = key + resInfo[0]
                        urlDownload = resInfo[1]

                        dotIndex = urlDownload.rfind('.')
                        surf = urlDownload[dotIndex:]

                        print(urlDownload)
                        path = self.__strSavePath + name + surf  # 保存的路径
                        strTip = f' {downCount} --即将下载: {urlDownload} \n 保存至: {path}'
                        print(strTip)
                        self.tipSignal.emit(strTip)
                        # wget.download(urlDownload, path)  # 下载

                        # strTest = f'F:/{str(downCount)}.rar'
                        # print(strTest)
                        try:
                            wget.download(urlDownload, out=path)  # 下载
                        except Exception as e:
                            print(e)
                            # self.tipSignal.emit(e)
                        downCount += 1
                        if self.__stop or downCount > self.__downCount:
                            self.tipSignal.emit('已停止下载')
                            return

        strTip = f'下载完成,共下载{downCount}个'
        print(strTip)
        self.tipSignal.emit(strTip)

    def getURLInfo(self, webUrl):
        """获取网页源代码"""
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/44.0.2403.157 Safari/537.36'}

        # print(webUrl)
        req = urllib.request.Request(url=webUrl, headers=header)

        try:
            response = urllib.request.urlopen(req, timeout=5)
            html = response.read().decode('gbk')
        except Exception as e:
            print(e)
            return None

        if response.getcode() == 200:
            soup = BeautifulSoup(html, 'html.parser')
            return soup

        return None

    def getSearchPage(self, webInfo):
        """获取搜索的结果有多少页"""
        mapLink = {}
        tables = webInfo.findAll('td', attrs={'align': 'Center'})
        # print(tables)
        for tab in tables:
            txt = tab.text
            if len(txt) >= 10:
                startIndex = txt.rfind('为')
                endIndex = txt.find('页')
                pageCount = txt[int(startIndex + 1): int(endIndex)]
                return pageCount

        return 0

    def getPageLinks(self, webInfo):
        """获取页面中的下载链接"""
        tables = webInfo.findAll('table', attrs={'bordercolordark': '#ffffff'})
        subTables = tables[0].findAll('div', attrs={'valign': 'middle'})

        mapDownInfo = {}
        # print(subTables[0])
        for item in subTables:
            title = item.text
            # title = item.text()
            href = item.find('a')
            urlDown = href.attrs['href']
            # print(title, urlDown)
            mapDownInfo[title] = urlDown

        return mapDownInfo

    def getDownLink(self, urlDown):
        """获取具体的下载地址"""
        webInfo = self.getURLInfo(urlDown)
        if webInfo is None:
            return None
        TxtDiv = webInfo.find('div', attrs={'class': 'TxtDiv'})
        scoreTxt = TxtDiv.find('font', attrs={'color': '#CC0000'})
        score = scoreTxt.text
        if score != '0':
            return None

        p = TxtDiv.find('p')
        describe = p.text

        # self.__formatIndex = 0    # 0/所有格式 1/PSD+AI 2/PSD 3/AI 4/EPS

        haveFind = False
        if self.__formatIndex == 0:     # # 0/所有格式
            haveFind = True
        elif self.__formatIndex == 1:   # 1/PSD+AI
            if describe.find('PSD') > -1 or describe.find('AI') > -1:
                haveFind = True
        elif self.__formatIndex == 2:   # 2/PSD
            if describe.find('PSD') > -1 or describe.find('AI') > -1:
                haveFind = True
        elif self.__formatIndex == 3:   # 3/AI
            if describe.find('AI') > -1:
                haveFind = True
        elif self.__formatIndex == 4:   # 4/EPS
            if describe.find('EPS') > -1:
                haveFind = True
        if haveFind is False:
            return None

        strExt = ''
        if describe.find('PSD') > -1:
            strExt = '_PSD'

        if describe.find('AI') > -1:
            strExt += '_AI'
        if describe.find('EPS') > -1:
            strExt += '_EPS'

        a = TxtDiv.find('a')
        url = a.attrs['href']
        return strExt, url
