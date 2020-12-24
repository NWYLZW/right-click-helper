#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import typing
from abc import abstractmethod
from functools import wraps

from PyQt5.QtWidgets import QWidget

from src.rightClickHelper.tool.widgetTool import WidgetTool

class ElePyWidget(
    QWidget
):
    def __init__(self, parent=None, properties: dict = {}):
        super().__init__(parent)
        self.__setPropertyWatch()
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

    def __setPropertyWatch(self):
        self.__watchProperties__ = {}
        for key in dir(self):
            attr = getattr(self, key)
            if hasattr(attr, '__watchProperties__'):
                for watchPropertyName, _watchProperty in getattr(attr, '__watchProperties__').items():
                    _watchProperty['handler'] = attr
                    self.__watchProperties__[watchPropertyName] = _watchProperty

    def setProperties(self, properties: dict = {}):
        WidgetTool.setProperties(properties)(self)

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

    def propertyChange(
        self, name: str, value: typing.Any
    ) -> bool:
        if name in self.__watchProperties__:
            _watchProperty = self.__watchProperties__[name]

            propertyType = _watchProperty['type']
            propertyHandler = _watchProperty['handler']

            if propertyType is not None and not isinstance(value, propertyType):
                raise TypeError('Property\'s type is different than expected.')
            returnVal = propertyHandler(value, self.property(name), name)
            if returnVal is None: return True
            return returnVal
        return True

    def setProperty(
        self, name: str, value: typing.Any
    ) -> bool:
        if self.propertyChange(name, value):
            return super().setProperty(name, value)
        return False

def watchProperty(
    properties: dict[str, object] or list[str]
):
    """
    检测Widget
    :param properties: 检测的property信息列表
    :return: 一个函数装饰器
    """
    def __wrapper(func):
        @wraps(func)
        def __fun(*args, **kwargs):
            return func(*args, **kwargs)

        __fun.__watchProperties__ = \
            (lambda: func.__watchProperties__ if hasattr(func, '__watchProperties__') else {})()
        if isinstance(properties, dict):
            for _propertyName, _property in properties.items():
                __fun.__watchProperties__[_propertyName] = \
                    _property if isinstance(_property, dict) else {
                        'type': None
                    }

                if _propertyName == '':
                    raise ValueError('Watched property\'s name can\'t set null.')
        else:
            for _propertyName in properties:
                __fun.__watchProperties__[_propertyName] = {
                    'type': None
                }

                if _propertyName == '':
                    raise ValueError('Watched property\'s name can\'t set null.')
        return __fun
    return __wrapper
