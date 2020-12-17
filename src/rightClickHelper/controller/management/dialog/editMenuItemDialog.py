#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

from src.rightClickHelper.tool.pathTool import PathTool
from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.tool.regTool import MenuItem
from src.rightClickHelper.view.management.dialog import editMenuItemCard

class EditMenuItemDialog(
    QDialog, editMenuItemCard.Ui_Dialog
):
    s_submit = QtCore.pyqtSignal(MenuItem, name='submit')

    def __init__(self, parent=None, menuItem: MenuItem = None):
        super(EditMenuItemDialog, self).__init__(parent)
        self._initUI()
        self._initData(menuItem)
        self._initEvent()

    def _initUI(self):
        self.setupUi(self)
        EffectTool.setBlur(self)

    def _initData(self, menuItem: MenuItem = None):
        self.menuItem = menuItem
        self.title.setText(
            '正在修改[' + menuItem.name + ']'
        )
        self.icon.setProperty('selFileTitle', '选择文件作为该菜单项的左侧小图标')

        self.icon.setProperty('fullProportion', 60)
        if menuItem.icon != '':
            self.icon.path = menuItem.icon
        else:
            self.icon.path = PathTool.appPath() + r'\src\resource\image\icon\not-found.png'
            self.icon.setToolTip('[点击修改]图标不存在')
        self.titleInput\
            .setText(menuItem.name)
        self.menuNameInput\
            .setText(menuItem.title)
        self.commandInput\
            .setText(menuItem.command)

        self.btnsStatusChange()

    def btnsStatusChange(self):
        self.shift\
            .setProperty('status', 'open' if self.menuItem.isShift else '')
        self.shift.clearFocus()
        self.style().polish(self.shift)

        self.explorer\
            .setProperty('status', 'open' if self.menuItem.isExplorer else '')
        self.explorer.clearFocus()
        self.style().polish(self.explorer)

        self.notCurWorkDir\
            .setProperty('status', 'open' if self.menuItem.isNotWorkingDir else '')
        self.notCurWorkDir.clearFocus()
        self.style().polish(self.notCurWorkDir)

    def onSubmit(self, e):
        self.menuItem.name = self.titleInput.text()
        self.menuItem.title = self.menuNameInput.text()
        self.menuItem.command = self.commandInput.text()
        self.menuItem.saveToReg()

        self.submit.emit(self.menuItem)
        self.close()

    def _initEvent(self):
        self.confirm.clicked.connect(self.onSubmit)

        def createBtnsStatusChange(index):
            def __createBtnsStatusChange(c):
                if index == 1: self.menuItem.isShift = not self.menuItem.isShift
                if index == 2: self.menuItem.isExplorer = not self.menuItem.isExplorer
                if index == 3: self.menuItem.isNotWorkingDir = not self.menuItem.isNotWorkingDir
                self.btnsStatusChange()
            return __createBtnsStatusChange
        waitConnectBtns = [
            self.shift, self.explorer, self.notCurWorkDir
        ]
        for waitConnectBtn in waitConnectBtns:
            waitConnectBtn.clicked.connect(
                createBtnsStatusChange(
                    waitConnectBtns.index(waitConnectBtn) + 1
                )
            )

        self.icon.pathChange.connect(
            lambda path: self.menuItem.__setattr__('icon', path)
        )
