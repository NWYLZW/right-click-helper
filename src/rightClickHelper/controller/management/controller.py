#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
from typing import ClassVar

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication

from src.rightClickHelper.component.elePyWidget import ElePyWidget, watchProperty
from src.rightClickHelper.component.notice.elePyMessage import ElePyMessage, ElePyMessageType
from src.rightClickHelper.component.popover.elePyMenuPopover import ElePyMenuPopover, PopoverMenuItem
from src.rightClickHelper.controller.management.menuItemCard import MenuItemCard, MenuItemCard_Package, MenuItemCard_New
from src.rightClickHelper.tool.pathTool import PathTool
from src.rightClickHelper.tool.regTool import RegTool, RegEnv, MenuItem, RegType

from src.rightClickHelper.view.management import index as management

class ManagementController(
    ElePyWidget,
    management.Ui_management
):
    moreOptionMenu = {
        'paste': {
            'label': '粘贴',
            'status': 'forbidden',
            'icon': PathTool.appPath() + r'\src\resource\image\common-icon\paste-ed.png'
        }
        ,'import': {
            'label': '导入',
            'icon': PathTool.appPath() + r'\src\resource\image\common-icon\import-ed.png'
        }
    }

    def __init__(
        self, parent=None, properties: dict = {}
    ):
        self.__tempList = []
        self.moreOptionPopovers = []   # type: list[ElePyMenuPopover]
        super().__init__(parent, {
            'clipboard': {
                'val': None, 'type': None
            }, **properties
        })

    def _initUi(self):
        self.setupUi(self)
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

    @watchProperty({
        'clipboard': {'type': dict}
    })
    def clipboardChange(self, clipboardData, *args):
        status = 'forbidden' if clipboardData['val'] is None else ''
        messages = {
            'copy': '复制成功',
            'cut': '剪切成功',
        }
        message = messages.get(clipboardData['type'], None)
        if message is not None:
            ElePyMessage.instance().show({
                'type': ElePyMessageType.SUCCESS,
                'message': message
            })
        if len(self.moreOptionPopovers) <= 1:
            self.__tempList.append({
                'index': 0, 'status': status
            })
        for moreOptionPopover in self.moreOptionPopovers:
            moreOptionPopover.changeItemStatus(0, status)

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

            if itemType == 'package':
                menuItemCard.clickTitle.connect(
                    lambda menuItem: self.refreshMenuItems(
                        (RegEnv.find(menuItem.regData['__path__'][0]), menuItem.regData['__path__'][1] + '\\shell')
                    )
                )
            menuItemCard.moreMenuSel.connect(
                lambda actionName, menuItem: self.setProperty('clipboard', {
                    'val': menuItem,
                    'type': actionName
                })
            )
            menuItemCard.cardRemove.connect(
                lambda: self.refreshMenuItems(self.path)
            )
        else:
            menuItemCard.createMenuItemSuccess.connect(
                lambda: self.refreshMenuItems(self.path)
            )

        menuItemCard.setGeometry(QtCore.QRect(
            index % lineNum * menuItemCard.width(), 0, menuItemCard.width(), menuItemCard.height()
        ))
        menuItemCard.setData(showMenuItem)

    def loadShowMenuItems(self):
        self.clearShowMenuItems()

        waitLoadMenuItems = [
            *self.showMenuItems, MenuItem('new menuItem', {
                '__path__': (self.path[0].value, self.path[1] + r'\new menuItem'),
                '__val__': {
                    '': ('', RegType.REG_SZ.value)
                }
            })
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
            .setMaximumHeight(len(self.listHLWs) * lineHeight)

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

    def refreshMenuItems(self, path: tuple):
        self.path = path
        currentRegPath = path[1] # type: str
        for menuItemRootName, menuItemsRoot in self.menuItemsRoots.items():
            currentRegPath = currentRegPath.replace(menuItemsRoot[1], menuItemRootName)
        self.currentRegPath.setText(currentRegPath)
        self.menuItems = []
        # type: [MenuItem]

        regDataTree = RegTool.recursion(*path, depth=3)
        for key, val in regDataTree.items():
            if key[:2] != '__':
                self.menuItems.append(
                    MenuItem(key, regDataTree[key])
                )
        self.refreshShowMenuItems()
        self.itemScrollArea.repaint(); self.itemScrollArea.update()

    def indexOfMenuItems(self, name: str) -> int:
        for i in range(len(self.menuItems)):
            if self.menuItems[i].name == name:
                return i
        return -1

    def moreOptionMenuClick(self, popoverMenuItem: PopoverMenuItem):
        if popoverMenuItem.property('label') == self.moreOptionMenu['import']['label']:
            try:
                clipboardData = json.loads(QApplication.clipboard().text())
                source = (
                    RegEnv.find(clipboardData['__path__'][0]),
                    clipboardData['__path__'][1]
                )
                split = source[1].split('\\')
                name = split[len(split) - 1]
                target = (
                    self.path[0], '\\'.join([
                        *self.path[1].split('\\')[:-1],
                        'shell', name
                    ])
                )
                if self.indexOfMenuItems(name) == -1:
                    RegTool.replacePath(
                        clipboardData, source, target
                    )
                    RegTool.writeKey(clipboardData)
                    self.refreshMenuItems(self.path)
                    ElePyMessage.instance().show({
                        'type': ElePyMessageType.SUCCESS,
                        'message': '从剪切板导入数据成功'
                    })
                else:
                    ElePyMessage.instance().show({
                        'type': ElePyMessageType.WARN,
                        'message': '当前目录存在同名菜单项'
                    })
            except: ElePyMessage.instance().show({
                'type': ElePyMessageType.WARN,
                'message': '从剪切板数据解析失败'
            })
        elif popoverMenuItem.property('label') == self.moreOptionMenu['paste']['label']:
            clipboard: dict = self.property('clipboard')

            if self.indexOfMenuItems(clipboard['val'].name) == -1:
                menuItem: MenuItem = clipboard['val']

                source = (
                    RegEnv.find(
                        menuItem.regData['__path__'][0]
                    ), menuItem.regData['__path__'][1]
                )
                target = (
                    self.path[0], '\\'.join([
                        *self.path[1].split('\\')[:-1],
                        'shell', menuItem.name
                    ])
                )
                if clipboard['type'] == 'copy':
                    RegTool.cpKey(source, target)
                elif clipboard['type'] == 'cut':
                    RegTool.mvKey(source, target)
                self.refreshMenuItems(self.path)
                ElePyMessage.instance().show({
                    'type': ElePyMessageType.SUCCESS,
                    'message': '粘贴成功'
                })
            else:
                ElePyMessage.instance().show({
                    'type': ElePyMessageType.WARN,
                    'message': '当前目录存在同名菜单项'
                })

    def createMoreMenuPopover(
        self
        , PopoverClass: ClassVar[ElePyMenuPopover], widget: QWidget, properties: dict
    ):
        for t in self.__tempList:
            items = properties.get('menu-popover-items', [])
            items[t['index']]['status'] = t['status']
        popover = PopoverClass(widget, properties)              # type: ElePyMenuPopover
        popover.itemClicked.connect(self.moreOptionMenuClick)

        def hideIts():
            for moreOptionPopover in self.moreOptionPopovers:
                moreOptionPopover.hide()
        popover.showed.connect(hideIts)
        self.moreOptionPopovers.append(popover)
        return popover

    def _initData(self):
        self.listHLWs = []  # type: [QWidget]
        self.menuItemsRoots = {
            '文件':
                (RegEnv.HKEY_CLASSES_ROOT, r'*\shell'),
            '文件夹':
                (RegEnv.HKEY_CLASSES_ROOT, r'Folder\shell'),
            '目录':
                (RegEnv.HKEY_CLASSES_ROOT, r'Directory\shell'),
            '目录背景':
                (RegEnv.HKEY_CLASSES_ROOT, r'Directory\Background\shell'),
            '桌面背景':
                (RegEnv.HKEY_CLASSES_ROOT, r'DesktopBackground\Shell')
        }
        self.selKind.setProperties({
            'select-menu-items': [
                {'label': key} for key in self.menuItemsRoots
            ],
            'sel-index-list': [0],
        })
        self.refreshMenuItems(self.menuItemsRoots.get(
            self.selKind.currentText(), []
        ))
        ElePyMenuPopover.setMenu(
            self.more, [
                item for name, item in self.moreOptionMenu.items()
            ], createPopover=self.createMoreMenuPopover
        )
        self.itemScrollArea.setProperty(
            'popover-show-pos', 'withMouseClickPos'
        )
        self.itemScrollArea.setProperty(
            'trigger-click-btns', 'right'
        )
        ElePyMenuPopover.setMenu(
            self.itemScrollArea, [
                item for name, item in self.moreOptionMenu.items()
            ], properties={
                'popover-trigger': 'click'
            }, createPopover=self.createMoreMenuPopover
        )

    def createListRefresh(self, mode):
        def searchEnd():
            self.refreshShowMenuItems(
                self.searchInput.text()
            )

        return {
            'showMenuItems': searchEnd
        }.get(mode, lambda: print('未知错误'))

    def _initEvent(self):
        self.searchInput.returnPressed \
            .connect(
                self.createListRefresh('showMenuItems')
            )
        self.selKind.change.connect(
            lambda menuItem, selList, allSelList: self.refreshMenuItems(self.menuItemsRoots.get(
                menuItem.label.text(), []
            ))
        )

        self.home.clicked.connect(
            lambda checked: self.refreshMenuItems(
                self.menuItemsRoots.get(self.selKind.currentText(), [])
            )
        )

        def getBackPath():
            pathSplit = self.path[1].split('\\shell')
            if len(pathSplit) == 2:
                return self.path[1]
            return '\\shell'.join(pathSplit[:-2]) + '\\shell'

        self.upPackage.clicked.connect(
            lambda checked: self.refreshMenuItems((
                self.menuItemsRoots.get(self.selKind.currentText(), [])[0], getBackPath()
            ))
        )

        self.refresh.clicked.connect(
            lambda c: self.refreshMenuItems(self.path)
        )
