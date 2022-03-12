# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/x/source/Python/renameExif/rename.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_cameraRename(object):
    def setupUi(self, cameraRename):
        cameraRename.setObjectName("cameraRename")
        cameraRename.resize(524, 290)
        self.horizontalLayout = QtWidgets.QHBoxLayout(cameraRename)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(cameraRename)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.HLayoutBrowser = QtWidgets.QHBoxLayout()
        self.HLayoutBrowser.setObjectName("HLayoutBrowser")
        self.lineEditFolder = QtWidgets.QLineEdit(cameraRename)
        self.lineEditFolder.setObjectName("lineEditFolder")
        self.HLayoutBrowser.addWidget(self.lineEditFolder)
        self.pushBtnBrowser = QtWidgets.QPushButton(cameraRename)
        self.pushBtnBrowser.setObjectName("pushBtnBrowser")
        self.HLayoutBrowser.addWidget(self.pushBtnBrowser)
        self.pushBtnOk = QtWidgets.QPushButton(cameraRename)
        self.pushBtnOk.setObjectName("pushBtnOk")
        self.HLayoutBrowser.addWidget(self.pushBtnOk)
        self.HLayoutBrowser.setStretch(0, 8)
        self.HLayoutBrowser.setStretch(1, 1)
        self.HLayoutBrowser.setStretch(2, 1)
        self.verticalLayout.addLayout(self.HLayoutBrowser)
        self.textBrowser = QtWidgets.QTextBrowser(cameraRename)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(cameraRename)
        QtCore.QMetaObject.connectSlotsByName(cameraRename)

    def retranslateUi(self, cameraRename):
        _translate = QtCore.QCoreApplication.translate
        cameraRename.setWindowTitle(_translate("cameraRename", "照片命名工具"))
        self.label.setText(_translate("cameraRename", "重命名目录:"))
        self.pushBtnBrowser.setText(_translate("cameraRename", "浏览..."))
        self.pushBtnOk.setText(_translate("cameraRename", "执行"))
        self.textBrowser.setHtml(_translate("cameraRename", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">本工具自动将相机的照片日期提取</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">并将现在的文件以年月日时分秒命名</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">若一秒钟有多张照片</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">则在后面累加</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">cppdpp@protonmail.com</span></p></body></html>"))
