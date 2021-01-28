#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel
from sqss import Compiler


class WidgetTool:
    @staticmethod
    def getProperty(name, defaultVal=''):
        def _fun(widget: QWidget):
            _property = widget.property(name)
            if _property is None:
                return defaultVal
            return _property
        return _fun

    @staticmethod
    def setProperties(properties: dict = {}):
        def _fun(widget: QWidget):
            for name, _property in properties.items():
                widget.setProperty(name, _property)
        return _fun

    @staticmethod
    def getTextWidth(label: QLabel) -> int:
        return label.fontMetrics() \
             .boundingRect(
            label.text()
        ).width()

    @staticmethod
    def setFont(
        label: QLabel
        , size: int = 10
        , family: str = 'Microsoft YaHei UI'
    ):
        font = QFont()
        font.setFamily(family)
        font.setPointSize(size)
        label.setFont(font)

    @staticmethod
    def setSqss(
        widget: QWidget
        , sqss: str
    ):
        widget.setStyleSheet(str(Compiler.deal_str(sqss)))
