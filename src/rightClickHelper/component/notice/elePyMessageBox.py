#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from typing import Union, Callable, Any

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QTextBrowser

from src.rightClickHelper.component.elePyDialog import ElePyDialog
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

        self.setStyleSheet('''\
        .ElePyMessageBox >QWidget {
            margin: 10px;
            border-radius: 4px;
            background-color: white;
        }
        .ElePyMessageBox >QWidget .top #delete:!hover {
            color: rgb(150, 150, 150);
        }
        .ElePyMessageBox >QWidget .top #delete:hover {
            color: rgb(0, 0, 0);
        }
        .ElePyMessageBox >QWidget .content QTextBrowser {
            border-width: 0;
            border-style: outset;
            background-color: rgba(0, 0, 0, 0);
        }
        .ElePyMessageBox >QWidget .bottom {
        }''')

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

        icon = ElePyIcon(top, {'text': '&#xe6da;'})
        icon.setFontPixel(20)
        top.layout().addWidget(icon)

        title = ElePyLabel(top, {'text': '测试'})
        WidgetTool.setFont(title, size=12)
        top.layout().addWidget(title)

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
        contentText.setHtml('测试')
        content.layout().addWidget(contentText)

        mainWidget.layout().addWidget(content)

        bottom = QWidget()
        bottom.setProperty('class', 'bottom')
        bottom.setFixedSize(mainWidget.width() - 20, 40)
        bottom.setLayout(QHBoxLayout())
        bottom.layout().addWidget(QPushButton())
        bottom.layout().addWidget(QPushButton())

        mainWidget.layout().addWidget(bottom)

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
        , content: str, title: str
        , icon: Union[ElePyIcon, str] = None
        , confirmBtnText: str = 'confirm'
        , callback: Callable[[AlertAction], Any] = None
    ):
        pass
