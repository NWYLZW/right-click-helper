#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from PyQt5.QtGui import QPixmap

from src.rightClickHelper.component.elePyWidget import ElePyWidget
from src.rightClickHelper.view.about.index import Ui_about as AboutUi

class About(
    ElePyWidget, AboutUi
):
    def __init__(
        self, parent=None, properties=None
    ):
        if properties is None:
            properties = {}
        super().__init__(parent, properties)

    def _initUi(self):
        self.setupUi(self)
        self.icon.setPixmap(
            QPixmap(self.__class__.getResourcePath(
                r'image\icon\right-click-helper.ico'
            ))
        )
        self.builtWithQtImg.setPixmap(
            QPixmap(self.__class__.getResourcePath(
                r'image\built-with-Qt-logos\built-with-Qt_Horizontal_Small.png'
            ))
        )
