#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from typing import Callable, Any

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

from src.rightClickHelper.component.elePyWidget import ElePyWidget, watchProperty
from src.rightClickHelper.component.popover.elePyPopover import ElePyPopover
from src.rightClickHelper.tool.widgetTool import WidgetTool

class MenuPopoverMode(Enum):
    LIGHT   = 0X000000
    DARK    = 0X000001

class PopoverMenuItem(
    ElePyWidget
):
    clicked = pyqtSignal(object)

    def __init__(
        self, parent=None, properties: dict = {}
    ):
        super().__init__(parent, {
            'status': '',
            **properties
        })

    def _initUi(self):
        menuItemVL = QHBoxLayout()
        self.setLayout(menuItemVL)
        menuItemVL.setContentsMargins(5, 0, 0, 0)
        menuItemVL.setSpacing(8)

        width = 15
        if WidgetTool.getProperty('isWithIconMenu', False)(self):
            icon = QLabel(self)
            icon.setFixedSize(16, 25)
            icon.setPixmap(
                QPixmap(
                    WidgetTool.getProperty('icon', '')(self)
                ).scaled(icon.width(), icon.width())
            )
            menuItemVL.addWidget(icon)
            width += icon.width() + 5

        label = QLabel(self)
        label.setText(
            WidgetTool.getProperty('label', '')(self)
        )
        WidgetTool.setFont(label)
        menuItemVL.addWidget(label)
        width += WidgetTool.getTextWidth(label)
        self.label = label

        self.initUiBeforeWidth = QSize(width, 25)

        def setSize(maxWidth):
            self.setFixedSize(maxWidth, 25)
        self.computedAllItemMaxWidth = setSize

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        super(PopoverMenuItem, self).mousePressEvent(event)
        if WidgetTool.getProperty('status', '')(self) == 'forbidden': return
        if event.buttons() == Qt.LeftButton:
            self.clicked.emit(self)

    @watchProperty({
        'status': {'type': str}
    })
    def statusChange(self, newVal, oldVal, name):
        if newVal is None or newVal == '':
            self.setCursor(Qt.PointingHandCursor)
        elif newVal == 'forbidden':
            self.setCursor(Qt.ForbiddenCursor)

class ElePyMenuPopover(
    ElePyPopover
):
    itemClicked = pyqtSignal(PopoverMenuItem)

    def __init__(
        self, parent=None, properties: dict = {}
    ):
        super().__init__(parent, properties)
        self.menuItemWs = []        # type: list[PopoverMenuItem]
        self.propertyChange.connect(
            lambda name, value, returnData:
                self.refreshData(value) if name == 'menu-popover-items' else None
        )

    def setWidget(self, widget: QWidget) -> None:
        super(ElePyMenuPopover, self).setWidget(widget)
        self.refreshData()

    def refreshData(self, items: [dict[str, str]] = None):
        if items is None: items = WidgetTool.getProperty('menu-popover-items', [])(self)

        menuItems = self.widget().popoverContent    # type: QWidget
        menuItemsHL = menuItems.layout()            # type: QVBoxLayout
        mode = WidgetTool.getProperty(
            'menu-popover-mode', MenuPopoverMode.LIGHT
        )(self)
        menuItems.setStyleSheet(f'''\
        .PopoverMenuItem[status='']:hover {{
            border-radius: 4px;
            background-color: rgba(200, 200, 200, 100);
        }}
        .PopoverMenuItem[status=''] QLabel {{
            color: {
                'black' if mode == MenuPopoverMode.LIGHT else 'white'
            };
        }}
        .PopoverMenuItem[status='forbidden'] QLabel {{
            color: rgb(200, 200, 200);
        }}
        .PopoverMenuItem[status=''] QLabel:hover {{
            color: rgba(50, 150, 220);
        }}''')

        menuItemsHL.setContentsMargins(0, 5, 0, 5)
        menuItemsHL.setSpacing(0)

        def clicked(menuItem: PopoverMenuItem):
            self.itemClicked.emit(menuItem)
            if WidgetTool.getProperty(
                'clicked-auto-hide', True
            )(menuItem): self.hide()

        maxWidth = 0; sumHeight = 0
        withIcon = False
        for item in items:  # type: dict
            icon = item.get('icon', None)
            if icon is not None and icon != '':
                withIcon = True; break

        for item in items:
            menuItemW = PopoverMenuItem(menuItems, {
                'isWithIconMenu': withIcon,
                **item
            })
            size = menuItemW.initUiBeforeWidth
            menuItemsHL.addWidget(menuItemW)
            menuItemW.clicked.connect(clicked)
            self.menuItemWs.append(menuItemW)

            maxWidth = maxWidth if maxWidth > size.width() else size.width()
            sumHeight += size.height()

        for menuItemW in self.menuItemWs: menuItemW.computedAllItemMaxWidth(maxWidth)
        menuItems.setFixedSize(maxWidth, sumHeight + 10)
        self.widget().setFixedSize(
            menuItems.size().width()  + self.shadowRadius * 2 + 10,
            menuItems.size().height() + self.shadowRadius * 2
        )

    def changeItemStatus(self, index: int, status: str = ''):
        if index < 0 or index > len(self.menuItemWs):
            raise ValueError('Index out of range.')
        self.menuItemWs[index].setProperty('status', status)

    @staticmethod
    def setMenu(
        widget: QWidget, items: [dict[str, str]], properties: dict = {}
        , mode: MenuPopoverMode = MenuPopoverMode.LIGHT
        , createPopover: Callable[
            [Any, QWidget, dict], 'ElePyMenuPopover'
        ] = None
    ):
        properties = {
            'popover-trigger':      'hover'
            , 'animation-type':      'fadeInOut'
            , 'menu-popover-items':  items
            , 'menu-popover-mode':   mode
            , **properties
        }

        menuItems = QWidget()
        menuItemsHL = QVBoxLayout()
        menuItems.setLayout(menuItemsHL)

        setting = {}
        if mode == MenuPopoverMode.LIGHT:
            setting['background-color'] = [255, 255, 255]
        elif mode == MenuPopoverMode.DARK:
            setting['background-color'] = [48, 49, 51]
        ElePyPopover.setPopoverWithBackground(
            widget, menuItems, properties
            , setting=setting
            , createPopover=createPopover
            , PopoverClass=ElePyMenuPopover
        )
