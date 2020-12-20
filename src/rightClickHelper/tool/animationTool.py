#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QPropertyAnimation
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
            return animation
        return _fun
