# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../src/rightClickHelper/view/mainInterFace.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 740)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 740))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setMouseTracking(False)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        MainWindow.setStyleSheet("#MainWindow{\n"
"    background-color: rgb(0, 0, 0);\n"
"}\n"
"")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.main = QtWidgets.QWidget(MainWindow)
        self.main.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.main.setStyleSheet("#main{\n"
"    background-color: rgb(255,255,255);\n"
"    margin:10px;\n"
"    border-radius: 10px;\n"
"}")
        self.main.setObjectName("main")
        self.headBar = QtWidgets.QWidget(self.main)
        self.headBar.setGeometry(QtCore.QRect(20, 20, 1161, 41))
        self.headBar.setStyleSheet("#appIcon {\n"
"    border: none;\n"
"    border-image: url(:/icon/image/icon/right-click-helper.ico);\n"
"}\n"
"\n"
"#minWindow {\n"
"    border-image: url(:/ico/image/common-icon/min.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"#minWindow:hover {\n"
"    border-image: url(:/ico/image/common-icon/min-ed.png);\n"
"}\n"
"\n"
"#closeWindow {\n"
"    border-image: url(:/ico/image/common-icon/close.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"#closeWindow:hover {\n"
"    border-image: url(:/ico/image/common-icon/close-ed.png);\n"
"}\n"
"")
        self.headBar.setObjectName("headBar")
        self.layoutWidget = QtWidgets.QWidget(self.headBar)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1161, 40))
        self.layoutWidget.setObjectName("layoutWidget")
        self.headBar_w = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.headBar_w.setContentsMargins(0, 0, 0, 0)
        self.headBar_w.setSpacing(0)
        self.headBar_w.setObjectName("headBar_w")
        self.topRight = QtWidgets.QHBoxLayout()
        self.topRight.setSpacing(10)
        self.topRight.setObjectName("topRight")
        self.appIcon = QtWidgets.QGraphicsView(self.layoutWidget)
        self.appIcon.setMaximumSize(QtCore.QSize(36, 36))
        self.appIcon.setStyleSheet("")
        self.appIcon.setObjectName("appIcon")
        self.topRight.addWidget(self.appIcon)
        self.appTitle = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.appTitle.setFont(font)
        self.appTitle.setObjectName("appTitle")
        self.topRight.addWidget(self.appTitle)
        self.appVersion = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.appVersion.setFont(font)
        self.appVersion.setObjectName("appVersion")
        self.topRight.addWidget(self.appVersion)
        self.appMode = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.appMode.setFont(font)
        self.appMode.setObjectName("appMode")
        self.topRight.addWidget(self.appMode)
        self.headBar_w.addLayout(self.topRight)
        spacerItem = QtWidgets.QSpacerItem(400, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.headBar_w.addItem(spacerItem)
        self.topLeft = QtWidgets.QHBoxLayout()
        self.topLeft.setSpacing(10)
        self.topLeft.setObjectName("topLeft")
        self.minWindow = QtWidgets.QGraphicsView(self.layoutWidget)
        self.minWindow.setMaximumSize(QtCore.QSize(24, 24))
        self.minWindow.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.minWindow.setStyleSheet("")
        self.minWindow.setObjectName("minWindow")
        self.topLeft.addWidget(self.minWindow)
        self.closeWindow = QtWidgets.QGraphicsView(self.layoutWidget)
        self.closeWindow.setMaximumSize(QtCore.QSize(24, 24))
        self.closeWindow.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.closeWindow.setStyleSheet("")
        self.closeWindow.setObjectName("closeWindow")
        self.topLeft.addWidget(self.closeWindow)
        self.headBar_w.addLayout(self.topLeft)
        self.headBar_w.setStretch(0, 1)
        self.headBar_w.setStretch(1, 10)
        self.content = QtWidgets.QWidget(self.main)
        self.content.setGeometry(QtCore.QRect(20, 70, 1161, 651))
        self.content.setObjectName("content")
        MainWindow.setCentralWidget(self.main)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AL-IDE"))
        self.appTitle.setText(_translate("MainWindow", "Right Click Helper"))
        self.appVersion.setText(_translate("MainWindow", "1.0.0.0"))
        self.appMode.setText(_translate("MainWindow", "Mod"))
        self.minWindow.setToolTip(_translate("MainWindow", "<html><head/><body><p>最小化</p></body></html>"))
        self.minWindow.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.closeWindow.setToolTip(_translate("MainWindow", "<html><head/><body><p>关闭</p></body></html>"))
        self.closeWindow.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
from src.resource import main_rc
