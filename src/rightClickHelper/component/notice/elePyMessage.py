#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from typing import Callable

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QApplication

from src.rightClickHelper.component.core import LifeStage
from src.rightClickHelper.component.elePyWidget import watchProperty
from src.rightClickHelper.component.label.elePyIcon import ElePyIcon
from src.rightClickHelper.component.elePyDockWidget import ElePyDockWidget
from src.rightClickHelper.tool.widgetTool import WidgetTool

class ElePyMessageType(Enum):
    SUCCESS = 0x000
    INFO    = 0x001
    WARN    = 0x002
    ERROR   = 0x003

class ElePyMessage(
    ElePyDockWidget
):
    __instance__ = None

    @staticmethod
    def instance() -> 'ElePyMessage':
        if hasattr(ElePyMessage, '__instance__'):
            setattr(ElePyMessage, '__instance__', ElePyMessage())
        return ElePyMessage.__instance__

    def __init__(self, parent=None):
        self.defaultProperties = {
            'status': 'info',
            'offset': 0,
            'duration': 3000,
            'showClose': False
        }
        super().__init__(parent, self.defaultProperties)

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
        self.delete.setVisible(self.property('showClose'))

    def _initUiAfter(self):
        super(ElePyMessage, self)._initUiAfter()
        self.setProperty('offset', WidgetTool.getProperty(
            'offset', 0
        )(self))

    def deleteBtnClick(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            onClose = WidgetTool.getProperty(
                'onClose', lambda: True
            )(self)
            if isinstance(onClose, Callable):
                val = onClose()
                if val or val is None: self.createMoveAnimation({'val': 0}, False)()

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

    @watchProperty({'offset': {'type': int}})
    def offsetChange(self, newVal, *args):
        if self._lifeStage in [
            LifeStage.INIT_UI_AFTER,
            LifeStage.INITED
        ]:
            size = QApplication.primaryScreen().size()
            self.move(int((size.width() - self.width()) / 2), newVal)

    @watchProperty({'showClose': {'type': bool}})
    def showCloseChange(self, newVal, *args):
        if hasattr(self, 'delete'):
            self.delete.setVisible(newVal)

    @watchProperty({
        'message': {'type': str},
        'type': {'type': ElePyMessageType}
    })
    def messageChange(self, newVal, oldVal, name):
        if name == 'message':
            if not hasattr(self, 'message'): return
            self.message.setText(newVal)
        elif name == 'type':
            if not hasattr(self, 'icon'): return
            leftIcons = {
                ElePyMessageType.SUCCESS: '&#xe6f2;',
                ElePyMessageType.INFO:    '&#xe6a8;',
                ElePyMessageType.WARN:    '&#xe710;',
                ElePyMessageType.ERROR:   '&#xe687;',
            }
            self.icon.setText(WidgetTool.getProperty(
                'iconUnicode', leftIcons[newVal]
            )(self))
            self.setProperty('status', newVal.name.lower())

    def createMoveAnimation(self, height: dict, direction: bool = True):
        def move():
            height['val'] += 1 if direction else -1
            self.mainWidget.move(0, height['val'])
            self.setWindowOpacity((height['val'] + 100)/100)
            self.repaint()
            if direction:
                if height['val'] >= 0:
                    if not WidgetTool.getProperty('showClose', False)(self):
                        QTimer.singleShot(WidgetTool.getProperty(
                            'duration', 3000
                        )(self), self.createMoveAnimation(height, False))
                    return
            else:
                if height['val'] <= -100:
                    self.hide()
                    return
            QTimer.singleShot(2, move)
        return move

    def hide(self) -> None:
        super(ElePyMessage, self).hide()
        self.setProperty('offset', 0)
        self.setProperty('message', '')
        self.setProperty('type', ElePyMessageType.INFO)
        self.setProperty('showClose', False)
        self.setProperty('onClose', lambda: True)
        self.setProperties(self.defaultProperties)

    def show(self, message: dict = None) -> None:
        if message is None: message = {}
        self.setProperties(message)
        super(ElePyMessage, self).show()

        self.activateWindow()
        self.setWindowOpacity(0)
        self.createMoveAnimation({'val': -100})()
