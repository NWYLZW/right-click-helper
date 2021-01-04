#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QLabel

from src.rightClickHelper.component.elePyWidget import ElePyWidget

class ElePyLabel(
    QLabel, ElePyWidget
):
    INIT_ICON_FONT: bool = False
    ICON_FONT: QFont     = None

    def __init__(self, parent=None, properties: dict = None):
        if not ElePyLabel.INIT_ICON_FONT:
            ElePyLabel.INIT_ICON_FONT = True

            fontId = QFontDatabase.addApplicationFont(
                os.path.abspath(os.path.join(__file__, '../elePy.ttf'))
            )
            fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
            if len(fontFamilies) > 0:
                fontFamily = fontFamilies[0]
                ElePyLabel.ICON_FONT = QFont(fontFamily)
        super().__init__(parent, properties)
