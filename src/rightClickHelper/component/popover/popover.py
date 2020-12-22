#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from typing import Callable, ClassVar

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QColor, QPolygon, QPainterPath, QPolygonF
from PyQt5.QtWidgets import QWidget, QGridLayout

from src.rightClickHelper.component.popover.basePopover import BasePopover
from src.rightClickHelper.tool.animationTool import AnimationTool
from src.rightClickHelper.tool.widgetTool import WidgetTool

class Popover(
    BasePopover
):
    def __init__(self, parent=None, properties: dict = {}):
        super().__init__(parent, properties)

    @staticmethod
    def __setPopoverInHover(
        widget: QWidget, popoverWidget: QWidget, properties: dict = {}
        , PopoverClass: ClassVar = None
    ):
        widget.popover: Popover = None
        sourceEnterEvent = widget.enterEvent
        sourceLeaveEvent = widget.leaveEvent

        def showPopover(event):
            sourceEnterEvent(event)
            if widget.popover is None:
                widget.popover = PopoverClass(widget, properties)
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
    def __setPopoverInClick(
        widget: QWidget, popoverWidget: QWidget, properties: dict = {}
        , PopoverClass: ClassVar = None
    ):
        widget.popover: Popover = None
        sourceMousePressEvent = widget.mousePressEvent

        data = {'count': 0}
        def changePopoverStatus(event: QtGui.QMouseEvent):
            sourceMousePressEvent(event)
            if event.buttons() == Qt.LeftButton:
                if data['count'] % 2 == 0:
                    if widget.popover is None:
                        widget.popover = PopoverClass(widget, properties)
                        widget.popover.setWidget(popoverWidget)
                    widget.popover.show(widget)
                else:
                    if widget.popover is not None:
                        widget.popover.hide()

                data['count'] += 1
                widget.repaint(); widget.update()

        widget.mousePressEvent = changePopoverStatus

    @staticmethod
    def setPopover(
        widget: QWidget, popoverWidget: QWidget, properties: dict = {}
        , PopoverClass: ClassVar = None
    ):
        if PopoverClass is None: PopoverClass = Popover

        triggerMode = properties.get('popover-trigger', 'hover')
        {
            'hover': Popover.__setPopoverInHover,
            'click': Popover.__setPopoverInClick,
        }.get(triggerMode, Popover.__setPopoverInHover)(widget, popoverWidget, properties, PopoverClass)

    @staticmethod
    def setPopoverWithBackground(
        widget: QWidget, popoverWidget: QWidget, properties: dict = {}
        , dealMainWidget: Callable = None, setting: dict = {}
        , PopoverClass: ClassVar = None
    ):
        GL = QGridLayout()
        mainWidget = QWidget()
        mainWidget.setLayout(GL)
        mainWidget.setFixedSize(
            popoverWidget.size().width()  + properties.get('shadowRadius', 10) * 2 + 10,
            popoverWidget.size().height() + properties.get('shadowRadius', 10) * 2
        )
        mainWidget.popoverContent = popoverWidget
        GL.addWidget(popoverWidget)

        if dealMainWidget is not None:
            dealMainWidget(mainWidget)
        else:
            mainWidget.setObjectName('mainWidget-' + str(random.randint(0, 1000000)))
            mainWidget.settingBackgroundColor = setting.get('background-color', [255, 255, 255, 255])
            mainWidget.setStyleSheet(f'''\
                #{mainWidget.objectName()} {{
                    margin: 10px;
                    border-radius: 4px;
                    background-color: rgba({','.join(
                        [str(color) for color in mainWidget.settingBackgroundColor]
                    )});
                }}''')

        properties['withTriangle'] = True
        Popover.setPopover(widget, mainWidget, properties, PopoverClass)

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

    def paintEvent(
        self, event: QtGui.QPaintEvent
    ) -> None:
        if WidgetTool.getProperty('withTriangle', False)(self):
            painter = QPainter(self)

            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(*self.widget().settingBackgroundColor[:3]))

            triangle = QPolygon()
            side = 12
            offset = {
                'top': [
                    int(self.width()/2) - int(side/2),
                    self.height() - 2*self.shadowRadius
                ],
                'bottom': [
                    int(self.width()/2) - int(side/2),
                    2*self.shadowRadius - side
                ],
                'left': [
                    self.width() - 2*self.shadowRadius,
                    int(self.height()/2) - int(side/2)
                ],
                'right': [
                    2*self.shadowRadius - side,
                    int(self.height()/2) - int(side/2)
                ]
            }[self.position]
            pos = {
                'top':      (int(side/2) + offset[0], 0           + offset[1]),
                'bottom':   (int(side/2) + offset[0], side        + offset[1]),
                'left':     (0           + offset[0], int(side/2) + offset[1]),
                'right':    (side        + offset[0], int(side/2) + offset[1]),
            }
            triangles = {
                'top': [*pos['bottom'], *pos['left'], *pos['right']],
                'bottom': [*pos['top'], *pos['left'], *pos['right']],
                'left': [*pos['top'], *pos['right'], *pos['bottom']],
                'right': [*pos['top'], *pos['left'], *pos['bottom']],
            }
            triangle.setPoints(triangles[self.position])
            painter.drawPolygon(triangle)
            painterPath = QPainterPath()
            painterPath.addPolygon(QPolygonF(triangle))
            painter.fillPath(painterPath, painter.brush())
        super(Popover, self).paintEvent(event)

    @property
    def position(self):
        return WidgetTool.getProperty('position', 'bottom')(self)

    @position.setter
    def position(self, val: str):
        self.setProperty('position', val)
