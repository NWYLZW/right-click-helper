#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QHBoxLayout, QPushButton

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
        label.setGeometry(0, 0, 100, 40)
        label.setStyleSheet('''\
            margin: 5px;
        ''')
        Popover.setPopoverWithBackground(widget, label, {
            'position': 'right'
        })

        positions = [
            'right', 'top', 'bottom', 'left', 0
        ]
        push1 = QPushButton(widget)
        push1.setText('changePosition')
        def changePosition(c):
            positions[4] += 1
            widget.popover.setProperty('position', positions[positions[4] % 4])
        push1.clicked.connect(changePosition)

        window.show()
        sys._excepthook = sys.excepthook
        def myExceptionHook(exctype, value, traceback):
            print(exctype, value, traceback)
            sys._excepthook(exctype, value, traceback)
            sys.exit(1)
        sys.excepthook = myExceptionHook
        try: sys.exit(app.exec_())
        except: pass
