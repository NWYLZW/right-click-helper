#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton

from src.rightClickHelper.component.popover.popover import Popover
from test.tool.testTool import TestTool

class TestPopoverWidget(unittest.TestCase):
    def test_WithBackgroundPopover(self):
        def setMainWindowContent(app, window):
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

        TestTool.createTestBlurWindow(setMainWindowContent, (400, 400))
