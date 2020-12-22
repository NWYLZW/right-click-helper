#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from src.rightClickHelper.tool.pathTool import PathTool
from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.tool.regTool import MenuItem, systemDir
from src.rightClickHelper.tool.systemTool import SystemTool
from src.rightClickHelper.view.management.dialog import editMenuItemCard

class EditMenuItemDialog(
    QDialog, editMenuItemCard.Ui_Dialog
):
    s_submit = QtCore.pyqtSignal(MenuItem, name='submit')

    def __init__(self, parent=None, menuItem: MenuItem = None, properties: dict = {}):
        super(EditMenuItemDialog, self).__init__(parent)
        for _propertyName, _property in properties.items():
            self.setProperty(_propertyName, _property)
        self._initUI()
        self._initData(menuItem)
        self._initEvent()

    def _initUI(self):
        self.setupUi(self)
        EffectTool.setBlur(self)

    def _initData(self, menuItem: MenuItem = None):
        self.menuItem = menuItem
        self.title.setPlaceholder(
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
            .setPlaceholder(menuItem.name)
        self.menuNameInput\
            .setPlaceholder(menuItem.title)
        self.commandInput\
            .setPlaceholder(menuItem.command)

        self.btnsStatusChange()

        if self.menuItem.isPackage:
            self.packbag.setToolTip('该菜单项为二级菜单')
            self.packbag.setProperty('status', 'open')
            self.style().polish(self.packbag)
            self.packbag.clearFocus()

            self.commandInput.setReadOnly(True)
            self.commandInput\
                .setCursor(Qt.ForbiddenCursor)
            self.selExeBtn\
                .setCursor(Qt.ForbiddenCursor)
        else:
            self.packbag.setToolTip('该菜单项不为二级菜单')
            self.packbag.setProperty('status', '')
            self.style().polish(self.packbag)
            self.packbag.clearFocus()

            self.commandInput.setReadOnly(False)
            self.commandInput\
                .setCursor(Qt.IBeamCursor)
            self.selExeBtn\
                .setCursor(Qt.PointingHandCursor)

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
        if self.icon.path != PathTool.appPath() + r'\src\resource\image\icon\not-found.png':
            self.menuItem.icon = self.icon.path
        else:
            self.menuItem.icon = ''
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

        if not self.menuItem.isPackage:
            self.icon.pathChange.connect(
                lambda path: self.menuItem.__setattr__('icon', path)
            )

            def changeCommand():
                if not self.menuItem.isPackage:
                    filePath = SystemTool.getFilePathByQFileDialog(
                        self, self.property('selFileTitle'), 'C:',
                        'Application (*.exe)'
                    ).replace('/', '\\')
                    if filePath != '':
                        self.icon.path = filePath
                        self.commandInput.setPlaceholder('"' + filePath + '" "%1"')
            self.selExeBtn.clicked\
                .connect(changeCommand)

        if self.property('ableChangePackageStatus'):
            def changePackageStatus(c):
                self.menuItem.isPackage = not self.menuItem.isPackage
                self._initData(self.menuItem)
            self.packbag.clicked.connect(changePackageStatus)
        else:
            self.packbag.setCursor(
                Qt.ForbiddenCursor
            )
