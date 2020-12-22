#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

from src.rightClickHelper.component.popover.popover import Popover

class MenuPopoverMode(Enum):
    LIGHT   = 0X000000
    DARK    = 0X000001

class MenuItem:
    def __init__(
        self, title: str, icon: str = ''
    ):
        self.title = title
        self.icon = icon

class MenuPopover(
    Popover
):
    itemClicked = pyqtSignal(MenuItem, name='itemClicked')

    def __init__(
        self, parent=None, properties: dict = {}
    ):
        super(Popover).__init__(parent, properties)

    @staticmethod
    def setMenu(
        widget: QWidget, items: [MenuItem], properties: dict = {},
        mode: MenuPopoverMode = MenuPopoverMode.LIGHT
    ):
        menuItems = QWidget()
        menuItemsHL = QHBoxLayout()
        menuItems.setLayout(menuItemsHL)
        menuItems.setFixedSize(100, 100)
        menuItemsHL.setContentsMargins(10, 10, 10, 10)
        for menuItem in items:              # type: MenuItem
            menuItemW = QWidget(menuItems)
            menuItemVL = QVBoxLayout()
            menuItemW.setLayout(menuItemVL)
            title = QLabel(menuItemW)
            title.setText(menuItem.title)
            menuItemVL.addChildWidget(title)
            menuItemsHL.addChildWidget(menuItemW)

        setting = {}
        if mode == MenuPopoverMode.LIGHT:
            setting['background-color'] = [255, 255, 255]
        elif mode == MenuPopoverMode.DARK:
            setting['background-color'] = [48, 49, 51]
        Popover.setPopoverWithBackground(
            widget, menuItems, properties, setting=setting
        )
