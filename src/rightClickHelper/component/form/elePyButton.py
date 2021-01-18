#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from typing import Union

from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from src.rightClickHelper.component.core import LifeStage
from src.rightClickHelper.component.elePyWidget import ElePyWidget, watchProperty
from src.rightClickHelper.component.label.elePyIcon import ElePyIcon
from src.rightClickHelper.component.label.elePyLabel import ElePyLabel
from src.rightClickHelper.tool.widgetTool import WidgetTool

elePyButtonQSS = """\
.ElePyButton {
    margin: 0;
    padding: 10px 15px;
    border-radius: 4px;
    outline: none;
}
.ElePyButton[round=true] {
    border-radius: 20px;
}

.ElePyButton {
    background-color: #fff;
    border: 1px solid #dcdfe6;
}
.ElePyButton QLabel {
    color: #606266;
}
.ElePyButton[hover=true][disabled=false] {
    background-color: #ecf5ff;
    border: 1px solid #409eff;
}
.ElePyButton[plain=true][hover=true][disabled=false] {
    background-color: #fff;
}
.ElePyButton[hover=true][disabled=false] QLabel {
    color: #409eff;
}

.ElePyButton[type='primary'] {
    background-color: #409eff;
    border: 1px solid #409eff;
}
.ElePyButton[plain=true][type='primary'] {
    background-color: #ecf5ff;
}
.ElePyButton[type='primary'] QLabel {
    color: #fff;
}
.ElePyButton[plain=true][type='primary'] QLabel {
    color: #409eff;
}
.ElePyButton[type='primary'][hover=true][disabled=false] {
    background-color: #66b1ff;
}
.ElePyButton[plain=true][type='primary'][hover=true][disabled=false] {
    background-color: #409eff;
}
.ElePyButton[type='primary'][hover=true][disabled=false] QLabel {
    color: #fff;
}

.ElePyButton[type='success'] {
    background-color: #67c23a;
    border: 1px solid #67c23a;
}
.ElePyButton[plain=true][type='success'] {
    background-color: #f0f9eb;
}
.ElePyButton[type='success'] QLabel {
    color: #fff;
}
.ElePyButton[plain=true][type='success'] QLabel {
    color: #67c23a;
}
.ElePyButton[type='success'][hover=true][disabled=false] {
    background-color: #85ce61;
}
.ElePyButton[type='success'][hover=true][disabled=false] QLabel {
    color: #fff;
}

.ElePyButton[type='info'] {
    background-color: #909399;
    border: 1px solid #909399;
}
.ElePyButton[plain=true][type='info'] {
    background-color: #f4f4f5;
}
.ElePyButton[type='info'] QLabel {
    color: #fff;
}
.ElePyButton[plain=true][type='info'] QLabel {
    color: #909399;
}
.ElePyButton[type='info'][hover=true][disabled=false] {
    background-color: #a6a9ad;
}
.ElePyButton[type='info'][hover=true][disabled=false] QLabel {
    color: #fff;
}

.ElePyButton[type='warning'] {
    background-color: #e6a23c;
    border: 1px solid #e6a23c;
}
.ElePyButton[plain=true][type='warning'] {
    background-color: #fdf6ec;
}
.ElePyButton[type='warning'] QLabel {
    color: #fff;
}
.ElePyButton[plain=true][type='warning'] QLabel {
    color: #e6a23c;
}
.ElePyButton[type='warning'][hover=true][disabled=false] {
    background-color: #ebb563;
}
.ElePyButton[type='warning'][hover=true][disabled=false] QLabel {
    color: #fff;
}

.ElePyButton[type='danger'] {
    background-color: #f56c6c;
    border: 1px solid #f56c6c;
}
.ElePyButton[plain=true][type='danger'] {
    background-color: #fef0f0;
}
.ElePyButton[type='danger'] QLabel {
    color: #fff;
}
.ElePyButton[type='danger'][hover=true][disabled=false] {
    background-color: #f78989;
}
.ElePyButton[plain=true][type='danger'] QLabel {
    color: #f56c6c;
}
.ElePyButton[type='danger'][hover=true][disabled=false] QLabel {
    color: #fff;
}"""

class ElePyButton(
    ElePyWidget
):
    class Size(Enum):
        MEDIUM = 0X000
        SMALL  = 0X001
        MINI   = 0X002

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
            'text': '',
            'disabled': False,
            **properties
        })

    def _initUi(self):
        super(ElePyButton, self)._initUi()
        self.setStyleSheet(elePyButtonQSS)
        self.setLayout(QHBoxLayout())

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

    def setText(self, text: str) -> 'ElePyButton':
        self.__label.setText(text)
        if text == '':
            self.__label.setVisible(False)
            self.setFixedSize(40, 40)
        else:
            self.__label.setVisible(True)
            width = WidgetTool.getTextWidth(self.__label) + 50
            self.setFixedSize(width, 40)
        return self

    def text(self) -> str:
        return self.__label.text()

    def setIcon(
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

        return self

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super(ElePyButton, self).mousePressEvent(event)
        if WidgetTool.getProperty(
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
                self.setIcon(newVal)
            elif name == 'icon-path':
                self.setIcon('', newVal)
            elif name == 'icon-pos':
                self.setIcon(iconPos=newVal)
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
