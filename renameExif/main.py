import sys
from PyQt6 import QtWidgets
from renameWnd import renameWnd

# pyinstaller -F -w  renameMain.py

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = renameWnd()
    ui.show()
    sys.exit(app.exec())
