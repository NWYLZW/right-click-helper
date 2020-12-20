#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QHBoxLayout

from src.rightClickHelper.component.popover.popover import Popover
from src.rightClickHelper.tool.effectTool import EffectTool

class TestPopoverWidget(unittest.TestCase):
    def test_widget(self):
        import sys
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)

        window = QMainWindow()
        EffectTool.setBlur(window)
        window.setMinimumSize(400, 400)

        widget = QWidget()
        window.setCentralWidget(widget)

        widget.setObjectName('w001')
        widget.setMaximumSize(360, 360)
        widget.setStyleSheet('#w001 {background-color: red;}')

        label = QLabel()
        label.setText('test')
        label.setObjectName('label')
        label.setStyleSheet('''
        #label {
            margin: 10px; padding: 5px;
            border-radius: 4px;
            background-color: white;
        }
        ''')
        Popover.setPopover(widget, label, {
            'position': 'right'
        })

        window.show()
        sys._excepthook = sys.excepthook
        def myExceptionHook(exctype, value, traceback):
            print(exctype, value, traceback)
            sys._excepthook(exctype, value, traceback)
            sys.exit(1)
        sys.excepthook = myExceptionHook
        try: sys.exit(app.exec_())
        except: pass
