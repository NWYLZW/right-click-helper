#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import abstractmethod

from PyQt5.QtWidgets import QWidget

from src.rightClickHelper.tool.widgetTool import WidgetTool

class ElePyWidget(
    QWidget
):
    def __init__(self, parent=None, properties: dict = {}):
        super().__init__(parent)
        WidgetTool.setProperties(properties)(self)

        self._initUIBefore()
        self._initUI()
        self._initUIAfter()

        self._initDataBefore()
        self._initData()
        self._initDataAfter()

        self._initEventBefore()
        self._initEvent()
        self._initEventAfter()

    def _initUIBefore(self): pass
    def _initUIAfter(self): pass
    def _initDataBefore(self): pass
    def _initDataAfter(self): pass
    def _initEventBefore(self): pass
    def _initEventAfter(self): pass

    @abstractmethod
    def _initUI(self): pass

    @abstractmethod
    def _initData(self): pass

    @abstractmethod
    def _initEvent(self): pass
