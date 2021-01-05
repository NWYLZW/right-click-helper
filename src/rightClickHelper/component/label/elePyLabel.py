#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QLabel

from src.rightClickHelper.component.core import LifeStage
from src.rightClickHelper.component.elePyWidget import ElePyWidget, watchProperty
from src.rightClickHelper.tool.pathTool import PathTool

class ElePyLabel(
    QLabel, ElePyWidget
):
    ICON_FONT: QFont     = None

    def __init__(self, parent=None, properties: dict = None):
        if ElePyLabel.ICON_FONT is None:
            fontId = QFontDatabase.addApplicationFont(
                PathTool.appPath() + r'\src\resource\font\elePy.ttf'
            )
            fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
            if len(fontFamilies) > 0:
                fontFamily = fontFamilies[0]
                ElePyLabel.ICON_FONT = QFont(fontFamily)
        self.__initData__ = {}
        super().__init__(parent, properties)

    def _initData(self):
        super(ElePyLabel, self)._initData()
        if self.__initData__.get('text', None):
            self.setText(self.__initData__['text'])

    @watchProperty({'text': {'type': str}})
    def textChange(self, newText, *args):
        if self._lifeStage not in [
            LifeStage.INIT_DATA, LifeStage.INITED
        ]: self.__initData__['text'] = newText
        else: self.setText(newText)
