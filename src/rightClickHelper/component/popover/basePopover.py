#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import typing

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDockWidget, QWidget

from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.tool.widgetTool import WidgetTool

class BasePopover(
    QDockWidget
):
    propertyChange = QtCore.pyqtSignal(str, object, dict, name='propertyChange')

    def __init__(self, parent=None, properties: dict = {}):
        super().__init__(parent)
        WidgetTool.setProperties(properties)(self)
        self._initUI()

    def _initUI(self):
        self.hide()
        temp = QWidget(); self.setTitleBarWidget(temp); del temp
        self.refreshUIByProperties()
        self.setFloating(True)

    def refreshUIByProperties(self):
        shadowRadius = WidgetTool.getProperty('shadowRadius', 10)(self)
        shadowColor = WidgetTool.getProperty('shadowColor', QtCore.Qt.gray)(self)
        EffectTool.setBlur(
            self, shadowRadius=shadowRadius, shadowColor=shadowColor
        )

    def setProperty(self, name: str, value: typing.Any) -> bool:
        returnData = {}
        self.propertyChange.emit(name, value, returnData)
        if returnData.get('value', True):
            return super().setProperty(name, value)
        return False
