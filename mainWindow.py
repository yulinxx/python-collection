import os

from PyQt6.QtWidgets import QMainWindow, QFileDialog
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

    def __del__(self):
        if self.__downThread:
            pass
            #self.__downThread.

    def slotBrowserFolder(self):
        folderName = QFileDialog.getExistingDirectory(self, "选取要保存的位置", os.getcwd() )
        self.lineEditSavePath.setText(folderName)

    def slotDown(self):
        self.__strSearchWord = self.lineEditKeyWord.text()
        self.__strSavePath = self.lineEditSavePath.text()

        # 开僻一个新线程


    def slotCancle(self):
        # 关闭下载线程
        pass