# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../src/rightClickHelper/view/management/menuItemCard_new.ui'
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
"\n"
"#addBtn {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/add-item.png);\n"
"}\n"
"#addBtn:hover {\n"
"    border-image: url(:/ico/image/add-item-ed.png);\n"
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
"#remove {\n"
"    border: none;\n"
"    border-image: url(:/ico/image/common-icon/delete.png);\n"
"}\n"
"#remove:hover {\n"
"    border-image: url(:/ico/image/common-icon/delete-ed.png);\n"
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
"    margin-top: 40px;\n"
"    margin-bottom: 40px;\n"
"}")
        self.main.setObjectName("main")
        self.addBtn = QtWidgets.QPushButton(self.main)
        self.addBtn.setGeometry(QtCore.QRect(20, 50, 81, 81))
        self.addBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addBtn.setText("")
        self.addBtn.setObjectName("addBtn")

        self.retranslateUi(item)
        QtCore.QMetaObject.connectSlotsByName(item)

    def retranslateUi(self, item):
        _translate = QtCore.QCoreApplication.translate
        item.setWindowTitle(_translate("item", "Form"))
from src.resource import main_rc
