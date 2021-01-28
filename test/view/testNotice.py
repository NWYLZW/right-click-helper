#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QMainWindow, QHBoxLayout

from src.rightClickHelper.component.form.elePyButton import ElePyButton
from src.rightClickHelper.component.notice.elePyMessage import ElePyMessage, ElePyMessageType
from src.rightClickHelper.component.notice.elePyMessageBox import ElePyMessageBox
from src.rightClickHelper.config.envs import data as envsData
from test.tool.testTool import TestTool

envsData['name'] = 'test'

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

    def test_messageBox(self):
        def setMainWindowContent(app: QApplication, window: QMainWindow):
            mainW = QWidget(None)
            window.setCentralWidget(mainW)
            mainW.setLayout(QHBoxLayout())

            def alert():
                ElePyMessageBox().alert(
                    '是否删除该文件?', '请确认'
                    , confirmBtnText='确定'
                )
            showMessage = ElePyButton(mainW)
            showMessage.setText('alert')
            showMessage.clicked.connect(alert)
            mainW.layout().addWidget(showMessage)

            def confirm():
                ElePyMessageBox().confirm(
                    '是否删除该文件?', '请确认'
                    , confirmBtnText='确定'
                    , cancelBtnText='取消'
                )
            showMessage = ElePyButton(mainW)
            showMessage.setText('confirm')
            showMessage.clicked.connect(confirm)
            mainW.layout().addWidget(showMessage)
        TestTool.createTestWindow(setMainWindowContent, (400, 400))
