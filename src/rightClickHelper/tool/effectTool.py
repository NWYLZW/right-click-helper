#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

class EffectTool:
    @staticmethod
    def setBlur(widget, blurRadius: int = 12):
        # 去除默认边框
        widget.setWindowFlags(Qt.FramelessWindowHint)
        # 背景透明（就是ui中黑色背景的那个控件）
        widget.setAttribute(Qt.WA_TranslucentBackground, True)

        # 添加阴影
        effect = QGraphicsDropShadowEffect(widget)
        effect.setBlurRadius(blurRadius)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        widget.setGraphicsEffect(effect)
