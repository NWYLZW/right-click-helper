#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from PyQt5.QtWidgets import QPushButton

from src.rightClickHelper.component.elePyWidget import ElePyWidget, watchProperty
from test.tool.testTool import TestTool

class TestWidget(unittest.TestCase):
    def test_watchProperty(self):

        class __TestWidget(ElePyWidget):
            def __init__(self, parent=None, properties: dict = {}):
                super().__init__(parent, properties)

            @watchProperty(['xxxx'])
            def xxxxWatch(self, newVal, oldVal, propertyName) -> bool:
                print('这是不会被检测到的xxxx修改')
                return True

            @watchProperty({
                'test': {'type': int}
            })
            def testWatch(self, newVal, oldVal, propertyName) -> bool:
                print(self._lifeStage)
                print(newVal, oldVal, propertyName)

        def setMainWindowContent(app, window):
            count = {'val': 0}
            mainW = __TestWidget(None)

            changeTestProperty = QPushButton(mainW)
            changeTestProperty.setText('change test property')

            def btnC(c):
                count['val'] += 1
                mainW.setProperty('test', count['val'])
            changeTestProperty.clicked\
                .connect(btnC)

            window.setCentralWidget(mainW)

        TestTool.createTestWindow(setMainWindowContent, (400, 400))
