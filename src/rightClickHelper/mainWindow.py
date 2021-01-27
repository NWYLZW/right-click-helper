#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__all__ = ['MainWindow']

from typing import ClassVar

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from src.rightClickHelper.controller.about import About
from src.rightClickHelper.controller.management import Management
from src.rightClickHelper.controller.setting import Setting
from src.rightClickHelper.tool.pathTool import PathTool
from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.tool.widgetTool import WidgetTool
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

        # self.setCursor(
        #     QtGui.QCursor(
        #         QtGui.QPixmap(PathTool.appPath() + r'\src\resource\image\icon\normal.cur'), 0, 0
        #     )
        # )

        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.yijie.rightClickHelper")

        WidgetTool.setSqss(self.leftMenu, """\
        @mixin image-icon($name, $path)
          ##{$name}
            border-image: url(:/icon/image/icon/#{$path})
        @include image-icon(management, right-click-helper.ico)
        @include image-icon(about,       about.png)
        @include image-icon(setting,     setting.png)
        @include image-icon(warehouse,   warehouse.png)
        """)

    def _initData(self):
        self.mDrag = False

        from src.rightClickHelper.config import configData
        self.appTitle\
            .setText(configData['appName'])
        self.appVersion\
            .setText(configData['appVersion'])
        self.appMode\
            .setText(configData['appMode'])

    def changeShowPage(self, pageName: str):
        pages = {
            'management': Management,
            'setting': Setting,
            'about': About
        }

        def __fun():
            self.showPage.deleteLater()

            clazz: ClassVar = pages.get(pageName)
            self.showPage = clazz(self.verticalLayoutWidget)
            self.showPage.setFixedHeight(
                self.leftMenu.height()
            )
            self.showPage.setObjectName("showPage")
            self.content.addWidget(self.showPage)
        return __fun

    def _initEvent(self):
        def mousePressEvent(event):
            self.mDragPosition = event.globalPos() - self.pos()
            if event.button() == Qt.LeftButton:
                self.mDrag = True
                event.accept()

        def mouseMoveEvent(event):
            if event.buttons() == Qt.LeftButton and self.mDrag:
                self.move(event.globalPos() - self.mDragPosition)
                event.accept()

        def mouseReleaseEvent(QMouseEvent):
            self.mDrag = False

        self.headBar.mousePressEvent   = mousePressEvent
        self.headBar.mouseMoveEvent    = mouseMoveEvent
        self.headBar.mouseReleaseEvent = mouseReleaseEvent

        self.management.clicked.connect(
            self.changeShowPage('management')
        )
        self.setting.clicked.connect(
            self.changeShowPage('setting')
        )
        self.about.clicked.connect(
            self.changeShowPage('about')
        )
