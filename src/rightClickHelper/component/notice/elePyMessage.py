#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QApplication

from src.rightClickHelper.component.elePyWidget import watchProperty
from src.rightClickHelper.component.label.elePyIcon import ElePyIcon
from src.rightClickHelper.component.notice.elePyDockWidget import ElePyDockWidget
from src.rightClickHelper.tool.widgetTool import WidgetTool

class ElePyMessageType(Enum):
    SUCCESS = 0x000
    INFO    = 0x001
    WARN    = 0x002
    ERROR   = 0x003

class ElePyMessage(
    ElePyDockWidget
):
    def __init__(
        self, parent=None, properties: dict = None
    ):
        if properties is None: properties = {}
        super().__init__(parent, {
            'status': 'info',
            'deleteAble': True,
            **properties
        })

    def _initUi(self):
        super(ElePyMessage, self)._initUi()
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.setFixedSize(400, 60)
        self.mainWidget = QWidget(self)
        self.mainWidget.setFixedSize(self.size())
        self.layout().addWidget(self.mainWidget)

        self.mainWidget.setLayout(QHBoxLayout())
        self.mainWidget.layout()\
            .setContentsMargins(20, 0, 20, 0)

        self.icon = ElePyIcon(self.mainWidget)
        self.icon.setProperty('class', 'icon')
        self.icon.setText('')
        self.mainWidget.layout().addWidget(self.icon)

        self.message = QLabel(self.mainWidget)
        self.message.setProperty('class', 'label')
        self.message.setText('')
        self.mainWidget.layout().addWidget(self.message)

        delete = ElePyIcon(self.mainWidget)
        delete.setObjectName('delete')
        delete.setText('&#xe65e;')
        delete.setCursor(Qt.PointingHandCursor)
        self.mainWidget.layout().addWidget(delete)
        self.delete = delete
        self.delete.mousePressEvent = self.deleteBtnClick
        self.delete.setVisible(self.property('deleteAble'))

    def _initUiAfter(self):
        super(ElePyMessage, self)._initUiAfter()
        size = QApplication.primaryScreen().size()
        self.move(int((size.width() - self.width()) / 2), 0)

    def deleteBtnClick(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.createMoveAnimation({'val': 0}, False)()

    @watchProperty({
        'shadowRadius': {'type': int},
    })
    def shadowChange(self, newVal, oldVal, name):
        super(ElePyMessage, self).shadowChange(newVal, oldVal, name)
        shadowRadius = WidgetTool.getProperty('shadowRadius', 10)(self)

        self.setStyleSheet(f'''\
        .ElePyMessage >QWidget {{
            margin: {shadowRadius}px;
            border-radius: 6px;
        }}
        .ElePyMessage[status='success'] >QWidget {{
            background-color: rgb(240, 249, 235);
        }}
        .ElePyMessage[status='info'] >QWidget {{
            background-color: rgb(237, 242, 252);
        }}
        .ElePyMessage[status='warn'] >QWidget {{
            background-color: rgb(253, 246, 236);
        }}
        .ElePyMessage[status='error'] >QWidget {{
            background-color: rgb(254, 240, 240);
        }}
        .ElePyMessage[status='success'] >QWidget >QWidget {{
            color: rgb(103, 194, 58);
        }}
        .ElePyMessage[status='info'] >QWidget >QWidget {{
            color: rgb(144, 147, 153);
        }}
        .ElePyMessage[status='warn'] >QWidget >QWidget {{
            color: rgb(230, 163, 62);
        }}
        .ElePyMessage[status='error'] >QWidget >QWidget {{
            color: rgb(245, 108, 108);
        }}
        .ElePyMessage #delete {{
            color: rgb(144, 147, 153);
        }}
        .ElePyMessage #delete:hover {{
            color: rgb(50, 50, 50);
        }}''')

    @watchProperty({
        'deleteAble': {'type': bool}
    })
    def deleteAbleChange(self, newVal, oldVal, name):
        if hasattr(self, 'delete'):
            self.delete.setVisible(newVal)

    @watchProperty({
        'message': {'type': str},
        'type': {'type': ElePyMessageType}
    })
    def messageChange(self, newVal, oldVal, name):
        if name == 'message':
            self.message.setText(newVal)
        elif name == 'type':
            leftIcons = {
                ElePyMessageType.SUCCESS: '&#xe6f2;',
                ElePyMessageType.INFO:    '&#xe6a8;',
                ElePyMessageType.WARN:    '&#xe710;',
                ElePyMessageType.ERROR:   '&#xe687;',
            }
            self.icon.setText(leftIcons[newVal])
            self.setProperty('status', newVal.name.lower())

    def createMoveAnimation(self, height: dict, direction: bool = True):
        def move():
            height['val'] += 1 if direction else -1
            self.mainWidget.move(0, height['val'])
            self.setWindowOpacity((height['val'] + 100)/100)
            self.repaint()
            if direction:
                if height['val'] >= 0:
                    if not WidgetTool.getProperty('deleteAble', False):
                        QTimer.singleShot(3000, self.createMoveAnimation(height, False))
                    return
            else:
                if height['val'] <= -100:
                    self.hide()
                    return
            QTimer.singleShot(2, move)
        return move

    def show(self) -> None:
        super(ElePyMessage, self).show()
        self.activateWindow()
        self.setWindowOpacity(0)
        self.createMoveAnimation({'val': -100})()
