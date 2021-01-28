#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent

from src.rightClickHelper.component.label.elePyLabel import ElePyLabel
from src.rightClickHelper.tool.widgetTool import WidgetTool

class ElePyIcon(
    ElePyLabel
):
    clicked = pyqtSignal()

    def __init__(self, parent=None, properties: dict = None):
        super().__init__(parent, properties)

    def _initUi(self):
        super(ElePyIcon, self)._initUi()
        self.setAlignment(Qt.AlignCenter)
        self.setFont(WidgetTool.getProperty(
            'icon-font', ElePyLabel.ICON_FONT
        )(self))
        self.setFontPixel()

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        super(ElePyIcon, self).mousePressEvent(ev)
        if ev.buttons() == Qt.LeftButton:
            self.clicked.emit()

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
