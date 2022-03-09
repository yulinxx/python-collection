import os

from PyQt6.QtWidgets import QMainWindow, QFileDialog

from downThread import DownThread
from sccnnDownloadUI import Ui_Dialog


class MainWindow(QMainWindow, Ui_Dialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__strSearchWord = ''
        self.__strSavePath = ''

        self.__downThread = None

        self.setupUi(self)
        self.pushBtnDown.clicked.connect(self.slotDown)
        self.pushBtnCancle.clicked.connect(self.slotCancle)
        self.pushBtnBrowser.clicked.connect(self.slotBrowserFolder)
        self.lineEditSavePath.setText(os.getcwd())

    def __del__(self):
        if self.__downThread:
            pass
            # self.__downThread.

    def slotBrowserFolder(self):
        folderName = QFileDialog.getExistingDirectory(self, "选取要保存的位置", os.getcwd())
        self.lineEditSavePath.setText(folderName)

    def slotDown(self):
        self.__strSearchWord = self.lineEditKeyWord.text()
        self.__strSavePath = self.lineEditSavePath.text()

        # 开僻一个新线程
        if self.__downThread and self.__downThread.isRunning():
            self.processTip("正在运行中")
            return

        # self.__thread = processExif(path, self.processTip, self.processEnd)
        self.__downThread = DownThread(self.__strSearchWord, self.__strSavePath)
        self.__downThread.tipSignal.connect(self.processTip)
        self.__downThread.endSignal.connect(self.processEnd)

        self.__downThread.start()

        self.lineEditFolder.setEnabled(False)
        self.pushBtnBrowser.setEnabled(False)
        self.pushBtnOk.setEnabled(False)
        self.textBrowser.setText("")

    def slotCancle(self):
        # 关闭下载线程
        while self.__downThread and self.__downThread.isRunning():
            self.__downThread.stop()

    def processTip(self, info):
        self.textInfo.setText(info)

    def processEnd(self):
        self.textInfo.setText('已停止')
