#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .lifeStage import LifeStage, initLink

class AbsWidget:
    @staticmethod
    def initLinks(self):
        initLink(self, [
            LifeStage.INIT_UI_BEFORE,
            LifeStage.INIT_UI,
            LifeStage.INIT_UI_AFTER,
        ])
        initLink(self, [
            LifeStage.INIT_DATA_BEFORE,
            LifeStage.INIT_DATA,
            LifeStage.INIT_DATA_AFTER,
        ])
        initLink(self, [
            LifeStage.INIT_EVENT_BEFORE,
            LifeStage.INIT_EVENT,
            LifeStage.INIT_EVENT_AFTER,
        ])
        self._lifeStage = LifeStage.INITED

    def _initUiBefore(self): pass
    def _initUi(self): pass
    def _initUiAfter(self): pass

    def _initDataBefore(self): pass
    def _initData(self): pass
    def _initDataAfter(self): pass

    def _initEventBefore(self): pass
    def _initEvent(self): pass
    def _initEventAfter(self): pass
