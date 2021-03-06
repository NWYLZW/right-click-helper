# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../src/rightClickHelper/view/management/menuItemCard_package.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_item(object):
    def setupUi(self, item):
        item.setObjectName("item")
        item.resize(120, 180)
        item.setMinimumSize(QtCore.QSize(120, 180))
        item.setMaximumSize(QtCore.QSize(120, 180))
        item.setStyleSheet("#item {\n"
"    background-color: rgb(0, 0, 0);\n"
"}\n"
"#main {\n"
"    border-radius: 10px;\n"
"    background-color: rgb(255, 255, 255);\n"
"}\n"
"#maskCard {\n"
"    border-radius: 10px;\n"
"    background-color: rgba(0, 0, 0, 50);\n"
"}\n"
"\n"
"#edit {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/edit.png);\n"
"}\n"
"#edit:hover {\n"
"    border-image: url(:/ico/image/common-icon/edit-ed.png);\n"
"}\n"
"\n"
"#switchItem {\n"
"    border: none;\n"
"}\n"
"#switchItem[status=\'open\'] {\n"
"    border-image: url(:/ico/image/switch-open.png);\n"
"}\n"
"#switchItem[status=\'close\'] {\n"
"    border-image: url(:/ico/image/switch-close.png);\n"
"}\n"
"\n"
"#more {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/more.png);\n"
"}\n"
"#more:hover {\n"
"    border-image: url(:/ico/image/common-icon/more-ed.png);\n"
"}")
        self.main = QtWidgets.QWidget(item)
        self.main.setGeometry(QtCore.QRect(0, 0, 120, 180))
        self.main.setMinimumSize(QtCore.QSize(120, 180))
        self.main.setStyleSheet("#main {\n"
"    margin: 10px;\n"
"}")
        self.main.setObjectName("main")
        self.title = QtWidgets.QLabel(self.main)
        self.title.setGeometry(QtCore.QRect(20, 110, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.title.setObjectName("title")
        self.icon = QtWidgets.QWidget(self.main)
        self.icon.setGeometry(QtCore.QRect(20, 20, 80, 80))
        self.icon.setObjectName("icon")
        self.gridLayoutWidget = QtWidgets.QWidget(self.icon)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 81, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.showMain = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.showMain.setContentsMargins(0, 0, 0, 0)
        self.showMain.setSpacing(4)
        self.showMain.setObjectName("showMain")
        self.icon_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.icon_2.setText("")
        self.icon_2.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_2.setObjectName("icon_2")
        self.showMain.addWidget(self.icon_2, 0, 1, 1, 1)
        self.icon_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.icon_1.setText("")
        self.icon_1.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_1.setObjectName("icon_1")
        self.showMain.addWidget(self.icon_1, 0, 0, 1, 1)
        self.icon_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.icon_3.setText("")
        self.icon_3.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_3.setObjectName("icon_3")
        self.showMain.addWidget(self.icon_3, 1, 0, 1, 1)
        self.icon_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.icon_4.setText("")
        self.icon_4.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_4.setObjectName("icon_4")
        self.showMain.addWidget(self.icon_4, 1, 1, 1, 1)
        self.showIcon = QtWidgets.QLabel(self.main)
        self.showIcon.setGeometry(QtCore.QRect(10, 80, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.showIcon.setFont(font)
        self.showIcon.setAlignment(QtCore.Qt.AlignCenter)
        self.showIcon.setObjectName("showIcon")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.main)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 140, 101, 21))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.switchItem = QtWidgets.QGraphicsView(self.horizontalLayoutWidget_2)
        self.switchItem.setMinimumSize(QtCore.QSize(30, 15))
        self.switchItem.setMaximumSize(QtCore.QSize(30, 15))
        self.switchItem.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.switchItem.setToolTip("")
        self.switchItem.setStyleSheet("")
        self.switchItem.setObjectName("switchItem")
        self.horizontalLayout.addWidget(self.switchItem)
        self.edit = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.edit.setMinimumSize(QtCore.QSize(16, 16))
        self.edit.setMaximumSize(QtCore.QSize(16, 16))
        self.edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.edit.setText("")
        self.edit.setObjectName("edit")
        self.horizontalLayout.addWidget(self.edit)
        self.more = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.more.setMinimumSize(QtCore.QSize(16, 16))
        self.more.setMaximumSize(QtCore.QSize(16, 16))
        self.more.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.more.setToolTip("")
        self.more.setText("")
        self.more.setObjectName("more")
        self.horizontalLayout.addWidget(self.more)

        self.retranslateUi(item)
        QtCore.QMetaObject.connectSlotsByName(item)

    def retranslateUi(self, item):
        _translate = QtCore.QCoreApplication.translate
        item.setWindowTitle(_translate("item", "Form"))
        self.title.setText(_translate("item", "标题"))
        self.showIcon.setText(_translate("item", "I"))
        self.edit.setToolTip(_translate("item", "编辑"))
from src.resource import main_rc
