#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog

from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.view.management.dialog import editMenuItemCard

class EditMenuItemDialog(
    QDialog, editMenuItemCard.Ui_Dialog
):
    def __init__(self, parent=None):
        super(EditMenuItemDialog, self).__init__(parent)
        self._initUI()
        self._initData()
        self._initEvent()

    def _initUI(self):
        self.setupUi(self)
        EffectTool.setBlur(self)

    def _initData(self):
        pass

    def _initEvent(self):
        pass
