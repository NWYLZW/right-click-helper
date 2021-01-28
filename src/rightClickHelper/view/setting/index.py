# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../src/rightClickHelper/view/setting/index.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_setting(object):
    def setupUi(self, setting):
        setting.setObjectName("setting")
        setting.resize(1100, 650)
        setting.setMinimumSize(QtCore.QSize(1100, 650))
        setting.setMaximumSize(QtCore.QSize(1100, 650))
        setting.setStyleSheet("")
        self.verticalLayoutWidget = QtWidgets.QWidget(setting)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1101, 651))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.selLang = ElePySelect(self.verticalLayoutWidget)
        self.selLang.setMinimumSize(QtCore.QSize(120, 0))
        self.selLang.setMaximumSize(QtCore.QSize(120, 16777215))
        self.selLang.setObjectName("selLang")
        self.horizontalLayout_3.addWidget(self.selLang)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.selLogLevel = ElePySelect(self.verticalLayoutWidget)
        self.selLogLevel.setMinimumSize(QtCore.QSize(120, 0))
        self.selLogLevel.setMaximumSize(QtCore.QSize(120, 16777215))
        self.selLogLevel.setObjectName("selLogLevel")
        self.horizontalLayout_4.addWidget(self.selLogLevel)
        self.openLogFileBtn = ElePyButton(self.verticalLayoutWidget)
        self.openLogFileBtn.setObjectName("openLogFileBtn")
        self.horizontalLayout_4.addWidget(self.openLogFileBtn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkoutUpdateBtn = ElePyButton(self.verticalLayoutWidget)
        self.checkoutUpdateBtn.setObjectName("checkoutUpdateBtn")
        self.horizontalLayout_2.addWidget(self.checkoutUpdateBtn)
        self.isAutoCheck = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(10)
        self.isAutoCheck.setFont(font)
        self.isAutoCheck.setObjectName("isAutoCheck")
        self.horizontalLayout_2.addWidget(self.isAutoCheck)
        self.isAutoCheckBeta = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(10)
        self.isAutoCheckBeta.setFont(font)
        self.isAutoCheckBeta.setObjectName("isAutoCheckBeta")
        self.horizontalLayout_2.addWidget(self.isAutoCheckBeta)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)

        self.retranslateUi(setting)
        QtCore.QMetaObject.connectSlotsByName(setting)

    def retranslateUi(self, setting):
        _translate = QtCore.QCoreApplication.translate
        setting.setWindowTitle(_translate("setting", "Form"))
        self.label_2.setText(_translate("setting", "常规"))
        self.label_3.setText(_translate("setting", "语言"))
        self.label_4.setText(_translate("setting", "日志"))
        self.openLogFileBtn.setText(_translate("setting", "打开日志文件夹"))
        self.label.setText(_translate("setting", "更新"))
        self.checkoutUpdateBtn.setText(_translate("setting", "手动检查"))
        self.isAutoCheck.setText(_translate("setting", "启动自动检查更新"))
        self.isAutoCheckBeta.setText(_translate("setting", "更新至Beta版本"))
from src.rightClickHelper.component.form.elePyButton import ElePyButton
from src.rightClickHelper.component.form.elePySelect import ElePySelect
