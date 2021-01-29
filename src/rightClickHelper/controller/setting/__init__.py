#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import re

from PyQt5.QtCore import QTimer

from src.rightClickHelper.component.elePyWidget import ElePyWidget
from src.rightClickHelper.component.form.elePyButton import ElePyButton
from src.rightClickHelper.component.notice.elePyMessage import ElePyMessage, ElePyMessageType
from src.rightClickHelper.component.notice.elePyMessageBox import ElePyMessageBox, AlertAction
from src.rightClickHelper.config import configData
from src.rightClickHelper.tool.markDownTool import MarkDownTool
from src.rightClickHelper.tool.pathTool import PathTool
from src.rightClickHelper.tool.requestTool import RequestTool
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

        setting = configData['userData'].get('setting', {})
        self.isAutoCheck.setChecked(
            setting.get('isAutoCheck', False)
        )
        self.isAutoCheckBeta.setChecked(
            setting.get('isAutoCheckBeta', False)
        )

    def _initEvent(self):
        self.checkoutUpdateBtn.clicked.connect(
            Setting.checkUpdate
        )

        def openLogDir():
            logFilePath = os.path.join(
                PathTool.appPath(), 'log'
            )
            if not os.path.exists(logFilePath):
                os.mkdir(logFilePath)
            os.startfile(logFilePath)
        self.openLogFileBtn.clicked.connect(openLogDir)

        def setUserData(name):
            def fun(c):
                if configData['userData'].get('setting') is None:
                    configData['userData']['setting'] = {}
                configData['userData']['setting'][name] = c
                configData['saveUserData']()
            return fun
        self.isAutoCheck.clicked.connect((setUserData('isAutoCheck')))
        self.isAutoCheckBeta.clicked.connect((setUserData('isAutoCheckBeta')))

    @staticmethod
    def getUpdate(alertAction: AlertAction):
        newChangeLogUrl = configData['repository'] + '/releases/download/1.0.3.0/Right.Click.Helper.zip'
        savePath = os.path.join(
            os.path.expanduser('~'), 'Downloads/Right.Click.Helper.zip'
        )

        mbox = ElePyMessageBox()

        def dealFun(
            data: bytes, contentSize: int, curDownloadSize: int
            , isEnd: bool
        ):
            schedule = curDownloadSize/contentSize
            downloadSize = curDownloadSize/1024/1024
            mbox.contentText.setText(f'{schedule:.2%}({downloadSize:.2f}Mb)')
            if isEnd:
                mbox.close()
                ElePyMessage.instance().show({
                    'type': ElePyMessageType.SUCCESS,
                    'message': '下载成功。'
                })
                os.startfile(os.path.dirname(savePath))

        try:
            t = RequestTool.downloadFileToPath(
                newChangeLogUrl, savePath, dealFun, 50*1024
            )

            mbox.alert(
                '0.00%(0.00Mb)', '下载资源中...'
                , '&#xe6b3;'
                , confirmBtnText='取消下载'
                , callback=lambda alertAction: t.destroyed()
            )
        except Exception as e:
            ElePyMessage.instance().show({
                'type': ElePyMessageType.ERROR,
                'message': '网络似乎有点差。'
            })

    @staticmethod
    def getTheNewChangeLog(callBack):
        newChangeLogUrl = configData['raw-repository'] + '/master/CHANGELOG.zh-CN.md'
        try:
            def wrapper(content, **kwargs):
                callBack(content.decode('utf-8'))
            RequestTool.downloadFile(
                newChangeLogUrl, wrapper
            )
        except Exception as e:
            ElePyMessage.instance().show({
                'type': ElePyMessageType.ERROR,
                'message': '获取更新失败。'
            })

    @classmethod
    def checkUpdate(cls):
        with open(os.path.join(
            PathTool.appPath(), 'CHANGELOG.zh-CN.md'
        ), encoding='utf-8') as f:
            changeLogMDStr = f.read()
        eleMsgBox = ElePyMessageBox()
        eleMsgBox.confirm(
            MarkDownTool.generate(changeLogMDStr), '变更'
            , confirmBtnText='更新'
            , confirmCallback=cls.getUpdate
            , cancelBtnText='取消更新'
            , contentWidth=400, contentHeight=300
        )
        eleMsgBox.confirmBtn.setProperty('disabled', True)

        def dealContent(content: str):
            lastVersion = content.split('\n')[2]
            theLastVersion = re.match(
                r'## \[(.*)\] - .*', lastVersion
            )
            a0, b0, c0, d0 = theLastVersion.group(1).split('.')
            a1, b1, c1, d1 = configData['appVersion'].split('.')
            serverVersion = int(a0)*1000 + int(b0)*100 + int(c0)*10 + int(d0)
            localVersion = int(a1)*1000 + int(b1)*100 + int(c1)*10 + int(d1)
            if serverVersion > localVersion:
                eleMsgBox.confirmBtn.setProperty('disabled', False)
            return eleMsgBox.contentText.setHtml(
                MarkDownTool.generate(
                    content
                )
            )

        QTimer.singleShot(
            1000
            , lambda: cls.getTheNewChangeLog(dealContent)
        )
