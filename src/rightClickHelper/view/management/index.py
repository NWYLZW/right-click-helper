# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../src/rightClickHelper/view/management/index.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_management(object):
    def setupUi(self, management):
        management.setObjectName("management")
        management.resize(1100, 649)
        management.setMinimumSize(QtCore.QSize(1100, 649))
        management.setMaximumSize(QtCore.QSize(1100, 650))
        management.setStyleSheet("QScrollBar:vertical {\n"
"    background-color: rgb(250, 250, 250);\n"
"    width: 6px;\n"
"    margin: 0px;border: none;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background-color: rgb(216, 216, 216);\n"
"    min-height: 5px;\n"
"    border-radius: 3px;\n"
"}\n"
"QScrollBar::handle:vertical:hover{background-color: rgb(181, 181, 181);}\n"
"QScrollBar:horizontal {\n"
"    background-color: rgb(250, 250, 250);\n"
"    height: 6px;\n"
"    margin: 0px;border: none;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background-color: rgb(216, 216, 216);\n"
"    min-width: 5px;\n"
"    border-radius: 3px;\n"
"}\n"
"QScrollBar::handle:horizontal:hover{background-color: rgb(181, 181, 181);}\n"
"\n"
"QScrollBar::up-arrow, QScrollBar::down-arrow,\n"
"QScrollBar::right-arrow, QScrollBar::left-arrow,\n"
"QScrollBar::add-page, QScrollBar::sub-page,\n"
"QScrollBar::add-line, QScrollBar::sub-line {\n"
"    border: none;background: none;color: none;height: 0;\n"
"}")
        self.verticalLayoutWidget = QtWidgets.QWidget(management)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1091, 641))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.management_w = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.management_w.setContentsMargins(0, 0, 0, 0)
        self.management_w.setSpacing(5)
        self.management_w.setObjectName("management_w")
        self.head = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.head.setStyleSheet("#home {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/home.png);\n"
"}\n"
"#home:hover {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/home-ed.png);\n"
"}\n"
"\n"
"#upPackage {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/back.png);\n"
"}\n"
"#upPackage:hover {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/back-ed.png);\n"
"}\n"
"\n"
"#refresh {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/refresh.png);\n"
"}\n"
"#refresh:hover {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/refresh-ed.png);\n"
"}\n"
"\n"
"#more {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/more.png);\n"
"}\n"
"#more:hover {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/more-ed.png);\n"
"}\n"
"\n"
"QLineEdit {\n"
"    padding-left: 8px;\n"
"    padding-top: 4px; padding-bottom: 4px;\n"
"\n"
"    border-radius: 4px;\n"
"    border: 1px solid rgb(220, 223, 230);\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 1px solid rgb(64, 158, 255);\n"
"}")
        self.head.setObjectName("head")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.head)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1091, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.headHL = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.headHL.setContentsMargins(10, 0, 10, 0)
        self.headHL.setSpacing(10)
        self.headHL.setObjectName("headHL")
        self.home = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.home.setMinimumSize(QtCore.QSize(20, 20))
        self.home.setMaximumSize(QtCore.QSize(20, 20))
        self.home.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.home.setText("")
        self.home.setObjectName("home")
        self.headHL.addWidget(self.home)
        self.upPackage = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.upPackage.setMinimumSize(QtCore.QSize(20, 20))
        self.upPackage.setMaximumSize(QtCore.QSize(20, 20))
        self.upPackage.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.upPackage.setText("")
        self.upPackage.setObjectName("upPackage")
        self.headHL.addWidget(self.upPackage)
        self.refresh = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.refresh.setMinimumSize(QtCore.QSize(20, 20))
        self.refresh.setMaximumSize(QtCore.QSize(20, 20))
        self.refresh.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.refresh.setText("")
        self.refresh.setObjectName("refresh")
        self.headHL.addWidget(self.refresh)
        self.currentRegPath = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.currentRegPath.setMinimumSize(QtCore.QSize(600, 0))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.currentRegPath.setFont(font)
        self.currentRegPath.setObjectName("currentRegPath")
        self.headHL.addWidget(self.currentRegPath)
        self.more = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.more.setMinimumSize(QtCore.QSize(20, 20))
        self.more.setMaximumSize(QtCore.QSize(20, 20))
        self.more.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.more.setText("")
        self.more.setObjectName("more")
        self.headHL.addWidget(self.more)
        self.searchLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(10)
        self.searchLabel.setFont(font)
        self.searchLabel.setObjectName("searchLabel")
        self.headHL.addWidget(self.searchLabel)
        self.searchInput = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.searchInput.setObjectName("searchInput")
        self.headHL.addWidget(self.searchInput)
        self.selKind = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.selKind.setMinimumSize(QtCore.QSize(100, 0))
        self.selKind.setObjectName("selKind")
        self.selKind.addItem("")
        self.selKind.addItem("")
        self.selKind.addItem("")
        self.selKind.addItem("")
        self.selKind.addItem("")
        self.headHL.addWidget(self.selKind)
        self.management_w.addWidget(self.head)
        self.itemScrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget)
        self.itemScrollArea.setStyleSheet("#itemScrollArea {\n"
"    border: none;\n"
"    background-color: rgb(250, 250, 250);\n"
"}\n"
"\n"
"#itemScrollAreaWidget {\n"
"    background-color: rgb(250, 250, 250);\n"
"}")
        self.itemScrollArea.setWidgetResizable(True)
        self.itemScrollArea.setObjectName("itemScrollArea")
        self.itemScrollAreaWidget = QtWidgets.QWidget()
        self.itemScrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 1089, 594))
        self.itemScrollAreaWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.itemScrollAreaWidget.setAutoFillBackground(False)
        self.itemScrollAreaWidget.setObjectName("itemScrollAreaWidget")
        self.itemScrollArea.setWidget(self.itemScrollAreaWidget)
        self.management_w.addWidget(self.itemScrollArea)
        self.management_w.setStretch(0, 1)
        self.management_w.setStretch(1, 15)

        self.retranslateUi(management)
        QtCore.QMetaObject.connectSlotsByName(management)

    def retranslateUi(self, management):
        _translate = QtCore.QCoreApplication.translate
        management.setWindowTitle(_translate("management", "Form"))
        self.currentRegPath.setText(_translate("management", "文件夹/"))
        self.searchLabel.setText(_translate("management", "搜索"))
        self.selKind.setItemText(0, _translate("management", "文件"))
        self.selKind.setItemText(1, _translate("management", "文件夹"))
        self.selKind.setItemText(2, _translate("management", "目录"))
        self.selKind.setItemText(3, _translate("management", "目录背景"))
        self.selKind.setItemText(4, _translate("management", "桌面背景"))
from src.resource import main_rc
