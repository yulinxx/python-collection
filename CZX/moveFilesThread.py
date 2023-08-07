import os
import re
import time
from PyQt6.QtCore import QThread, pyqtSignal


class moveFilesThread(QThread):
    __index = 1
    __listName = []
    tipSignal = pyqtSignal(str)
    endSignal = pyqtSignal()

    def __init__(self, path):
        super(moveFilesThread, self).__init__()
        self.__searchPath = path

    def run(self):
        self.__listName = []
        # self.__funcTip("---------------------------------------------\n")
        start = time.time()
        # self.__funcTip("开始..." )
        self.process()

        end = time.time()
        # self.__funcTip("结束...%s 耗时" % (end - start))
        tmDuration = ('%.2f' % (end - start))
        self.tipSignal.emit("结束, 共耗时:%s " % tmDuration)
        # self.__funcTip("---------------------------------------------\n")
        self.tipSignal.emit("---------------------------------------------\n")

        # self.__funcEnd()
        self.endSignal.emit()


    def checkID(self, strID):
        '''判断是否为身份证'''
        if strID.len() < 18:
            return False
        # 正则表达式检验格式
        if not re.match(r"^[1-9]\d{5}(19\d{2}|2\d{3})(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])\d{3}[0-9Xx]$", strID):
            return False

        return True
    def process(self):
        fileIDSet = set()

        for curDir, subDirs, fileNames in os.walk(self.__searchPath):
            for fileName in fileNames:
                strID = fileName[0:18]
                if self.checkID(strID):
                    fileIDSet.add(strID)

        for id in fileIDSet:
            os.makedirs(self.__searchPath + "/" + id)

    def __renameImg(self, path, fileName):
        pass

    def __renameVideo(self, path, filename):
        pass
        # self.tipSignal.emit(strLog)

