# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainInterFace.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


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
"}")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.main = QtWidgets.QWidget(MainWindow)
        self.main.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.main.setStyleSheet("#main{\n"
"    margin: 10px;\n"
"    border-radius: 10px;\n"
"    background-color: rgb(255,255,255);\n"
"}")
        self.main.setObjectName("main")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.main)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1201, 741))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.mainVL = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.mainVL.setContentsMargins(10, 0, 10, 10)
        self.mainVL.setSpacing(0)
        self.mainVL.setObjectName("mainVL")
        self.headBar = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.headBar.setMaximumSize(QtCore.QSize(16777215, 50))
        self.headBar.setStyleSheet("#headBar {\n"
"    border-top-left-radius: 10px;\n"
"    border-top-right-radius: 10px;\n"
"    background-color: qlineargradient(spread:reflect, x1:0, y1:0.511, x2:1, y2:0.489, stop:0 rgba(0, 198, 251, 255), stop:1 rgba(0, 91, 234, 255));\n"
"    border-bottom: 1px solid rgba(0, 91, 234, 255);\n"
"}\n"
"#appIcon {\n"
"    border: none;\n"
"    border-image: url(:/icon/image/icon/right-click-helper.ico);\n"
"}\n"
"\n"
"#minWindow {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/min.png);\n"
"}\n"
"#minWindow:hover {\n"
"    border-image: url(:/ico/image/common-icon/min-ed.png);\n"
"}\n"
"\n"
"#closeWindow {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/close.png);\n"
"}\n"
"#closeWindow:hover {\n"
"    border-image: url(:/ico/image/common-icon/close-ed.png);\n"
"}\n"
"")
        self.headBar.setObjectName("headBar")
        self.layoutWidget = QtWidgets.QWidget(self.headBar)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1181, 51))
        self.layoutWidget.setObjectName("layoutWidget")
        self.headBar_w = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.headBar_w.setContentsMargins(5, 5, 5, 5)
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
        self.minWindow = QtWidgets.QPushButton(self.layoutWidget)
        self.minWindow.setMinimumSize(QtCore.QSize(24, 24))
        self.minWindow.setMaximumSize(QtCore.QSize(24, 24))
        self.minWindow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.minWindow.setText("")
        self.minWindow.setObjectName("minWindow")
        self.topLeft.addWidget(self.minWindow)
        self.closeWindow = QtWidgets.QPushButton(self.layoutWidget)
        self.closeWindow.setMinimumSize(QtCore.QSize(24, 24))
        self.closeWindow.setMaximumSize(QtCore.QSize(24, 24))
        self.closeWindow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.closeWindow.setText("")
        self.closeWindow.setObjectName("closeWindow")
        self.topLeft.addWidget(self.closeWindow)
        self.headBar_w.addLayout(self.topLeft)
        self.headBar_w.setStretch(0, 1)
        self.headBar_w.setStretch(1, 10)
        self.mainVL.addWidget(self.headBar)
        self.content = QtWidgets.QHBoxLayout()
        self.content.setContentsMargins(10, 10, 10, 10)
        self.content.setSpacing(10)
        self.content.setObjectName("content")
        self.leftMenu = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.leftMenu.setStyleSheet("#mannagement {\n"
"    border: none;\n"
"    border-image: url(:/icon/image/icon/right-click-helper.ico);\n"
"}\n"
"#about {\n"
"    border: none;\n"
"    border-image: url(:/icon/image/icon/about.png);\n"
"}\n"
"#setting {\n"
"    border: none;\n"
"    border-image: url(:/icon/image/icon/setting.png);\n"
"}\n"
"#warehouse {\n"
"    border: none;\n"
"    border-image: url(:/icon/image/icon/warehouse.png);\n"
"}")
        self.leftMenu.setObjectName("leftMenu")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.leftMenu)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 51, 181))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.leftMenuVL = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.leftMenuVL.setContentsMargins(10, 10, 10, 10)
        self.leftMenuVL.setSpacing(10)
        self.leftMenuVL.setObjectName("leftMenuVL")
        self.mannagement = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.mannagement.setMinimumSize(QtCore.QSize(30, 30))
        self.mannagement.setMaximumSize(QtCore.QSize(30, 30))
        self.mannagement.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mannagement.setText("")
        self.mannagement.setObjectName("mannagement")
        self.leftMenuVL.addWidget(self.mannagement)
        self.warehouse = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.warehouse.setMinimumSize(QtCore.QSize(30, 30))
        self.warehouse.setMaximumSize(QtCore.QSize(30, 30))
        self.warehouse.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.warehouse.setText("")
        self.warehouse.setObjectName("warehouse")
        self.leftMenuVL.addWidget(self.warehouse)
        self.setting = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.setting.setMinimumSize(QtCore.QSize(30, 30))
        self.setting.setMaximumSize(QtCore.QSize(30, 30))
        self.setting.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setting.setText("")
        self.setting.setObjectName("setting")
        self.leftMenuVL.addWidget(self.setting)
        self.about = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.about.setMinimumSize(QtCore.QSize(30, 30))
        self.about.setMaximumSize(QtCore.QSize(30, 30))
        self.about.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.about.setText("")
        self.about.setObjectName("about")
        self.leftMenuVL.addWidget(self.about)
        self.content.addWidget(self.leftMenu)
        self.showPage = ManagementController(self.verticalLayoutWidget)
        self.showPage.setObjectName("showPage")
        self.content.addWidget(self.showPage)
        self.content.setStretch(0, 1)
        self.content.setStretch(1, 22)
        self.mainVL.addLayout(self.content)
        MainWindow.setCentralWidget(self.main)

        self.retranslateUi(MainWindow)
        self.minWindow.clicked.connect(MainWindow.hide)
        self.closeWindow.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AL-IDE"))
        self.appTitle.setText(_translate("MainWindow", "Right Click Helper"))
        self.appVersion.setText(_translate("MainWindow", "1.0.0.0"))
        self.appMode.setText(_translate("MainWindow", "Mod"))
from src.rightClickHelper.controller.management.controller import ManagementController
import main_rc
