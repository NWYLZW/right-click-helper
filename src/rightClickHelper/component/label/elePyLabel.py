#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QLabel

from src.rightClickHelper.component.elePyWidget import ElePyWidget
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
        super().__init__(parent, properties)
