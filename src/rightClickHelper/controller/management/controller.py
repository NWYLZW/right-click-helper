#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from src.rightClickHelper.controller.management.menuItemCard import MenuItemCard, MenuItemCard_Package, MenuItemCard_New
from src.rightClickHelper.tool.regTool import RegTool, RegEnv, MenuItem

from src.rightClickHelper.view.management import index as management

class ManagementController(
    QtWidgets.QWidget,
    management.Ui_management
):
    def __init__(self, parent=None):
        super(ManagementController, self).__init__(parent)
        self._initUI()
        self._initData()
        self._initEvent()

    def _initUI(self):
        self.setupUi(self)
        self.currentRegPath.setText(
            self.selKind.currentText() + '/'
        )

        self.itemScrollAreaWidgetVL = QVBoxLayout()
        self.itemScrollAreaWidgetVL.setContentsMargins(0, 0, 0, 0)
        self.itemScrollAreaWidget.setLayout(
            self.itemScrollAreaWidgetVL
        )

    def clearShowMenuItems(self):
        for HLW in self.listHLWs:   # type: QWidget
            HLW.setParent(None)
            HLW.deleteLater()

        self.listHLWs = []      # type: [QWidget]
        self.menuItemCards = [] # type: [MenuItemCard]

    def loadShowMenuItem(self, showMenuItem: MenuItem, itemType: str, lineNum: int):
        lineWidth = 1100; lineHeight = 180

        index = len(self.menuItemCards)
        if index % lineNum == 0:
            HLW = QWidget(self.itemScrollAreaWidget)
            HLW.setGeometry(QtCore.QRect(
                0, int(index / lineNum) * lineHeight, lineWidth, lineHeight
            ))
            self.itemScrollAreaWidgetVL.addWidget(HLW)
            self.listHLWs.append(HLW)

        menuItemGenerator = {
            '': MenuItemCard,
            'new': MenuItemCard_New,
            'package': MenuItemCard_Package
        }
        menuItemCard = menuItemGenerator[itemType](
            self.listHLWs[len(self.listHLWs) - 1]
        ) # type: MenuItemCard
        if itemType != 'new':
            self.menuItemCards.append(menuItemCard)

        menuItemCard.setGeometry(QtCore.QRect(
            index % lineNum * menuItemCard.width(), 0, menuItemCard.width(), menuItemCard.height()
        ))
        menuItemCard.setData(showMenuItem)

    def loadShowMenuItems(self):
        self.clearShowMenuItems()

        waitLoadMenuItems = [
            *self.showMenuItems, {}
        ] # type: [MenuItem]
        for index in range(len(waitLoadMenuItems)):
            if index == len(waitLoadMenuItems) - 1:
                itemType = 'new'
            else:
                if waitLoadMenuItems[index].isPackage:
                    itemType = 'package'
                else:
                    itemType = ''

            self.loadShowMenuItem(
                waitLoadMenuItems[index], itemType, 9
            )

        lineHeight = 180
        self.itemScrollAreaWidget\
            .setMinimumHeight(len(self.listHLWs) * lineHeight)

    def refreshShowMenuItems(self, searchStr: str = ''):
        if searchStr == '':
            self.showMenuItems = self.menuItems.copy()
        else:
            self.showMenuItems = []
            for menuItem in self.menuItems:
                if re.match('.*' + searchStr + '.*', menuItem.name) or re.match('.*' + searchStr + '.*', menuItem.title):
                    self.showMenuItems.append(
                        menuItem
                    )
        self.loadShowMenuItems()

    def refreshMenuItems(self, regData: tuple):
        self.menuItems = []
        # type: [MenuItem]

        regDataTree = RegTool.recursion(*regData)
        for key, val in regDataTree.items():
            if key[:2] != '__':
                self.menuItems.append(
                    MenuItem(key, regDataTree[key])
                )
        self.refreshShowMenuItems()

    def _initData(self):
        self.listHLWs = []  # type: [QWidget]
        self.regDatas = {
            '文件':
                (RegEnv.HKEY_CLASSES_ROOT, r'*\shell', 3),
            '文件夹':
                (RegEnv.HKEY_CLASSES_ROOT, r'Folder\shell', 3),
            '目录':
                (RegEnv.HKEY_CLASSES_ROOT, r'Directory\shell', 3),
            '目录背景':
                (RegEnv.HKEY_CLASSES_ROOT, r'Directory\Background\shell', 3),
            '桌面背景':
                (RegEnv.HKEY_CLASSES_ROOT, r'DesktopBackground\Shell', 3)
        }
        self.refreshMenuItems(self.regDatas.get(
            self.selKind.currentText(), []
        ))

    def createListRefresh(self, mode):
        def selEnd():
            self.refreshMenuItems(self.regDatas.get(
                self.selKind.currentText(), []
            ))
            self.currentRegPath.setText(
                self.selKind.currentText() + '/'
            )

        def searchEnd():
            self.refreshShowMenuItems(
                self.searchInput.text()
            )

        return {
            'menuItems': selEnd,
            'showMenuItems': searchEnd
        }.get(mode, lambda: print('未知错误'))

    def _initEvent(self):
        self.searchInput.returnPressed \
            .connect(
                self.createListRefresh('showMenuItems')
            )
        self.selKind.currentTextChanged \
            .connect(
                self.createListRefresh('menuItems')
            )