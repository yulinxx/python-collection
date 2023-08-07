import os
import datetime
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog
from move_files import Ui_moveFilesDlg
from moveFilesThread import moveFilesThread

class mainWindow(QtWidgets.QWidget, Ui_moveFilesDlg):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)
        self.pushBtnBrowser.clicked.connect(self.browserFolder)
        self.pushBtnOk.clicked.connect(self.processFiles)
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

    def processFiles(self):
        path = self.lineEditFolder.text()

        if self.__thread and self.__thread.isRunning():
            self.processTip("正在运行中")
            return

        self.__thread = moveFilesThread(path)
        self.__thread.tipSignal.connect(self.processTip)
        self.__thread.endSignal.connect(self.processEnd)

        self.__thread.start()

        self.lineEditFolder.setEnabled(False)
        self.pushBtnBrowser.setEnabled(False)
        self.pushBtnOk.setEnabled(False)
        self.textBrowser.setText("")

