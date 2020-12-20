#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget

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
