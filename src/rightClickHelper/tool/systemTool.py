#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ctypes, win32ui, win32gui

from PyQt5.QtWinExtras import QtWin

class SystemTool:
    @staticmethod
    def getIcon(dataStr: str):
        try: (path, index) = dataStr.split(',')
        except: (path, index) = (dataStr, 0)

        large, small = win32gui.ExtractIconEx(path, int(index) + (0 if path.find('.dll') == -1 else 1))
        win32gui.DestroyIcon(small[0])
        pixMap = QtWin.fromHBITMAP(SystemTool.__bitmapFromHIcon(large[0]), 2)
        win32gui.DestroyIcon(large[0])
        return pixMap

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
