#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__all__ = ['ElePyWidget', 'watchProperty']

import os
import typing
from sqss import Compiler
from functools import wraps

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from src.rightClickHelper.component.core import AbsWidget, LifeStage
from src.rightClickHelper.tool.pathTool import PathTool
from src.rightClickHelper.tool.widgetTool import WidgetTool

class ElePyWidget(
    QWidget, AbsWidget
):
    def __init__(self, parent=None, properties: dict = None):
        QWidget.__init__(self, parent)
        # 设置style对当前widget起作用
        self.setAttribute(Qt.WA_StyledBackground)

        self._lifeStage = LifeStage.SET_PROPERTY_WATCH
        self.__setPropertyWatch()
        self._lifeStage = LifeStage.INIT_PROPERTIES
        if properties is None: properties = {}
        WidgetTool.setProperties(properties)(self)

        ElePyWidget.initLinks(self)

    def __setPropertyWatch(self):
        self.__watchProperties__ = {}
        for key in dir(self):
            attr = getattr(self, key)
            if hasattr(attr, '__watchProperties__'):
                for watchPropertyName, _watchProperty in getattr(attr, '__watchProperties__').items():
                    self.__watchProperties__[watchPropertyName] = {
                        'handler': attr,
                        **_watchProperty
                    }

    def setProperties(self, properties: dict = {}):
        WidgetTool.setProperties(properties)(self)

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
        returnBool = False
        if self.propertyChange(name, value):
            returnBool = super().setProperty(name, value)
        self.setStyleSheet(self.styleSheet())
        self.repaint(); self.update()
        return returnBool

    def setSQSS(self, sqss: str) -> None:
        self.setStyleSheet(str(Compiler.deal_str(sqss)))

    @classmethod
    def getResource(cls, path):
        with open(cls.getResourcePath(path), 'r') as f:
            return f.read()

    @staticmethod
    def getResourcePath(path):
        return os.path.join(
            PathTool.appPath(), r'src\resource', path
        )

def watchProperty(
    properties: dict[str, object] or list[str]
):
    """
    检测Widget
    :param properties: 检测的property信息列表
    :return: 一个函数装饰器
    """
    def __wrapper(func: typing.Callable[
        [typing.Any, typing.Any, str], bool
    ]):
        """
        :param func: 观测值变化的函数
        :return: 返回一个被装饰后的观测函数
        """
        @wraps(func)
        def __fun(*args, **kwargs):
            return func(*args, **kwargs)

        __fun.__watchProperties__ = func.__watchProperties__ if hasattr(func, '__watchProperties__') else {}
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
