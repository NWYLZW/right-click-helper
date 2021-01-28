#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__all__ = ['SystemTool']
import ctypes, win32ui, win32gui
import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWinExtras import QtWin

class SystemTool:
    @staticmethod
    def getFilePathByQFileDialog(
        parent=None, caption='', directory='',
        filter='', initialFilter=''
        , *args, **kwargs
    ) -> str:
        return QFileDialog.getOpenFileName(
            parent=parent, caption=caption, directory=directory,
            filter=filter, initialFilter=initialFilter
            , *args, **kwargs
        )[0]

    @staticmethod
    def getIcon(dataStr: str):
        try: (path, index) = dataStr.split(',')
        except: (path, index) = (dataStr, 0)

        path = path.replace('/', '\\')
        if os.path.exists(path):
            large, small = win32gui.ExtractIconEx(
                path, int(index) + (0 if path.find('.dll') == -1 else 1)
            )
            win32gui.DestroyIcon(small[0])
            pixMap = QtWin.fromHBITMAP(SystemTool.__bitmapFromHIcon(large[0]), 2)
            win32gui.DestroyIcon(large[0])
            return pixMap
        return QPixmap()

    @staticmethod
    def __bitmapFromHIcon(hIcon):
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), hIcon)
        hdc.DeleteDC()
        return hbmp.GetHandle()

    @staticmethod
    def isAdmin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
