#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QMainWindow

from src.rightClickHelper.component.notice.elePyMessage import ElePyMessage, ElePyMessageType
from test.tool.testTool import TestTool

class TestNotice(unittest.TestCase):
    def test_message(self):
        def setMainWindowContent(app: QApplication, window: QMainWindow):
            mainW = QWidget(None)
            window.setCentralWidget(mainW)

            temp = ElePyMessage.instance()
            count = {'val': 0}
            list0 = [{
                'type': ElePyMessageType.SUCCESS,
                'message': '测试成功',
                'showClose': True
            }, {
                'type': ElePyMessageType.INFO,
                'message': '测试消息',
                'showClose': True,
                'onClose': lambda: print(123)
            }, {
                'type': ElePyMessageType.WARN,
                'message': '测试警告',
                'offset':  100
            }, {
                'type': ElePyMessageType.ERROR,
                'message': '测试错误',
                'duration': 1000
            }]

            def btnA(c):
                temp.show()
                temp.setProperties(list0[count['val'] % 4])
                count['val'] += 1
            showMessage = QPushButton(mainW)
            showMessage.setText('show message')
            showMessage.clicked.connect(btnA)

        TestTool.createTestWindow(setMainWindowContent, (400, 400))
