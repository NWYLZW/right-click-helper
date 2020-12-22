#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel

from src.rightClickHelper.component.popover.popover import Popover

class ToolTipMode(Enum):
    LIGHT   = 0X000000
    DARK    = 0X000001

class Tooltip(
    Popover
):
    def __init__(self, parent=None, properties: dict = {}):
        super(Tooltip).__init__(parent, properties)

    @staticmethod
    def setTooltip(
        widget: QWidget, text: str, position: str = 'bottom', mode: ToolTipMode = ToolTipMode.DARK
    ):
        tooltip = QLabel()
        tooltip.setAlignment(Qt.AlignCenter)
        tooltip.setText(text)

        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        tooltip.setFont(font)

        width = tooltip.fontMetrics()\
            .boundingRect(
                tooltip.text()
            ).width() + 10

        tooltip.setFixedWidth(width)
        tooltip.setMaximumHeight(45)

        setting = {}
        if mode == ToolTipMode.LIGHT:
            tooltip.setStyleSheet('''\
                margin: 5px;
                color: black;
            ''')
            setting['background-color'] = [255, 255, 255]
        elif mode == ToolTipMode.DARK:
            tooltip.setStyleSheet('''\
                margin: 5px;
                color: white;
            ''')
            setting['background-color'] = [48, 49, 51]

        Popover.setPopoverWithBackground(widget, tooltip, {
            'position': position
        }, setting=setting)
