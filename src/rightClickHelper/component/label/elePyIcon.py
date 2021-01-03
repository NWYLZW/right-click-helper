#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from PyQt5.QtCore import Qt

from src.rightClickHelper.component.label.elePyLabel import ElePyLabel

class ElePyIcon(
    ElePyLabel
):
    def __init__(self, parent=None, properties: dict = None):
        super().__init__(parent, properties)

    def _initUi(self):
        super(ElePyIcon, self)._initUi()
        self.setAlignment(Qt.AlignCenter)
        self.setFont(ElePyLabel.ICON_FONT)
        self.setFontPixel()

    def setText(self, text: str) -> None:
        result = re.findall(r'\&\#(.*);', text)
        if result is not None and len(result) > 0:
            text = chr(int('0' + result[0], 16))
        super(ElePyIcon, self).setText(text)

    def setFontPixel(self, pixel: int = 16):
        font = self.font()
        font.setPixelSize(pixel)
        self.setFont(font)
        self.setFixedSize(pixel, pixel)
