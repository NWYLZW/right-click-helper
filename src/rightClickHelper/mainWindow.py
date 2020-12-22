#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__all__ = ['MainWindow']

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from src.rightClickHelper.tool.pathTool import PathTool
from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.view import mainInterFace

class MainWindow(QMainWindow, mainInterFace.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # 解决输出窗口打印出“UpdateLayeredWindowIndirect failed for ptDst=xxx”的错误
        self.setWindowFlag(Qt.FramelessWindowHint)

        self._initUI()
        self._initData()
        self._initEvent()

    def _initUI(self):
        self.setupUi(self)
        EffectTool.setBlur(self)

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(PathTool.appPath() + r'\src\resource\image\icon\right-click-helper.ico'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.setWindowIcon(icon)

        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.yijie.rightClickHelper")

    def _initData(self):
        self.mDrag = False

        from src.rightClickHelper.config import configData
        self.appTitle\
            .setPlaceholder(configData['appName'])
        self.appVersion\
            .setPlaceholder(configData['appVersion'])
        self.appMode\
            .setPlaceholder(configData['appMode'])

        # self.test.setPixmap(SystemHelper.getIcon(r'%systemroot%\system32\themecpl.dll,-1'))

    def mousePressEvent(self, event):
        self.mDragPosition = event.globalPos() - self.pos()
        if event.button() == Qt.LeftButton:
            self.mDrag = True
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mDrag:
            self.move(event.globalPos() - self.mDragPosition)
            event.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.mDrag = False

    def _initEvent(self):
        pass
