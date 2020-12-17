#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QFileDialog

from src.rightClickHelper.tool.regTool import RegTool, RegEnv
from src.rightClickHelper.tool.systemTool import SystemTool

class DragLabel(QLabel):
    s_pathChange = QtCore.pyqtSignal(str, name='pathChange')

    def __init__(
        self, parent=None
    ):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self._path = ''
        self.acceptEnds = ['.png', '.jpg', '.jpeg', '.ico', '.exe']

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if ev.buttons() == QtCore.Qt.LeftButton:
            userPicturesPath = RegTool.getVal(
                RegEnv.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders', 'My Pictures'
            ).val
            directoryPath = QFileDialog.getOpenFileName(
                self, self.property('selFileTitle'), userPicturesPath, 'Picture File (*.png *.jpg *.jpeg *.ico);;Application (*.exe)'
            )[0]
            if directoryPath != '':
                self.path = directoryPath

    def dragEnterEvent(self, e):
        print('dragEnterEvent', e)
        for acceptEnd in self.acceptEnds:
            if e.mimeData().text().endswith(
                acceptEnd
            ): e.accept(); break
            else: e.ignore()

    def dropEvent(self, e):
        print('dropEvent', e)
        self.path = e.mimeData().text()\
            .replace('file:///', '')

    def _refreshPixmap(self):
        if self.path == '': return
        try:
            if self.path.endswith('.exe'):
                pixMap = QPixmap(SystemTool.getIcon(self.path))
            else:
                pixMap = QPixmap(self.path)
            if self.property('fullProportion') is None:
                self.setProperty('fullProportion', -1)

            fullProportion = self.property('fullProportion')
            if fullProportion != -1:
                pixMap = pixMap.scaled(
                    self.width() * fullProportion/100
                    , self.height() * fullProportion/100
                )
            self.setPixmap(pixMap)
            self.repaint()
        except Exception as e:
            raise e

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path
        self.setToolTip('[点击修改]' + path)
        self._refreshPixmap()
        self.pathChange.emit(self.path)
