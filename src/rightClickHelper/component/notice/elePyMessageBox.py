#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from typing import Callable, Any

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QTextBrowser

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
        mainWidget.layout().setSpacing(0)

        top = QWidget()
        top.setProperty('class', 'top')
        top.setFixedHeight(40)
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
        self.content = content
        self.contentText = contentText

        mainWidget.layout().addWidget(content)

        bottom = QWidget()
        bottom.setProperty('class', 'bottom')
        bottom.setFixedHeight(60)
        bottom.setLayout(QHBoxLayout())
        self.bottom = bottom
        self.cancelBtn = self.pushBtn()
        self.confirmBtn = self.pushBtn(properties={
            'type': ElePyButton.Type.PRIMARY
        })

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

        self.contentText.setOpenLinks(False)
        self.contentText.anchorClicked.connect(
            lambda url: QDesktopServices.openUrl(url)
        )

    def exec(self) -> int:
        self.setWindowModality(Qt.ApplicationModal)
        self.show()

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

    def setBaseData(
        self
        , content: str, title: str = 'Please confirm'
        , leftIcon: str = '&#xe6a8;'
        , contentWidth: int = -1
        , contentHeight: int = -1
    ):
        self.contentText.setHtml(content)

        if contentWidth != -1:
            self.setFixedWidth(contentWidth + 40)
        if contentHeight != -1:
            self.setFixedHeight(contentHeight + 100)

        self.mainWidget.setFixedSize(self.size())
        self.title.setText(title)
        self.leftIcon.setText(leftIcon)

    def pushBtn(
        self
        , text: str = ''
        , properties: dict = {}
    ) -> ElePyButton:
        self.bottom.layout().setAlignment(
            Qt.AlignRight
        )
        btn = ElePyButton(self.bottom, {
            'text': text,
            'el-size': ElePyButton.Size.SMALL.value
            , **properties
        })
        self.bottom.layout().addWidget(btn)
        return btn

    def setBtn(
        self, btn: ElePyButton, isShow: bool = True
        , text: str = ''
        , callback: Callable[[AlertAction], Any] = None
        , alertAction: AlertAction = AlertAction.CONFIRM
    ):
        def clicked():
            if callback:
                val = callback(alertAction)
                if val is None or val is True:
                    self.close()
            else:
                self.close()
        btn.setVisible(isShow)
        btn.setText(text)
        btn.clicked.connect(clicked)

    def alert(
        self
        , content: str, title: str = 'Please confirm'
        , leftIcon: str = '&#xe6a8;'
        , confirmBtnText: str = 'confirm'
        , callback: Callable[[AlertAction], Any] = None
        , contentWidth: int = -1
        , contentHeight: int = -1
    ):
        self.setBaseData(
            content, title, leftIcon
            , contentWidth=contentWidth, contentHeight=contentHeight
        )
        self.setBtn(
            self.cancelBtn, False)
        self.setBtn(
            self.confirmBtn, True
            , confirmBtnText, callback
            , AlertAction.CONFIRM)
        self.exec()

    def confirm(
        self
        , content: str, title: str = 'Please confirm'
        , leftIcon: str = '&#xe6a8;'
        , confirmBtnText: str = 'confirm'
        , confirmCallback: Callable[[AlertAction], Any] = None
        , cancelBtnText: str = 'cancel'
        , cancelCallback: Callable[[AlertAction], Any] = None
        , contentWidth: int = -1
        , contentHeight: int = -1
    ):
        self.setBaseData(
            content, title, leftIcon
            , contentWidth=contentWidth, contentHeight=contentHeight
        )
        self.setBtn(
            self.confirmBtn, True
            , confirmBtnText, confirmCallback
            , AlertAction.CONFIRM)
        self.setBtn(
            self.cancelBtn, True
            , cancelBtnText, cancelCallback
            , AlertAction.CANCEL)
        self.exec()
