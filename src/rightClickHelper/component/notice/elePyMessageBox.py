#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from typing import Union, Callable, Any

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QTextBrowser

from src.rightClickHelper.component.elePyDialog import ElePyDialog
from src.rightClickHelper.component.form.elePyButton import ElePyButton
from src.rightClickHelper.component.label.elePyIcon import ElePyIcon
from src.rightClickHelper.component.label.elePyLabel import ElePyLabel
from src.rightClickHelper.tool.animationTool import AnimationTool
from src.rightClickHelper.tool.widgetTool import WidgetTool

class AlertAction(Enum):
    CANCEL  = 0x000
    CONFIRM = 0x001

class ElePyMessageBox(
    ElePyDialog
):
    __instance__ = None

    @staticmethod
    def instance() -> 'ElePyMessageBox':
        if hasattr(ElePyMessageBox, '__instance__'):
            setattr(ElePyMessageBox, '__instance__', ElePyMessageBox())
        return ElePyMessageBox.__instance__

    def __init__(self, parent=None, properties: dict = None):
        super().__init__(parent, properties)

    def _initUi(self):
        super(ElePyMessageBox, self)._initUi()
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.setSQSS(
            self.__class__.getResource('sqss/component/ele_py_message_box.sqss')
        )

        self.setFixedSize(360, 180)
        mainWidget = QWidget(self)
        mainWidget.setFixedSize(self.size())
        self.layout().addWidget(mainWidget)
        self.mainWidget = mainWidget

        mainWidget.setLayout(QVBoxLayout())
        mainWidget.layout().setContentsMargins(10, 10, 10, 10)
        mainWidget.layout().setSpacing(0)

        top = QWidget()
        top.setProperty('class', 'top')
        top.setFixedSize(mainWidget.width() - 20, 40)
        top.setLayout(QHBoxLayout())
        top.setCursor(Qt.SizeAllCursor)
        self.top = top

        icon = ElePyIcon(top)
        icon.setFontPixel(20)
        top.layout().addWidget(icon)
        self.leftIcon = icon

        title = ElePyLabel(top)
        WidgetTool.setFont(title, size=12)
        title.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        title.setCursor(
            Qt.IBeamCursor
        )
        top.layout().addWidget(title)
        self.title = title

        deleteIcon = ElePyIcon(top, {'text': '&#xe65e;'})
        deleteIcon.setObjectName('delete')
        deleteIcon.setFontPixel(20)
        deleteIcon.setCursor(Qt.PointingHandCursor)
        deleteIcon.clicked.connect(self.close)
        top.layout().addWidget(deleteIcon)

        mainWidget.layout().addWidget(top)

        content = QWidget()
        content.setProperty('class', 'content')
        content.setLayout(QHBoxLayout())
        contentText = QTextBrowser(content)
        WidgetTool.setFont(contentText)
        contentText.viewport().setCursor(
            Qt.IBeamCursor
        )
        content.layout().addWidget(contentText)
        self.contentText = contentText

        mainWidget.layout().addWidget(content)

        bottom = QWidget()
        bottom.setProperty('class', 'bottom')
        bottom.setFixedSize(mainWidget.width() - 20, 60)
        self.bottom = bottom

        mainWidget.layout().addWidget(bottom)

    def _initData(self):
        self.mDrag = False

    def _initEvent(self):
        def mousePressEvent(event):
            self.mDragPosition = event.globalPos() - self.pos()
            if event.button() == Qt.LeftButton:
                self.mDrag = True
                event.accept()

        def mouseMoveEvent(event):
            if event.buttons() == Qt.LeftButton and self.mDrag:
                self.move(event.globalPos() - self.mDragPosition)
                event.accept()

        def mouseReleaseEvent(QMouseEvent):
            self.mDrag = False

        self.top.mousePressEvent   = mousePressEvent
        self.top.mouseMoveEvent    = mouseMoveEvent
        self.top.mouseReleaseEvent = mouseReleaseEvent

    def show(self) -> None:
        super(ElePyMessageBox, self).show()
        AnimationTool.createReverse(
            self, False
        )()

    def close(self) -> bool:
        AnimationTool.createReverse(
            self, True, super(ElePyMessageBox, self).close
        )()
        return True

    def alert(
        self
        , content: str, title: str = 'Please confirm'
        , leftIcon: str = '&#xe6a8;'
        , confirmBtnText: str = 'confirm'
        , callback: Callable[[AlertAction], Any] = None
    ):
        self.contentText.setHtml(content)
        self.title.setText(title)
        self.leftIcon.setText(leftIcon)

        self.bottom.setLayout(QHBoxLayout())
        self.bottom.layout().setAlignment(
            Qt.AlignRight
        )
        confirmBtn = ElePyButton(self.bottom, {
            'text': confirmBtnText,
            'type': ElePyButton.Type.PRIMARY,
            'el-size': ElePyButton.Size.SMALL.value
        })
        self.bottom.layout().addWidget(confirmBtn)

        def clicked():
            if callback: callback(AlertAction.CONFIRM)
            self.close()
        confirmBtn.clicked.connect(clicked)

        self.show()
