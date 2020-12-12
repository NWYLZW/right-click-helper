#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, winreg
from enum import Enum

class CommandFlag(Enum):
    NONE = 0X00000000
    HIDE = 0X00000008

class RegEnv(Enum):
    HKEY_CLASSES_ROOT = winreg.HKEY_CLASSES_ROOT

class RegTool:
    def __init__(self):
        pass

    @staticmethod
    def listKey(env: RegEnv, path: str) -> list:
        regKey = winreg.OpenKey(env.value, path)
        regCount = winreg.QueryInfoKey(regKey)[0]
        regKeys = []
        for i in range(int(regCount)):
            name = winreg.EnumKey(regKey, i)
            regKeys.append(name)
        winreg.CloseKey(regKey)
        return regKeys

    @staticmethod
    def listVal(env: RegEnv, path: str) -> dict:
        regKey = winreg.OpenKey(env.value, path)
        i = 0
        regVals = {}
        try:
            while True:
                name, val, type = winreg.EnumValue(regKey, i)
                regVals[name] = val
                i += 1
        finally:
            winreg.CloseKey(regKey)
            return regVals

    @staticmethod
    def recursion(env: RegEnv, startPath: str, depth: int = 1000) -> {}:
        if depth == 0: return {}

        originData = {}
        originList = RegTool.listKey(env, startPath)

        for item in originList:
            originData[item] = RegTool.recursion(env, startPath + '\\' + item, depth - 1)

        originData['__path__'] = (env, startPath)
        originData['__val__'] = RegTool.listVal(env, startPath)
        return originData

class MenuItem:
    def __init__(self, name: str, regData: dict):
        self.regData = regData
        self.name    = name

        regDataVal = regData.get('__val__', {})
        commandVal = regData.get('command', {
            '__val__': {}
        }).get('__val__', {})

        self.title      = regDataVal.get('', '')
        # type: str
        self.icon       = regDataVal.get('Icon', '')
        # type: str
        self.command    = commandVal.get('', '')
        # type: str

        self.isPackage  = regDataVal.get('SubCommands', False) == ''
        # type: bool
        # 二级菜单
        self.isHide     = not (regDataVal.get('CommandFlags', CommandFlag.NONE.value) == CommandFlag.HIDE.value)
        # type: bool
        # 隐藏
        self.isShift    = regDataVal.get('Extended', False) == ''
        # type: bool
        # 按下shift时
        self.isExplorer = regDataVal.get('OnlyInBrowserWindow', False) == ''
        # type: bool
        # 文件浏览器中
        self.isNotWorkingDir = regDataVal.get('NoWorkingDirectory', False) == ''
        # type: bool
        # 不以当前目录为打开的工作目录

    @property
    def children(self) -> []:
        if not self.isPackage:
            return []

        returnChildren = []
        env, path = self.regData.get('__path__')
        regDataTree = RegTool.recursion(env, path + '\\shell', 3)
        for key, val in regDataTree.items():
            if key[:2] != '__':
                returnChildren.append(
                    MenuItem(key, regDataTree[key])
                )
        return returnChildren

    def __str__(self):
        return json.dumps(self.regData, sort_keys=False, indent=2, separators=(',', ':'))
