#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QWidget

from src.rightClickHelper.component.popover.basePopover import BasePopover
from src.rightClickHelper.tool.animationTool import AnimationTool
from src.rightClickHelper.tool.widgetTool import WidgetTool

class Popover(
    BasePopover
):
    def __init__(self, parent=None, properties: dict = {}):
        super().__init__(parent, properties)

    @staticmethod
    def __setPopoverInHover(widget: QWidget, popoverWidget: QWidget, properties: dict = {}):
        widget.popover: Popover = None
        sourceEnterEvent = widget.enterEvent
        sourceLeaveEvent = widget.leaveEvent

        def showPopover(event):
            sourceEnterEvent(event)
            if widget.popover is None:
                widget.popover = Popover(widget, properties)
            widget.popover.setWidget(popoverWidget)
            widget.popover.show(widget)

            widget.repaint(); widget.update()

        def hidePopover(event):
            sourceLeaveEvent(event)
            if widget.popover is not None:
                widget.popover.hide()

            widget.repaint(); widget.update()

        widget.enterEvent = showPopover
        widget.leaveEvent = hidePopover

    @staticmethod
    def setPopover(widget: QWidget, popoverWidget: QWidget, properties: dict = {}):
        triggerMode = WidgetTool.getProperty('popover-trigger-mode', 'hover')(widget)
        {
            'hover': Popover.__setPopoverInHover
        }.get(triggerMode, Popover.__setPopoverInHover)(widget, popoverWidget, properties)

    def show(self, widget: QWidget) -> None:
        super().show()
        pos = widget.mapToGlobal(QPoint(0, 0))
        targetOffset = {
            'bottom': {
                'x': [int((widget.width() - self.width()) / 2), 0],
                'y': [widget.height(), 100],
            },
            'top': {
                'x': [int((widget.width() - self.width()) / 2), 0],
                'y': [-self.height(), -100],
            },
            'left': {
                'x': [-self.width(), -100],
                'y': [int((widget.height() - self.height())/2), 0],
            },
            'right': {
                'x': [widget.width(), 100],
                'y': [int((widget.height() - self.height())/2), 0],
            },
        }
        targetPoint = QPoint(
            pos.x() + targetOffset[self.position]['x'][0],
            pos.y() + targetOffset[self.position]['y'][0]
        )
        originPoint = QPoint(
            targetPoint.x() + targetOffset[self.position]['x'][1],
            targetPoint.y() + targetOffset[self.position]['y'][1],
        )

        AnimationTool.create({
            'type': b'pos',
            'startVal': originPoint,
            'endVal': targetPoint,
            'duration': 100
        })(self).start()

    def hide(self) -> None:
        targetOffset = {
            'bottom': {
                'x': 0, 'y': 100,
            },
            'top': {
                'x': 0, 'y': -100,
            },
            'left': {
                'x': -100, 'y': 0,
            },
            'right': {
                'x': 100, 'y': 0,
            },
        }
        animation = AnimationTool.create({
            'type': b'pos',
            'startVal': self.pos(),
            'endVal': QPoint(
                self.pos().x() + targetOffset[self.position]['x'],
                self.pos().y() + targetOffset[self.position]['y'],
            ),
            'duration': 100
        })(self)
        animation.start()
        animation.finished.connect(
            lambda: super(Popover, self).hide()
        )

    @property
    def position(self):
        return WidgetTool.getProperty('position', 'bottom')(self)

    @position.setter
    def position(self, val: str):
        self.setProperty('position', val)
