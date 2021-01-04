#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, QEvent

from src.rightClickHelper.component.elePyDockWidget import ElePyDockWidget
from src.rightClickHelper.tool.widgetTool import WidgetTool

class BasePopover(
    ElePyDockWidget
):
    hided = pyqtSignal(); showed = pyqtSignal()

    def __init__(
        self, parent=None, properties: dict = None
    ):
        if properties is None: properties = {}
        self._inWidget = False
        super().__init__(parent, properties)

    def _initUi(self):
        super(BasePopover, self)._initUi()
        self.hide()

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

    @property
    def shadowRadius(self):
        return WidgetTool.getProperty('shadowRadius', 10)(self)

    @shadowRadius.setter
    def shadowRadius(self, val: str):
        self.setProperty('shadowRadius', val)
