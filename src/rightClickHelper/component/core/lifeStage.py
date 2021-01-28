#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum

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
