#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from abc import abstractmethod
from typing import ClassVar

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QWidget, QApplication

from src.rightClickHelper.component.popover.elePyMenuPopover import ElePyMenuPopover, PopoverMenuItem, MenuPopoverMode
from src.rightClickHelper.component.popover.elePyTooltip import ElePyTooltip
from src.rightClickHelper.controller.management.dialog.editMenuItemDialog import EditMenuItemDialog
from src.rightClickHelper.tool.pathTool import PathTool
from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.tool.regTool import MenuItem, RegTool, RegEnv
from src.rightClickHelper.tool.systemTool import SystemTool

from src.rightClickHelper.view.management import menuItemCard, menuItemCard_new, menuItemCard_package

class MenuItemCard_itf:
    cardRemove = QtCore.pyqtSignal(MenuItem)
    moreMenuSel = QtCore.pyqtSignal(str, MenuItem)
    moreOptionMenu = {
        'copy': {
            'label': '复制',
            'icon': PathTool.appPath() + r'\src\resource\image\common-icon\copy-ed.png'
        },
        'cut': {
            'label': '剪切',
            'icon': PathTool.appPath() + r'\src\resource\image\common-icon\cut-ed.png'
        },
        'share': {
            'label': '分享',
            'icon': PathTool.appPath() + r'\src\resource\image\common-icon\share-ed.png'
        },
        'save': {
            'label': '保存',
            'icon': PathTool.appPath() + r'\src\resource\image\common-icon\save-ed.png'
        }
    }

    def _initUI(self):
        try:
            self.setupUi(self)
            EffectTool.setBlur(self)

            self.maskCard.hide()
        except Exception as e: raise e

    def createChangeStatus(self):
        def changeStatus(event):
            result = QMessageBox.question(
                self, '提示', '是否' + ('打开' if self.menuItem.isHide else '关闭') + '该右键菜单',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
            if result == QMessageBox.Yes:
                self.menuItem.isHide = not self.menuItem.isHide
                self.menuItem.saveToReg()
                self.setData(self.menuItem)
        return changeStatus

    def doCardRemove(self):
        path = self.menuItem.regData['__path__']
        RegTool.delKey(
            RegEnv.find(path[0]), path[1]
        )

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

            def cardRemove(c):
                result = QMessageBox.question(
                    self, '提示', '是否删除该右键菜单',
                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                    QMessageBox.Cancel
                )
                if result == QMessageBox.Yes:
                    self.doCardRemove()
                    self.cardRemove.emit(self.menuItem)
            self.remove.clicked.connect(cardRemove)
        except Exception as e: raise e

    @abstractmethod
    def setIcon(self, menuItem: MenuItem):
        pass

    def customSetData(self, menuItem: MenuItem):
        pass

    def setTitle(self, menuItem: MenuItem):
        try:
            self.title.setText(menuItem.name)
            ElePyTooltip.setTooltip(
                self.title, menuItem.name
            )
        except Exception as e: raise e

    def createMenuPopover(
        self
        , PopoverClass: ClassVar[ElePyMenuPopover], widget: QWidget, properties: dict
    ):
        popover = PopoverClass(widget, properties)  # type: ElePyMenuPopover

        def __itemClick(popoverMenuItem):
            if popoverMenuItem.property('label') == self.moreOptionMenu['copy']['label']:
                self.moreMenuSel.emit('copy', self.menuItem)
            elif popoverMenuItem.property('label') == self.moreOptionMenu['cut']['label']:
                self.moreMenuSel.emit('cut', self.menuItem)
            elif popoverMenuItem.property('label') == self.moreOptionMenu['share']['label']:
                QApplication.clipboard().setText(
                    json.dumps(
                        RegTool.recursion(
                            RegEnv.find(self.menuItem.regData['__path__'][0]), self.menuItem.regData['__path__'][1]
                        )
                    )
                )
        popover.itemClicked.connect(__itemClick)
        return popover

    def setData(self, menuItem: MenuItem):
        self.menuItem = menuItem
        self.setIcon(menuItem)
        self.setTitle(menuItem)
        ElePyMenuPopover.setMenu(
            self.more, [
                val for item, val in self.moreOptionMenu.items()
            ], createPopover=self.createMenuPopover
        )
        self.customSetData(menuItem)
        self.repaint()

    @staticmethod
    def setSwitchItem(menuItemCard, menuItem: MenuItem):
        menuItemCard.switchItem.setProperty('status', 'close' if menuItem.isHide else 'open')
        ElePyTooltip.setTooltip(
            menuItemCard.switchItem, '显示该选项' if menuItem.isHide else '隐藏该选项'
        )
        menuItemCard.style().polish(menuItemCard.switchItem)

class MenuItemCard(
    QtWidgets.QWidget,
    menuItemCard.Ui_item,
    MenuItemCard_itf
):
    def __init__(self, parent=None):
        super(MenuItemCard, self).__init__(parent)
        self._initUI()
        self._initSelfUI()
        self._initEvent()
        self._initSelfEvent()

    def _initSelfUI(self):
        pass

    def _initSelfEvent(self):
        def createEditDialog(checked):
            dialog = EditMenuItemDialog(None, self.menuItem)
            dialog.submit.connect(
                lambda menuItem: self.setData(menuItem)
            )
            dialog.exec()

        self.edit.clicked.connect(createEditDialog)

    def setIcon(self, menuItem: MenuItem):
        if menuItem.icon != '':
            self.icon.setPixmap(
                SystemTool.getIcon(menuItem.icon)
            )
            self.status.setText('')
        else:
            rect = self.icon.geometry()
            self.icon.setPixmap(
                QPixmap(PathTool.appPath() + r'\src\resource\image\icon\not-found.png')
                    .scaled(rect.width(), rect.height())
            )
            rect = self.status.geometry()
            self.status.setPixmap(
                QPixmap(PathTool.appPath() + r'\src\resource\image\exclamation-mark.png')
                    .scaled(rect.width(), rect.height())
            )
            self.status.setToolTip('图标不存在')
        self.icon.repaint()

    def customSetData(self, menuItem: MenuItem):
        MenuItemCard_itf.setSwitchItem(self, menuItem)

class MenuItemCard_Package(
    QtWidgets.QWidget,
    menuItemCard_package.Ui_item,
    MenuItemCard_itf
):
    s_clickTitle = QtCore.pyqtSignal(MenuItem, name='clickTitle')

    def __init__(self, parent=None):
        super(MenuItemCard_Package, self).__init__(parent)
        self._initUI()
        self._initSelfUI()
        self._initEvent()
        self._initSelfEvent()

    def _initSelfUI(self):
        self.title.setCursor(
            QtCore.Qt.PointingHandCursor
        )

    def _initSelfEvent(self):
        def createEditDialog(checked):
            dialog = EditMenuItemDialog(None, self.menuItem)
            dialog.submit.connect(
                lambda menuItem: self.setData(menuItem)
            )
            dialog.exec()
        self.edit.clicked.connect(createEditDialog)
        self.title.mousePressEvent = lambda e: \
            self.clickTitle.emit(self.menuItem) if e.buttons() == QtCore.Qt.LeftButton else None

    def setIcon(self, menuItem: MenuItem):
        if menuItem.icon != '':
            self.showIcon.setPixmap(
                SystemTool.getIcon(menuItem.icon)
            )
        else:
            rect = self.showIcon.geometry()
            self.showIcon.setPixmap(
                QPixmap(PathTool.appPath() + r'\src\resource\image\icon\package.png')
                    .scaled(rect.width(), rect.height())
            )
        self.showIcon.repaint()

        ions = [
            self.icon_1, self.icon_2, self.icon_3, self.icon_4
        ]
        children = menuItem.children
        for index in range(0, 4 if len(children) > 4 else len(children)):
            child = children[index]
            if child.icon == '': continue

            ions[index].setPixmap(SystemTool.getIcon(child.icon))
            ions[index].repaint()

    def customSetData(self, menuItem: MenuItem):
        MenuItemCard_itf.setSwitchItem(self, menuItem)

class MenuItemCard_New(
    QtWidgets.QWidget,
    menuItemCard_new.Ui_item
):
    s_createMenuItemSuccess = QtCore.pyqtSignal(name='createMenuItemSuccess')

    def __init__(self, parent=None):
        super(MenuItemCard_New, self).__init__(parent)
        self._initUI()
        self._initEvent()

    def _initUI(self):
        self.setupUi(self)
        EffectTool.setBlur(self)
        ElePyTooltip.setTooltip(
            self.addBtn, '新建菜单项'
        )

    def _initEvent(self):
        def createEditDialog(checked):
            dialog = EditMenuItemDialog(None, self.menuItem, {
                'ableChangePackageStatus': True
            })
            dialog.submit.connect(
                lambda menuItem: self.createMenuItemSuccess.emit()
            )
            dialog.exec()
        self.addBtn.clicked\
            .connect(createEditDialog)

    def setData(self, menuItem: MenuItem):
        self.menuItem = menuItem
