#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from PyQt5.QtWidgets import QDialog, QWidget

from src.rightClickHelper.component.label.dragLabel import DragLabel
from src.rightClickHelper.tool.effectTool import EffectTool

class TestDragLabelAndDialog(unittest.TestCase):
    def test_noDialog(self):
        import sys
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)

        window = QDialog()
        EffectTool.setBlur(window, 20)
        window.setMinimumSize(250, 250)
        main = QWidget(window)
        main.setGeometry(
            25, 25, 200, 200
        )
        main.setObjectName('main')
        main.setStyleSheet(
            '''
            #main {
                border-radius: 10px;
                background-color: white;
            }
            '''
        )
        d1 = DragLabel(main)
        d1.path = r'F:\version-control\GIT\python\right-click-helper\src\resource\image\icon\warehouse.png'

        window.show()
        sys._excepthook = sys.excepthook
        def myExceptionHook(exctype, value, traceback):
            print(exctype, value, traceback)
            sys._excepthook(exctype, value, traceback)
            sys.exit(1)
        sys.excepthook = myExceptionHook
        try: sys.exit(app.exec_())
        except: pass
