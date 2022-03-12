import os
import datetime
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog
from renameUi import Ui_cameraRename
from processExif import processExif


class renameWnd(QtWidgets.QWidget, Ui_cameraRename):
    def __init__(self):
        super(renameWnd, self).__init__()
        self.setupUi(self)
        self.pushBtnBrowser.clicked.connect(self.browserFolder)
        self.pushBtnOk.clicked.connect(self.processPhoto)
        # self.lineEditFolder.setText("G:\\New folder")
        self.lineEditFolder.setText(os.getcwd())
        self.__thread = None

    def browserFolder(self):
        folderName = QFileDialog.getExistingDirectory(self, "选取要处理的文件夹", os.getcwd())
        self.lineEditFolder.setText(folderName)

    def processTip(self, strTip):
        self.textBrowser.append(strTip)
        self.textBrowser.forward()

    def processEnd(self):
        # self.processTip(self, "运行结束")
        self.lineEditFolder.setEnabled(True)
        self.pushBtnBrowser.setEnabled(True)
        self.pushBtnOk.setEnabled(True)
        self.textBrowser.append("\n")
        self.textBrowser.append("运行结束")

    def processPhoto(self):
        # self.textBrowser.setText("/home/x/Pictures/NEF")
        path = self.lineEditFolder.text()

        if self.__thread and self.__thread.isRunning():
            self.processTip("正在运行中")
            return

        # self.__thread = processExif(path, self.processTip, self.processEnd)
        self.__thread = processExif(path)
        self.__thread.tipSignal.connect(self.processTip)
        self.__thread.endSignal.connect(self.processEnd)

        self.__thread.start()

        self.lineEditFolder.setEnabled(False)
        self.pushBtnBrowser.setEnabled(False)
        self.pushBtnOk.setEnabled(False)
        self.textBrowser.setText("")

    # 每n秒执行一次
    # def timer(n):
    #     while True:
    #         print(datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
    #         datetime.time.sleep(n)
