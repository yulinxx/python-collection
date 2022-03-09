# 开头加上导入sys
import sys
from PyQt6 import QtWidgets
from mainWindow import MainWindow

# pyuic6 -o E:\pyProj\python-collection\sccnnDownloadUI.py  E:\pyProj\python-collection\sccnnDownload.ui

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    wnd = MainWindow()
    wnd.show()

    sys.exit(app.exec())
