#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from src.rightClickHelper.tool.regTool import systemDir
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
            filePath = SystemTool.getFilePathByQFileDialog(
                self, self.property('selFileTitle'), systemDir['pictures'],
                'Picture File (*.png *.jpg *.jpeg *.ico);;Application (*.exe)'
            )
            if filePath != '':
                self.path = filePath

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
            if self.path.endswith('exe') or re.search(r'\..*,-?\d+$', self.path):
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
