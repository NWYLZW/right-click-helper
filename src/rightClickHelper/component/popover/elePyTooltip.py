#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel

from src.rightClickHelper.component.popover.elePyPopover import ElePyPopover
from src.rightClickHelper.tool.widgetTool import WidgetTool

class ToolTipMode(Enum):
    LIGHT   = 0X000000
    DARK    = 0X000001

class ElePyTooltip(
    ElePyPopover
):
    def __init__(self, parent=None, properties: dict = {}):
        super().__init__(parent, properties)

    @staticmethod
    def setTooltip(
        widget: QWidget, text: str, position: str = 'bottom', mode: ToolTipMode = ToolTipMode.DARK
    ):
        tooltip = QLabel()
        tooltip.setAlignment(Qt.AlignCenter)
        tooltip.setText(text)
        tooltip.setTextInteractionFlags(Qt.TextBrowserInteraction)
        tooltip.setCursor(Qt.IBeamCursor)
        WidgetTool.setFont(tooltip)

        width = tooltip.fontMetrics()\
            .boundingRect(
                tooltip.text()
            ).width() + 10

        tooltip.setFixedWidth(width)
        tooltip.setMaximumHeight(30)

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

        ElePyPopover.setPopoverWithBackground(widget, tooltip, {
            'position': position,
            'animation-type': 'fadeInOut'
        }, setting=setting, PopoverClass=ElePyTooltip)
