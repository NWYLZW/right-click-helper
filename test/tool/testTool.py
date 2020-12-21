#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from typing import Callable

from PyQt5.QtWidgets import QApplication, QMainWindow

from src.rightClickHelper.tool.effectTool import EffectTool

class TestTool:
    @staticmethod
    def createTestWindow(setMainWindowContent: Callable, size: tuple = (200, 200)):
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setMinimumSize(*size)

        setMainWindowContent(app, window)

        window.show()
        sys._excepthook = sys.excepthook
        def myExceptionHook(exctype, value, traceback):
            print(exctype, value, traceback)
            sys._excepthook(exctype, value, traceback)
            sys.exit(1)
        sys.excepthook = myExceptionHook
        try: sys.exit(app.exec_())
        except: pass
    @staticmethod
    def createTestBlurWindow(setMainWindowContent: Callable, size: tuple = (200, 200)):
        def __setMainWindowContent(app, window):
            setMainWindowContent(app, window)
            EffectTool.setBlur(window)
        TestTool.createTestWindow(__setMainWindowContent, size)
