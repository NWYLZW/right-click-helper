#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__all__ = ['ElePyWidget', 'watchProperty', 'LifeStage']
import typing
from enum import Enum
from functools import wraps

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from src.rightClickHelper.tool.widgetTool import WidgetTool

class LifeStage(Enum):
    SET_PROPERTY_WATCH = 0X00000001
    INIT_PROPERTIES = 0X00000002

    INIT_UI_BEFORE = 0X00000003
    INIT_UI = 0X00000004
    INIT_UI_AFTER = 0X00000005

    INIT_DATA_BEFORE = 0X00000006
    INIT_DATA = 0X00000007
    INIT_DATA_AFTER = 0X00000008

    INIT_EVENT_BEFORE = 0X00000009
    INIT_EVENT = 0X0000000a
    INIT_EVENT_AFTER = 0X0000000b

    INITED = 0Xffffffff

def initLink(obj, lifeStages: list[LifeStage]):
    def str2Hump(text):
        res = ''.join(
            [_str[0].upper() + _str[1:] for _str in text.lower().split('_')]
        )
        return res[0].lower() + res[1:]

    for lifeStage in lifeStages:
        methodName = f'_{str2Hump(lifeStage.name)}'
        obj._lifeStage = lifeStage
        if hasattr(obj, methodName):
            getattr(obj, methodName)()

class ElePyWidget(
    QWidget
):
    def __init__(self, parent=None, properties: dict = {}):
        super().__init__(parent)
        # 设置style对当前widget起作用
        self.setAttribute(Qt.WA_StyledBackground)

        self._lifeStage = LifeStage.SET_PROPERTY_WATCH
        self.__setPropertyWatch()
        self._lifeStage = LifeStage.INIT_PROPERTIES
        WidgetTool.setProperties(properties)(self)

        initLink(self, [
            LifeStage.INIT_UI_BEFORE,
            LifeStage.INIT_UI,
            LifeStage.INIT_UI_AFTER,
        ])
        initLink(self, [
            LifeStage.INIT_DATA_BEFORE,
            LifeStage.INIT_DATA,
            LifeStage.INIT_DATA_AFTER,
        ])
        initLink(self, [
            LifeStage.INIT_EVENT_BEFORE,
            LifeStage.INIT_EVENT,
            LifeStage.INIT_EVENT_AFTER,
        ])
        self._lifeStage = LifeStage.INITED

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

    def _initUiBefore(self): pass
    def _initUi(self): pass
    def _initUiAfter(self): pass

    def _initDataBefore(self): pass
    def _initData(self): pass
    def _initDataAfter(self): pass

    def _initEventBefore(self): pass
    def _initEvent(self): pass
    def _initEventAfter(self): pass

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
