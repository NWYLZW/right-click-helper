#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import typing

from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtWidgets import QDockWidget, QWidget

from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.tool.widgetTool import WidgetTool

class BasePopover(
    QDockWidget
):
    hided = pyqtSignal(); showed = pyqtSignal()
    propertyChange = pyqtSignal(str, object, dict)

    def __init__(self, parent=None, properties: dict = {}):
        self._inWidget = False
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
        shadowColor = WidgetTool.getProperty('shadowColor', Qt.gray)(self)
        EffectTool.setBlur(
            self, shadowRadius=shadowRadius, shadowColor=shadowColor
        )

    def enterEvent(self, event: QEvent) -> None:
        super(BasePopover, self).enterEvent(event)
        self._inWidget = True

    def leaveEvent(self, event: QEvent) -> None:
        super(BasePopover, self).enterEvent(event)
        self._inWidget = False

    def show(self) -> None:
        if WidgetTool.getProperty('forbiddenShow', False)(self): return

        super(BasePopover, self).show()
        self.showed.emit()

    def hide(self) -> None:
        super(BasePopover, self).hide()
        self.hided.emit()

    def setProperty(self, name: str, value: typing.Any) -> bool:
        returnData = {}
        self.propertyChange.emit(name, value, returnData)
        if returnData.get('value', True):
            return super().setProperty(name, value)
        return False

    @property
    def shadowRadius(self):
        return WidgetTool.getProperty('shadowRadius', 10)(self)

    @shadowRadius.setter
    def shadowRadius(self, val: str):
        self.setProperty('shadowRadius', val)
