#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import abstractmethod

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

from src.rightClickHelper.controller.management.dialog.editMenuItemDialog import EditMenuItemDialog
from src.rightClickHelper.tool.pathTool import PathTool
from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.tool.regTool import MenuItem, RegTool, RegEnv
from src.rightClickHelper.tool.systemTool import SystemTool

from src.rightClickHelper.view.management import menuItemCard, menuItemCard_new, menuItemCard_package

class MenuItemCard_itf:
    s_cardRemove = QtCore.pyqtSignal(MenuItem, name='cardRemove')
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

    def doCardRemove(self): pass

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
            self.title.setToolTip(menuItem.name)
        except Exception as e: raise e

    def setData(self, menuItem: MenuItem):
        self.menuItem = menuItem
        self.setIcon(menuItem)
        self.setTitle(menuItem)
        self.customSetData(menuItem)
        self.repaint()

    @staticmethod
    def setSwitchItem(menuItemCard, menuItem: MenuItem):
        menuItemCard.switchItem.setProperty('status', 'close' if menuItem.isHide else 'open')
        menuItemCard.switchItem.setToolTip(
            '隐藏该选项' if menuItem.isHide else '显示该选项'
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

    def doCardRemove(self):
        path = self.menuItem.regData['__path__']
        RegTool.delKey(
            RegEnv.find(path[0]), path[1]
        )

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
