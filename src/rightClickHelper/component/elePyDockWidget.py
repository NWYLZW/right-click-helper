#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDockWidget, QWidget

from src.rightClickHelper.component.elePyWidget import ElePyWidget, watchProperty
from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.tool.widgetTool import WidgetTool

class ElePyDockWidget(
    QDockWidget, ElePyWidget
):
    def __init__(self, parent=None, properties: dict = None):
        if properties is None: properties = {}
        super().__init__(parent, {
            'shadowRadius': 10
            , 'shadowColor': Qt.gray
            , **properties
        })

    def _initUi(self):
        temp = QWidget(); self.setTitleBarWidget(temp); del temp
        self.setFloating(True)

    def repaint(self) -> None:
        super(ElePyDockWidget, self).repaint()

        # 修复WA_TranslucentBackground导致的子控件界面不刷新bug
        def repaint():
            try:
                for child in self.children():       # type: QWidget
                    if isinstance(child, QWidget):
                        child.update()
            except: pass
        QTimer.singleShot(10, repaint)

    @watchProperty({
        'shadowColor': {'type': int},
        'shadowRadius': {'type': int},
    })
    def shadowChange(self, newVal, oldVal, name):
        EffectTool.setBlur(
            self
            , shadowRadius=WidgetTool.getProperty('shadowRadius', 10)(self)
            , shadowColor=WidgetTool.getProperty('shadowColor', Qt.gray)(self)
        )
