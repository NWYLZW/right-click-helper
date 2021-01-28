#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from src.rightClickHelper.component.elePyWidget import ElePyWidget
from src.rightClickHelper.component.form.elePyButton import ElePyButton
from src.rightClickHelper.view.setting.index import Ui_setting as SettingUi

class Setting(
    ElePyWidget, SettingUi
):
    languages = [{
        'label': '简体中文'
    }]
    logLevels = [{
        'label': '关'
    }, {
        'label': '调试'
    }, {
        'label': '普通'
    }]

    def __init__(
        self, parent=None, properties=None
    ):
        if properties is None:
            properties = {}
        super().__init__(parent, properties)

    def _initUi(self):
        super(Setting, self)._initUi()
        self.setupUi(self)
        self.checkoutUpdateBtn.setProperties({
            'icon': '&#xe72f;',
            'el-size': ElePyButton.Size.SMALL.value
        })
        self.openLogFileBtn.setProperties({
            'icon': '&#xe6c9;',
            'el-size': ElePyButton.Size.SMALL.value
        })

    def _initData(self):
        self.selLang.setProperties({
            'select-menu-items': Setting.languages,
            'sel-index-list': [0],
        })
        self.selLogLevel.setProperties({
            'select-menu-items': Setting.logLevels,
            'sel-index-list': [2],
        })
