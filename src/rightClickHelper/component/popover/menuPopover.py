#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

from src.rightClickHelper.component.popover.popover import Popover
from src.rightClickHelper.tool.widgetTool import WidgetTool

class MenuPopoverMode(Enum):
    LIGHT   = 0X000000
    DARK    = 0X000001

class PopoverMenuItem:
    def __init__(
        self, title: str, icon: str = ''
    ):
        self.title = title
        self.icon = icon

    def createWidget(
        self, parent: QWidget, mode: MenuPopoverMode = MenuPopoverMode.LIGHT
    ) -> (QWidget, QSize):
        menuItemW = QWidget(parent)
        menuItemW.setObjectName('menuItemW')
        menuItemW.setCursor(Qt.PointingHandCursor)

        menuItemVL = QHBoxLayout()
        menuItemW.setLayout(menuItemVL)
        menuItemVL.setContentsMargins(5, 5, 5, 5)
        menuItemVL.setSpacing(5)

        if mode == MenuPopoverMode.LIGHT:
            menuItemW.setStyleSheet(f'''\
            #{menuItemW.objectName()} {{
                border-radius: 4px;
            }}
            #{menuItemW.objectName()}:hover {{
                background-color: rgba(240, 240, 240);
            }}
            #{menuItemW.objectName()} QLabel {{
                padding: 5px;
                color: black;
            }}''')
        elif mode == MenuPopoverMode.DARK:
            menuItemW.setStyleSheet(f'''\
            #{menuItemW.objectName()} {{
                border-radius: 4px;
            }}
            #{menuItemW.objectName()}:hover {{
                background-color: rgba(100, 100, 100);
            }}
            #{menuItemW.objectName()} QLabel {{
                padding: 5px;
                color: white;
            }}''')

        title = QLabel(menuItemW)
        title.setText(self.title)
        WidgetTool.setFont(title)
        menuItemVL.addChildWidget(title)

        def setSize(maxWidth):
            title\
                .setFixedSize(maxWidth, 25)
            menuItemW\
                .setFixedSize(maxWidth, 25)
        menuItemW.computedAllItemMaxWidth = setSize

        return (
            menuItemW, QSize(WidgetTool.getTextWidth(title) + 20, 25)
        )

class MenuPopover(
    Popover
):
    itemClicked = pyqtSignal(PopoverMenuItem, QWidget, name='itemClicked')

    def __init__(
        self, parent=None, properties: dict = {}
    ):
        super().__init__(parent, properties)

    def setWidget(self, widget: QWidget) -> None:
        super(MenuPopover, self).setWidget(widget)
        self.refreshData()

    def refreshData(self, items: [PopoverMenuItem] = None):
        if items is None: items = WidgetTool.getProperty('menu-popover-items', [])(self)

        menuItems = self.widget().popoverContent    # type: QWidget
        menuItemsHL = menuItems.layout()            # type: QVBoxLayout

        menuItemsHL.setContentsMargins(0, 5, 0, 5)
        menuItemsHL.setSpacing(0)

        def createForwardClicked(menuItem: PopoverMenuItem, widget: QWidget):
            def forwardClicked(event: QtGui.QMouseEvent):
                if event.buttons() == Qt.LeftButton:
                    self.itemClicked.emit(menuItem, widget)

            return forwardClicked

        maxWidth = 0; sumHeight = 0
        menuItemWs = []
        for menuItem in items:  # type: PopoverMenuItem
            (menuItemW, size) = menuItem.createWidget(
                menuItems, mode=WidgetTool.getProperty(
                    'menu-popover-mode', MenuPopoverMode.LIGHT
                )(self)
            )
            maxWidth = maxWidth if maxWidth > size.width() else size.width()
            sumHeight += size.height()

            menuItemsHL.addWidget(menuItemW)
            menuItemW.mousePressEvent = createForwardClicked(menuItem, menuItemW)

            menuItemWs.append(menuItemW)

        for menuItemW in menuItemWs: menuItemW.computedAllItemMaxWidth(maxWidth)
        menuItems.setFixedSize(maxWidth, sumHeight + 10)
        self.widget().setFixedSize(
            menuItems.size().width()  + self.shadowRadius * 2 + 10,
            menuItems.size().height() + self.shadowRadius * 2
        )

    @staticmethod
    def setMenu(
        widget: QWidget, items: [PopoverMenuItem], properties: dict = {},
        mode: MenuPopoverMode = MenuPopoverMode.LIGHT
    ):
        properties['popover-trigger'] = properties.get('popover-trigger', 'click')
        properties['menu-popover-items'] = items
        properties['menu-popover-mode'] = mode

        menuItems = QWidget()
        menuItemsHL = QVBoxLayout()
        menuItems.setLayout(menuItemsHL)

        setting = {}
        if mode == MenuPopoverMode.LIGHT:
            setting['background-color'] = [255, 255, 255]
        elif mode == MenuPopoverMode.DARK:
            setting['background-color'] = [48, 49, 51]
        Popover.setPopoverWithBackground(
            widget, menuItems, properties
            , setting=setting
            , PopoverClass=MenuPopover
        )
