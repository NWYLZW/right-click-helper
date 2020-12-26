#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, datetime

from PyQt5.QtWidgets import QApplication

from src.rightClickHelper import config
from src.rightClickHelper.mainWindow import MainWindow

if __name__ == '__main__':
    try:
        if hasattr(sys, 'frozen'):
            os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()

        sys._excepthook = sys.excepthook

        def myExceptionHook(exctype, value, traceback):
            print(exctype, value, traceback)
            sys._excepthook(exctype, value, traceback)
            sys.exit(1)

        sys.excepthook = myExceptionHook

        try: sys.exit(app.exec_())
        except: pass
    except Exception as e:
        import traceback
        now = datetime.datetime.now()
        errorStr = now.strftime('[%Y-%m-%d %H:%M:%S]\n') + repr(e) + '\n' + traceback.format_exc() + '\n'

        if config.configData['appMode'] == '[development]':
            print(errorStr)
        else:
            if not os.path.exists('./log'): os.mkdir('./log')
            with open(
                f'./log/{now.year}-{now.month}-{now.day}.log'
                , mode='a+', encoding='utf-8'
            ) as file:
                file.write(errorStr)
