# 开头加上导入sys
import sys
from PyQt6 import QtWidgets

# pyuic6 -o  E:\pyProj\python-collection\sccnnDownload\sccnnDownloadUI.py  E:\pyProj\python-collection\sccnnDownload\sccnnDownload.ui

from mainWindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    wnd = MainWindow()
    wnd.show()

    sys.exit(app.exec())
