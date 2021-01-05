#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from src.rightClickHelper.component.elePyWidget import ElePyWidget, watchProperty
from src.rightClickHelper.tool.effectTool import EffectTool
from src.rightClickHelper.tool.widgetTool import WidgetTool

class ElePyDialog(
    QDialog, ElePyWidget
):
    def __init__(self, parent=None, properties: dict = None):
        if properties is None: properties = {}
        super().__init__(parent, {
            'shadowRadius': 10
            , 'shadowColor': Qt.gray
            , **properties
        })

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
