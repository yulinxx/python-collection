import os

from PyQt6.QtWidgets import QFileDialog, QDialog

from downThread import DownThread
from sccnnDownloadUI import Ui_Dialog


class MainWindow(QDialog, Ui_Dialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__strSearchWord = ''
        self.__strSavePath = ''
        self.__downThread = None

        self.setupUi(self)

        self.pushBtnBrowser.clicked.connect(self.slotBrowserFolder)
        self.pushBtnTestPages.clicked.connect(self.slotTestPages)
        self.pushBtnDown.clicked.connect(self.slotDown)
        self.lineEditSavePath.setText(os.getcwd())

    def __del__(self):
        if self.__downThread:
            pass
            # self.__downThread.

    def slotBrowserFolder(self):
        """浏览存储路径"""
        folderName = QFileDialog.getExistingDirectory(self, "选取要保存的位置", os.getcwd())
        self.lineEditSavePath.setText(folderName)

    def slotTestPages(self):
        """获取页数"""
        self.initThread()
        pages = self.__downThread.getPages()
        # self.textInfo.append(f'搜索 {self.lineEditKeyWord.text()}, 得到 {pages} 页, 大约共 {pages * 12} 个文件')

    def stopDownload(self):
        # 若在运行则关闭下载线程
        if self.__downThread and self.__downThread.isRunning():
            self.progressBar.setValue(0)
            self.progressBar.setVisible(False)
            self.__downThread.stop()
            self.pushBtnDown.setText("开始下载")
            return True
        return False

    def initThread(self):
        if self.__downThread is None:
            self.__downThread = DownThread()

            self.__downThread.tipSignal.connect(self.slotProcessTip)
            self.__downThread.tipDownProcess.connect(self.slotDownProcess)
            self.__downThread.endSignal.connect(self.slotProcessEnd)

        self.__strSearchWord = self.lineEditKeyWord.text()
        self.__strSavePath = self.lineEditSavePath.text()

        self.__downThread.setDownKeyword(self.__strSearchWord)
        self.__downThread.setSavePath(self.__strSavePath)
        self.__downThread.setDownFormat(self.cmbFormat.currentIndex())

    def startDownload(self):
        self.textInfo.setText('')
        self.progressBar.setVisible(True)
        self.progressBar.setValue(0)

        self.initThread()

        if len(self.__strSearchWord) < 1 and len(self.__strSavePath) < 1:
            self.textInfo.append('请输入')
            return

        # 开僻一个新线程
        if self.__downThread and self.__downThread.isRunning():
            self.slotProcessTip("正在运行中")
            return

        # self.__thread = processExif(path, self.slotProcessTip, self.slotProcessEnd)


        try:
            self.__downThread.setDownCount(int(self.cmbDownCount.currentText()))
        except:
            self.__downThread.setDownCount(9999)
            pass

        pageCount = self.__downThread.getPages()

        if pageCount < 1:
            self.textInfo.setText('未搜索到任何结果')
            return

        self.__downThread.start()

        self.pushBtnDown.setText("停止下载")
        self.setUIEnable(False)

    def slotDown(self):
        if self.stopDownload():
            return

        self.startDownload()

    def slotProcessTip(self, info):
        self.textInfo.append(info)

    def slotDownProcess(self, percent):
        self.progressBar.setValue(percent)

    def setUIEnable(self, enable):
        self.lineEditKeyWord.setEnabled(enable)
        self.lineEditSavePath.setEnabled(enable)
        self.pushBtnBrowser.setEnabled(enable)

        self.cmbFormat.setEnabled(enable)
        self.cmbDownCount.setEnabled(enable)

    def slotProcessEnd(self):
        self.setUIEnable(True)
