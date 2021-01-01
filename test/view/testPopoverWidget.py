#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from typing import ClassVar

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton

from src.rightClickHelper.component.form.elePySelect import ElePySelect
from src.rightClickHelper.component.popover.elePyMenuPopover import ElePyMenuPopover, PopoverMenuItem, MenuPopoverMode
from src.rightClickHelper.component.popover.elePyPopover import ElePyPopover
from src.rightClickHelper.component.popover.elePyTooltip import ElePyTooltip
from src.rightClickHelper.tool.pathTool import PathTool
from test.tool.testTool import TestTool

class TestPopoverWidget(unittest.TestCase):
    def test_Popover(self):
        def setMainWindowContent(app, window):
            widget = QWidget()
            window.setCentralWidget(widget)

            widget.setObjectName('w001')
            widget.setMaximumSize(360, 360)
            widget.setStyleSheet('#w001 {background-color: red;}')

            label = QLabel()
            label.setMaximumSize(100, 40)
            label.setText('test')
            label.setObjectName('label')
            label.setStyleSheet('''
            #label {
                margin: 10px; padding: 5px;
                border-radius: 4px;
                background-color: white;
            }
            ''')
            ElePyPopover.setPopover(widget, label, {
                'position': 'right'
            })

        TestTool.createTestBlurWindow(setMainWindowContent, (400, 400))

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
                color: white;
            ''')
            ElePyPopover.setPopoverWithBackground(widget, label, {
                'position': 'right'
            }, setting={
                'background-color': [48, 49, 51]
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

    def test_TooltipPopover(self):
        def setMainWindowContent(app, window):
            widget = QWidget()
            window.setCentralWidget(widget)

            widget.setObjectName('w001')
            widget.setMaximumSize(360, 360)
            widget.setStyleSheet(f'''\
            #{widget.objectName()} {{
                margin: 10px;
                background-color: rgba(200, 200, 200);
            }}
            ''')

            ElePyTooltip.setTooltip(
                widget, '2345678911111测试中文111111testEnglish11111111198765432'
            )

        TestTool.createTestBlurWindow(setMainWindowContent, (400, 400))

    def test_MenuPopover(self):
        def setMainWindowContent(app, window):
            label = QLabel()
            label.setText('请选择')
            window.setCentralWidget(label)

            label.setObjectName('w001')
            label.setMaximumSize(120, 25)
            label.setStyleSheet('''\
            #w001 {
                border: 1px solid;
                border-radius: 4px;
                background-color: rgb(250, 250, 250);
            }''')

            def createPopover(PopoverClass: ClassVar, widget, properties):
                popover = PopoverClass(widget, properties)

                def __itemClick(popoverMenuItem):
                    popoverMenuItem.setProperty('status', 'forbidden')
                popover.itemClicked.connect(__itemClick)
                return popover

            ElePyMenuPopover.setMenu(
                label, [{
                    'label': '测试选项148941516',
                    'icon':  PathTool.appPath(isTest=True) + r'\src\resource\image\common-icon\paste.png'
                }, {
                    'label': '测试选项2',
                    'status': 'forbidden'
                }, {
                    'label':  '测试选项3',
                    'icon':  PathTool.appPath(isTest=True) + r'\src\resource\image\common-icon\paste-ed.png'
                }], mode=MenuPopoverMode.DARK
                , createPopover=createPopover
            )

        TestTool.createTestWindow(setMainWindowContent, (400, 400))

    def test_Select(self):
        def setMainWindowContent(app, window):
            mainW = QWidget()

            select = ElePySelect(mainW, properties={
                'select-menu-items': [{
                    'label': '测试下拉选择1',
                    'icon':  PathTool.appPath(isTest=True) + r'\src\resource\image\common-icon\paste.png'
                }, {
                    'label': '测试下拉选择2',
                    'status': 'forbidden'
                }, {
                    'label':  '测试下拉选择3',
                    'icon':  PathTool.appPath(isTest=True) + r'\src\resource\image\common-icon\paste-ed.png'
                }]
            })
            select.change.connect(
                lambda m, indexList, selItems: print(m.title, indexList, selItems)
            )

            window.setCentralWidget(mainW)

        TestTool.createTestBlurWindow(setMainWindowContent, (400, 400))
