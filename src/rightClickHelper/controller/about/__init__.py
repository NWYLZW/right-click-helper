#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap, QDesktopServices

from src.rightClickHelper.component.elePyWidget import ElePyWidget
from src.rightClickHelper.component.form.elePyButton import ElePyButton
from src.rightClickHelper.component.notice.elePyMessageBox import ElePyMessageBox
from src.rightClickHelper.component.popover.elePyTooltip import ElePyTooltip
from src.rightClickHelper.config import configData
from src.rightClickHelper.tool.markDownTool import MarkDownTool
from src.rightClickHelper.tool.pathTool import PathTool
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
        self.github.setProperties({
            'icon': '&#xe600;',
            'el-size': ElePyButton.Size.SMALL.value
        })
        ElePyTooltip.setTooltip(
            self.github, '你的❤star就是我的动力'
        )
        self.openResourceLicenseBtn.setProperties({
            'icon': '&#xe7d7;',
            'el-size': ElePyButton.Size.SMALL.value
        })

        self.thankIcon.setText('&#xe74c;')

    def _initData(self):
        self.appName.setText(
            configData['appName']
        )
        self.description.setText(
            configData['appDesc']
        )
        self.version.setText(
            configData['appVersion'] + '-' + configData['appMode']
        )
        self.publishDatetime.setText(
            f"({configData['lastPublishDate']})"
        )

        self.thankList.setHtml(MarkDownTool.generate(
            '### UI\n'
            '* 项目的大多数图标 [iconfont](https://www.iconfont.cn/)'
        ))

    def _initEvent(self):
        self.github.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(configData['repository']))
        )
        with open(os.path.join(
            PathTool.appPath(), 'external-dependencies-LICENSE.md'
        ), encoding='utf-8') as f:
            externalDependenciesLICENSE = f.read()
        self.openResourceLicenseBtn.clicked.connect(
            lambda: ElePyMessageBox().alert(
                MarkDownTool.generate(externalDependenciesLICENSE), '开源许可'
                , confirmBtnText='我知道了'
                , contentWidth=600, contentHeight=400
            )
        )
        self.thankList.setOpenLinks(False)
        self.thankList.anchorClicked.connect(
            lambda url: QDesktopServices.openUrl(url)
        )
