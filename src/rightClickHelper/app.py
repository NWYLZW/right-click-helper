#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, datetime

from PyQt5.QtWidgets import QApplication

from src.rightClickHelper.mainWindow import MainWindow

if __name__ == '__main__':
    try:
        if hasattr(sys, 'frozen'):
            os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

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
        except: pass
    except Exception as e:
        import traceback
        if not os.path.exists('./log'): os.mkdir('./log')

        now = datetime.datetime.now()
        with open(
            f'./log/{now.year}-{now.month}-{now.day}.log'
            , mode='a+', encoding='utf-8'
        ) as file:
            file.write(
                now.strftime('[%Y-%m-%d %H:%M:%S]\n') + repr(e) + '\n' + traceback.format_exc() + '\n'
            )
