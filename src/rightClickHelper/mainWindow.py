#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__all__ = ['MainWindow']

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect
from PyQt5.uic.properties import QtWidgets

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

    def _initData(self):
        self.mDrag = False

        from src.rightClickHelper.config import configData
        self.appTitle\
            .setText(configData['appName'])
        self.appVersion\
            .setText(configData['appVersion'])
        self.appMode\
            .setText(configData['appMode'])

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

    def initToolBar(self):
        def windowClick(element):
            def __windowClick(event):
                if event.buttons() == QtCore.Qt.LeftButton:
                    element.clickType = QtCore.Qt.LeftButton
                element.down = True
            return __windowClick

        def windowRelease(element):
            def __windowRelease(event):
                if element.clickType == QtCore.Qt.LeftButton:
                    if element == self.closeWindow and element.down:
                        self.close()
                    elif element == self.minWindow and element.down:
                        self.showMinimized()
                element.down = False
            return __windowRelease

        def connectClick(element: QtWidgets, fun):
            element.mousePressEvent = fun

        def connectRelease(element: QtWidgets, fun):
            element.mouseReleaseEvent = fun

        for ele in [self.closeWindow, self.minWindow]:
            connectClick(ele, windowClick(ele))
            connectRelease(ele, windowRelease(ele))

    def _initEvent(self):
        self.initToolBar()
