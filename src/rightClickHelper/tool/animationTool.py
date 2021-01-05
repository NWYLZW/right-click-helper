#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Callable

from PyQt5.QtCore import QPropertyAnimation, QTimer
from PyQt5.QtWidgets import QWidget

class AnimationTool:
    @staticmethod
    def create(data: dict):
        def _fun(target: QWidget):
            animation = QPropertyAnimation(target, data['type'], target.parent())
            keyVals = data.get('keyVals', [])
            if len(keyVals) == 0:
                animation.setStartValue(
                    data.get('startVal')
                )
                animation.setEndValue(
                    data.get('endVal')
                )
            else:
                animation.setKeyValues(keyVals)
            animation.setDuration(data.get('duration'))
            finishedFun = data.get('finished', None)
            if finishedFun is not None: animation.finished.connect(finishedFun)
            return animation
        return _fun

    @staticmethod
    def createReverse(widget, mode: bool, callback: Callable = None):
        opacity = {'val': 1.0 if mode else 0.0}
        source = (widget.x(), widget.y())

        def reverse():
            if (mode and opacity['val'] <= 0) or (not mode and opacity['val'] >= 1.0):
                if callback is not None: callback()
                return
            widget.move(source[0], int((source[1] - 50) + opacity['val'] * 50))
            widget.setWindowOpacity(opacity['val'])
            opacity['val'] += -0.04 if mode else 0.04
            QTimer.singleShot(10, reverse)
        return reverse
