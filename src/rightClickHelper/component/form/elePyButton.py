#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from typing import Union

from PyQt5.QtCore import Qt, QEvent, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from src.rightClickHelper.component.core import LifeStage
from src.rightClickHelper.component.elePyWidget import ElePyWidget, watchProperty
from src.rightClickHelper.component.label.elePyIcon import ElePyIcon
from src.rightClickHelper.component.label.elePyLabel import ElePyLabel
from src.rightClickHelper.tool.widgetTool import WidgetTool

class ElePyButton(
    ElePyWidget
):
    class Size(Enum):
        COMMON = '40'
        MEDIUM = '36'
        SMALL  = '32'
        MINI   = '28'

    class Type(Enum):
        NONE    = 0x000
        PRIMARY = 0x001
        SUCCESS = 0x002
        WARNING = 0x003
        DANGER  = 0x004
        INFO    = 0x005
        TEXT    = 0x006

    class IconPos(Enum):
        CENTER = 0x000
        LEFT   = 0x001
        RIGHT  = 0x002

    clicked = pyqtSignal()

    def __init__(self, parent=None, properties: dict = None):
        if properties is None: properties = {}
        self.__initData__ = {}
        super().__init__(parent, {
            'text':     '',
            'disabled': False,
            'el-size':  ElePyButton.Size.COMMON.value,
            **properties
        })

    def _initUi(self):
        super(ElePyButton, self)._initUi()
        self.setSQSS(
            self.__class__.getResource('sqss/component/ele_py_button.sqss')
        )
        self.setLayout(QHBoxLayout())
        self.layout().setSpacing(0)

        icon = ElePyIcon(self)
        icon.hide()
        self.layout().addWidget(icon)
        self.__icon = icon

        label = ElePyLabel(self)
        WidgetTool.setFont(label)
        label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(label)
        self.__label = label

    def _initData(self):
        super(ElePyButton, self)._initData()
        if self.__initData__.get('text', None) is not None:
            self.setText(self.__initData__['text'])
        if self.__initData__.get('icon-data', None):
            self.__initData__['icon-data']()

    def refreshSize(self, elSize=None):
        text = self.__label.text()
        size = QSize()
        if elSize is None:
            elSize = int(self.property('el-size'))
        if text == '':
            self.layout().setContentsMargins(5, 5, 5, 5)
            self.__label.setVisible(False)
            size.setWidth(elSize)
        else:
            self.layout().setContentsMargins(20, 5, 20, 5)
            self.__label.setVisible(True)
            width = int(
                (WidgetTool.getTextWidth(self.__label) + 60) * (elSize/int(ElePyButton.Size.COMMON.value))
            )
            if self.property('icon') or self.property('icon-path'):
                width += int(int(elSize/2.5))
            size.setWidth(width)
        size.setHeight(elSize)
        WidgetTool.setFont(self.__label, int(elSize/4))
        self.__icon.setFontPixel(int(elSize/2))
        self.setFixedSize(size)

    def setText(self, text: str) -> 'ElePyButton':
        self.__label.setText(text)
        self.refreshSize()
        return self

    def text(self) -> str:
        return self.__label.text()

    def __setIcon(
        self
        , iconUnicode: str = '', iconPath: str = ''
        , iconPos: IconPos = IconPos.LEFT
    ) -> 'ElePyButton':
        icon = self.__icon
        label = self.__label
        layout = self.layout()

        layout.removeWidget(icon)
        layout.removeWidget(label)
        if iconPos in [ElePyButton.IconPos.CENTER, ElePyButton.IconPos.LEFT]:
            layout.addWidget(icon)
            layout.addWidget(label)
        else:
            layout.addWidget(label)
            layout.addWidget(icon)

        if iconUnicode != '':
            icon.setText(iconUnicode)
        if iconPath != '':
            icon.setPixmap(
                QPixmap(iconPath).scaled(icon.size())
            )

        if iconUnicode == '' and iconPath == '':
            icon.hide()
        else:
            icon.show()

        self.refreshSize()
        return self

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super(ElePyButton, self).mousePressEvent(event)
        if not WidgetTool.getProperty(
            'disabled', False
        )(self):
            if event.buttons() == Qt.LeftButton:
                self.clicked.emit()

    def enterEvent(self, event: QEvent) -> None:
        super(ElePyButton, self).enterEvent(event)
        self.setProperty('hover', True)

    def leaveEvent(self, event: QEvent) -> None:
        super(ElePyButton, self).leaveEvent(event)
        self.setProperty('hover', False)

    @watchProperty({'disabled': {'type': bool}})
    def disabledChange(self, newVal, *args):
        cursors = {
            True: Qt.ForbiddenCursor,
            False: Qt.PointingHandCursor
        }
        self.setCursor(cursors[newVal])
        self.update()

    @watchProperty({
        'icon': {'type': str},
        'icon-path': {'type': str},
        'icon-pos': {'type': IconPos}
    })
    def iconChange(
        self, newVal: Union[str, IconPos], oldVal: Union[str, IconPos], name: str
    ):
        def __setData():
            if name == 'icon':
                self.__setIcon(newVal)
            elif name == 'icon-path':
                self.__setIcon('', newVal)
            elif name == 'icon-pos':
                self.__setIcon(iconPos=newVal)
        if self._lifeStage in [
            LifeStage.INIT_DATA,
            LifeStage.INITED,
        ]:
            __setData()
        else:
            self.__initData__['icon-data'] = __setData

    @watchProperty({'type': {'type': Type}})
    def typeChange(self, newType: Type, *args):
        QWidget.setProperty(self, 'type', newType.name.lower())
        return False

    @watchProperty({'text': {'type': str}})
    def textChange(self, newText, *args):
        if self._lifeStage not in [
            LifeStage.INIT_DATA, LifeStage.INITED
        ]: self.__initData__['text'] = newText
        else: self.setText(newText)

    @watchProperty({'el-size': {'type': str}})
    def sizeChange(self, *args):
        if self._lifeStage in [
            LifeStage.INIT_DATA, LifeStage.INITED
        ]: self.refreshSize(int(args[0]))
