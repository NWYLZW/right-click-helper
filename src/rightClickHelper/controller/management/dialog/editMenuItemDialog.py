#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

        self.shift\
            .setProperty('status', 'open' if menuItem.isShift else '')
        self.explorer\
            .setProperty('status', 'open' if menuItem.isExplorer else '')
        self.notCurWorkDir\
            .setProperty('status', 'open' if menuItem.isNotWorkingDir else '')

    def _initEvent(self):
        pass
