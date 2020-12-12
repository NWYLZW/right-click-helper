#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from abc import abstractmethod

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

from src.rightClickHelper.tool.PathTool import PathTool
from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.tool.regTool import MenuItem
from src.rightClickHelper.tool.systemTool import SystemTool

from src.rightClickHelper.view.management import menuItemCard, menuItemCard_new, menuItemCard_package

class MenuItemCard_itf:
    def _initUI(self):
        try:
            self.setupUi(self)
            EffectTool.setBlur(self)

            self.maskCard.hide()
        except Exception as e: raise e

    def createChangeStatus(self):
        def changeStatus(event):
            result = QMessageBox.question(
                self, '提示', '是否打开该右键菜单',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
        return changeStatus

    def _initEvent(self):
        try:
            self.icon.enterEvent = lambda e: \
                self.maskCard.show()

            maskHide = lambda e: \
                self.maskCard.hide()
            self.leaveEvent = maskHide
            self.title.enterEvent = maskHide
            self.maskCard.leaveEvent = maskHide

            self.switchItem.mousePressEvent = \
                self.createChangeStatus()
        except Exception as e: raise e

    @abstractmethod
    def setIcon(self, menuItem: MenuItem):
        pass

    def customSetData(self, menuItem: MenuItem):
        pass

    def setTitle(self, menuItem: MenuItem):
        try:
            self.title.setText(menuItem.name)
            self.title.setToolTip(menuItem.name)
        except Exception as e: raise e

    def setData(self, menuItem: MenuItem):
        self.menuItem = menuItem
        self.setIcon(menuItem)
        self.setTitle(menuItem)
        self.customSetData(menuItem)

class MenuItemCard(
    QtWidgets.QWidget,
    menuItemCard.Ui_item,
    MenuItemCard_itf
):
    def __init__(self, parent=None):
        super(MenuItemCard, self).__init__(parent)
        self._initUI()
        self._initEvent()

    def setIcon(self, menuItem: MenuItem):
        if menuItem.icon != '':
            self.icon.setPixmap(
                SystemTool.getIcon(menuItem.icon)
            )

    def customSetData(self, menuItem: MenuItem):
        self.switchItem.setProperty('status', 'open' if menuItem.isHide else 'close')
        self.switchItem.setToolTip(
            '隐藏该选项' if menuItem.isHide else '显示该选项'
        )

class MenuItemCard_Package(
    QtWidgets.QWidget,
    menuItemCard_package.Ui_item,
    MenuItemCard_itf
):
    def __init__(self, parent=None):
        super(MenuItemCard_Package, self).__init__(parent)
        self._initUI()
        self._initEvent()

    def setIcon(self, menuItem: MenuItem):
        if menuItem.icon != '':
            self.showIcon.setPixmap(
                SystemTool.getIcon(menuItem.icon)
            )
        else:
            self.showIcon.setPixmap(
                QPixmap(PathTool.appPath() + r'\src\resource\image\icon\package.png').scaled(30, 30)
            )

        ions = [
            self.icon_1, self.icon_2, self.icon_3, self.icon_4
        ]
        children = menuItem.children
        for index in range(0, 4 if len(children) > 4 else len(children)):
            child = children[index]
            ions[index].setPixmap(SystemTool.getIcon(child.icon))

    def customSetData(self, menuItem: MenuItem):
        self.switchItem.setProperty('status', 'open' if menuItem.isHide else 'close')
        self.switchItem.setToolTip(
            '隐藏该选项' if menuItem.isHide else '显示该选项'
        )


class MenuItemCard_New(
    QtWidgets.QWidget,
    menuItemCard_new.Ui_item
):
    def __init__(self, parent=None):
        super(MenuItemCard_New, self).__init__(parent)
        self._initUI()
        self._initEvent()

    def _initUI(self):
        self.setupUi(self)
        EffectTool.setBlur(self)

    def _initEvent(self): pass

    def setData(self, menuItem: MenuItem):
        self.menuItem = menuItem
