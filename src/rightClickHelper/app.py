#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from src.rightClickHelper.mainWindow import MainWindow

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    APP = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    sys._excepthook = sys.excepthook

    def my_exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = my_exception_hook

    try: sys.exit(APP.exec_())
    except Exception as e: print("Exiting")
