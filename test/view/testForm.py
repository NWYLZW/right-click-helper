#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

from src.rightClickHelper.component.form.elePyButton import ElePyButton
from src.rightClickHelper.config.env import data as envsData
from test.tool.testTool import TestTool

envsData['name'] = 'test'

class TestNotice(unittest.TestCase):
    def test_buttons(self):
        def setMainWindowContent(app: QApplication, window: QMainWindow):
            mainW = QWidget(None)
            window.setCentralWidget(mainW)
            mainW.setLayout(QVBoxLayout())

            def createBtns(attachProperties: dict = {}, btnsData: list = None):
                btns = QWidget()
                mainW.layout().addWidget(btns)
                btns.setLayout(QHBoxLayout())
                if btnsData is None:
                    btnsData = [{
                        'text': '默认按钮'
                    }, {
                        'text': '主要按钮',
                        'type': ElePyButton.Type.PRIMARY
                    }, {
                        'text': '成功按钮',
                        'type': ElePyButton.Type.SUCCESS
                    }, {
                        'text': '信息按钮',
                        'type': ElePyButton.Type.INFO
                    }, {
                        'text': '警告按钮',
                        'type': ElePyButton.Type.WARNING
                    }, {
                        'text': '危险按钮',
                        'type': ElePyButton.Type.DANGER
                    }]
                for btnData in btnsData:
                    btns.layout().addWidget(
                        ElePyButton(mainW, {
                            **btnData,
                            **attachProperties
                        })
                    )
            createBtns()
            createBtns({
                "plain": True
            })
            createBtns({
                "round": True
            })
            createBtns({
                "round": True
            }, [{
                'icon': '&#xe6da;'
            }, {
                'icon': '&#xe6db;',
                'type': ElePyButton.Type.PRIMARY
            }, {
                'icon': '&#xe6dc;',
                'type': ElePyButton.Type.SUCCESS
            }, {
                'icon': '&#xe6dd;',
                'type': ElePyButton.Type.INFO
            }, {
                'icon': '&#xe6de;',
                'type': ElePyButton.Type.WARNING
            }, {
                'icon': '&#xe6df;',
                'type': ElePyButton.Type.DANGER
            }])
            createBtns({
                "round": True
            }, [{
                'text': '仓库',
                'icon': '&#xe6da;'
            }, {
                'text': '电话',
                'icon': '&#xe6db;',
                'type': ElePyButton.Type.PRIMARY
            }, {
                'text': '图片',
                'icon': '&#xe6dc;',
                'type': ElePyButton.Type.SUCCESS
            }, {
                'text': '刷新',
                'icon': '&#xe6dd;',
                'type': ElePyButton.Type.INFO
            }, {
                'text': '图片',
                'icon': '&#xe6de;',
                'type': ElePyButton.Type.WARNING
            }, {
                'text': '计时',
                'icon': '&#xe6df;',
                'type': ElePyButton.Type.DANGER
            }])
        TestTool.createTestWindow(setMainWindowContent, (400, 400))

    def test_disabledButton(self):
        def setMainWindowContent(app: QApplication, window: QMainWindow):
            mainW = QWidget(None)
            window.setCentralWidget(mainW)
            mainW.setLayout(QVBoxLayout())

            def createBtns(attachProperties: dict = {}, btnsData: list = None):
                btns = QWidget()
                mainW.layout().addWidget(btns)
                btns.setLayout(QHBoxLayout())
                if btnsData is None:
                    btnsData = [{
                        'text': '默认按钮'
                    }, {
                        'text': '主要按钮',
                        'type': ElePyButton.Type.PRIMARY
                    }, {
                        'text': '成功按钮',
                        'type': ElePyButton.Type.SUCCESS
                    }, {
                        'text': '信息按钮',
                        'type': ElePyButton.Type.INFO
                    }, {
                        'text': '警告按钮',
                        'type': ElePyButton.Type.WARNING
                    }, {
                        'text': '危险按钮',
                        'type': ElePyButton.Type.DANGER
                    }]
                for btnData in btnsData:
                    btns.layout().addWidget(
                        ElePyButton(mainW, {
                            **btnData,
                            **attachProperties
                        })
                    )
            createBtns({
                "disabled": True
            })
            createBtns({
                "disabled": True,
                "plain": True
            })
        TestTool.createTestWindow(setMainWindowContent, (400, 400))

    def test_btnsWithDisabled(self):
        def setMainWindowContent(app: QApplication, window: QMainWindow):
            mainW = QWidget(None)
            window.setCentralWidget(mainW)
            mainW.setLayout(QVBoxLayout())

            def createBtns(attachProperties: dict = {}, btnsData: list = None):
                btns = QWidget()
                mainW.layout().addWidget(btns)
                btns.setLayout(QHBoxLayout())
                if btnsData is None:
                    btnsData = [{
                        'text': '默认按钮'
                    }, {
                        'text': '主要按钮',
                        'type': ElePyButton.Type.PRIMARY
                    }, {
                        'text': '成功按钮',
                        'type': ElePyButton.Type.SUCCESS
                    }, {
                        'text': '信息按钮',
                        'type': ElePyButton.Type.INFO
                    }, {
                        'text': '警告按钮',
                        'type': ElePyButton.Type.WARNING
                    }, {
                        'text': '危险按钮',
                        'type': ElePyButton.Type.DANGER
                    }]
                for btnData in btnsData:
                    btns.layout().addWidget(
                        ElePyButton(mainW, {
                            **btnData,
                            **attachProperties
                        })
                    )
            createBtns()
            createBtns({
                "plain": True
            })
            createBtns({
                "round": True
            })
            createBtns({
                "round": True
            }, [{
                'icon': '&#xe6da;'
            }, {
                'icon': '&#xe6db;',
                'type': ElePyButton.Type.PRIMARY
            }, {
                'icon': '&#xe6dc;',
                'type': ElePyButton.Type.SUCCESS
            }, {
                'icon': '&#xe6dd;',
                'type': ElePyButton.Type.INFO
            }, {
                'icon': '&#xe6de;',
                'type': ElePyButton.Type.WARNING
            }, {
                'icon': '&#xe6df;',
                'type': ElePyButton.Type.DANGER
            }])
            createBtns({
                "disabled": True
            })
            createBtns({
                "disabled": True,
                "plain": True
            })

        TestTool.createTestWindow(setMainWindowContent, (400, 400))

    def test_btnsSize(self):
        def setMainWindowContent(app: QApplication, window: QMainWindow):
            mainW = QWidget(None)
            window.setCentralWidget(mainW)
            mainW.setLayout(QVBoxLayout())

            iconBtns = [{
                'icon': '&#xe6da;'
            }, {
                'icon': '&#xe6db;',
                'type': ElePyButton.Type.PRIMARY
            }, {
                'icon': '&#xe6dc;',
                'type': ElePyButton.Type.SUCCESS
            }, {
                'icon': '&#xe6dd;',
                'type': ElePyButton.Type.INFO
            }, {
                'icon': '&#xe6de;',
                'type': ElePyButton.Type.WARNING
            }, {
                'icon': '&#xe6df;',
                'type': ElePyButton.Type.DANGER
            }]
            def createBtns(attachProperties: dict = {}, btnsData: list = None):
                btns = QWidget()
                mainW.layout().addWidget(btns)
                btns.setLayout(QHBoxLayout())
                if btnsData is None:
                    btnsData = [{
                        'text': '默认按钮'
                    }, {
                        'text': '主要按钮',
                        'type': ElePyButton.Type.PRIMARY
                    }, {
                        'text': '成功按钮',
                        'type': ElePyButton.Type.SUCCESS
                    }, {
                        'text': '信息按钮',
                        'type': ElePyButton.Type.INFO
                    }, {
                        'text': '警告按钮',
                        'type': ElePyButton.Type.WARNING
                    }, {
                        'text': '危险按钮',
                        'type': ElePyButton.Type.DANGER
                    }]
                for btnData in btnsData:
                    btns.layout().addWidget(
                        ElePyButton(mainW, {
                            **btnData,
                            **attachProperties
                        })
                    )
            sizes = [
                {'el-size': ElePyButton.Size.COMMON.value},
                {'el-size': ElePyButton.Size.MEDIUM.value},
                {'el-size': ElePyButton.Size.SMALL.value},
                {'el-size': ElePyButton.Size.MINI.value},
            ]
            for size in sizes:
                createBtns({
                    **size
                })
            for size in sizes:
                createBtns({
                    'round': True,
                    **size
                }, iconBtns)

        TestTool.createTestWindow(setMainWindowContent, (400, 600))
