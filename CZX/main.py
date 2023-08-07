import sys
from PyQt6 import QtWidgets
from mainWindow import mainWindow

# pyinstaller -F -w  renameMain.py
# pyuic5 -o d:\ui.py D:\xx\Documents\QtProj\UIForPython\mainwindow.ui

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWindow()
    ui.show()
    sys.exit(app.exec())
