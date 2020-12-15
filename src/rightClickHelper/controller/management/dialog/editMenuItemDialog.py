#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

from src.rightClickHelper.tool.pathTool import PathTool
from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.tool.regTool import MenuItem
from src.rightClickHelper.tool.systemTool import SystemTool
from src.rightClickHelper.view.management.dialog import editMenuItemCard

class EditMenuItemDialog(
    QDialog, editMenuItemCard.Ui_Dialog
):
    s_submit = QtCore.pyqtSignal(MenuItem, name='submit')

    def __init__(self, parent=None, data: MenuItem = None):
        super(EditMenuItemDialog, self).__init__(parent)
        self._initUI()
        self._initData(data)
        self._initEvent()

    def _initUI(self):
        self.setupUi(self)
        EffectTool.setBlur(self, 20)

    def _initData(self, menuItem: MenuItem = None):
        self.menuItem = menuItem
        self.title.setText(
            '正在修改[' + menuItem.title + ']'
        )
        if menuItem.icon != '':
            self.icon.setPixmap(
                SystemTool.getIcon(menuItem.icon)
            )
        else:
            rect = self.icon.geometry()
            self.icon.setPixmap(
                QPixmap(PathTool.appPath() + r'\src\resource\image\icon\not-found.png')
                    .scaled(rect.width(), rect.height())
            )
            self.icon.setToolTip('图标不存在')
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
