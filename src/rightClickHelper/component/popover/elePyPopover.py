#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from typing import Callable, ClassVar, Any

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPolygon, QPainterPath, QPolygonF
from PyQt5.QtWidgets import QWidget, QGridLayout

from src.rightClickHelper.component.popover.basePopover import BasePopover
from src.rightClickHelper.tool.animationTool import AnimationTool
from src.rightClickHelper.tool.widgetTool import WidgetTool

class ElePyPopover(
    BasePopover
):
    """
    properties: {
        with-triangle: {
            type     : bool,
            default  : False,
            command  : '是否带小三角指示位置',
        },
        position: {
            type     : str,
            default  : 'bottom',
            candidate: ['top', 'bottom', 'left', 'right'],
            command  : 'popover出现的位置',
        },
        animation-type: {
            type     : str,
            default  : 'transform',
            candidate: ['transform', 'fadeInOut'],
            command  : 'popover的展示动画 transform滑动移入移出，fadeInOut 淡入淡出',
        },
    }
    """

    def __init__(self, parent=None, properties: dict = {}):
        super().__init__(parent, properties)

    def invertVisible(self, widget: QWidget):
        self.hide() if self.isVisible() else self.show(widget)

    def show(self, widget: QWidget) -> None:
        super(ElePyPopover, self).show()
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
        animationType = WidgetTool.getProperty('animation-type', 'transform')(self)
        if   animationType == 'transform':
            originPoint = QPoint(
                targetPoint.x() + targetOffset[self.position]['x'][1],
                targetPoint.y() + targetOffset[self.position]['y'][1],
            )

            AnimationTool.create({
                'type': b'pos',
                'startVal': originPoint,
                'endVal':   targetPoint,
                'duration': 100
            })(self).start()
        elif animationType == 'fadeInOut':
            self.move(targetPoint)
            AnimationTool.create({
                'type': b'windowOpacity',
                'startVal': 0,
                'endVal':   1,
                'duration': 200
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
        animationType = WidgetTool.getProperty('animation-type', 'transform')(self)
        if   animationType == 'transform':
            AnimationTool.create({
                'type': b'pos',
                'startVal': self.pos(),
                'endVal': QPoint(
                    self.pos().x() + targetOffset[self.position]['x'],
                    self.pos().y() + targetOffset[self.position]['y'],
                ),
                'duration': 100,
                'finished': lambda: super(ElePyPopover, self).hide()
            })(self).start()
        elif animationType == 'fadeInOut':
            self.move(self.pos())
            AnimationTool.create({
                'type': b'windowOpacity',
                'startVal': 1,
                'endVal':   0,
                'duration': 200,
                'finished': lambda: super(ElePyPopover, self).hide()
            })(self).start()

    def paintEvent(
        self, event: QtGui.QPaintEvent
    ) -> None:
        if WidgetTool.getProperty('with-triangle', False)(self):
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
        super(ElePyPopover, self).paintEvent(event)

    @property
    def position(self):
        return WidgetTool.getProperty('position', 'bottom')(self)

    @position.setter
    def position(self, val: str):
        self.setProperty('position', val)

    @staticmethod
    def __setPopoverInHover(
        widget: QWidget, popoverWidget: QWidget, properties: dict = {}
        , PopoverClass: ClassVar['ElePyPopover'] = None
        , createPopover: Callable[
            [Any, QWidget, dict], 'ElePyPopover'
        ] = None
    ):
        widget.popover = None
        sourceEnterEvent = widget.enterEvent
        sourceLeaveEvent = widget.leaveEvent

        _is = {
            'hide': True,
            'inWidget': False
        }

        def showPopover(event):
            def __showPopover():
                if not _is['inWidget']: return
                if not _is['hide']:
                    timer = QTimer(widget)
                    timer.setSingleShot(True)
                    timer.timeout.connect(__showPopover)

                    timer.start(300)
                    return

                sourceEnterEvent(event)
                if widget.popover is None:
                    if createPopover is None:
                        widget.popover = PopoverClass(widget, properties)
                    else:
                        widget.popover = createPopover(PopoverClass, widget, properties)
                    widget.popover.setWidget(popoverWidget)
                widget.popover.show(widget)

                widget.repaint(); widget.update()
                _is['hide'] = False
            _is['inWidget'] = True
            __showPopover()

        # 当前位于popover上不隐藏
        # 当前位于widget上不隐藏
        def hidePopover(event):
            def __hidePopover(must: bool = False):
                if _is['inWidget']: return
                if must or (widget.popover is not None and widget.popover._inWidget):
                    timer = QTimer(widget)
                    timer.setSingleShot(True)
                    timer.timeout.connect(__hidePopover)

                    timer.start(300)
                    return

                sourceLeaveEvent(event)
                if widget.popover is not None:
                    widget.popover.hide()

                widget.repaint(); widget.update()
                _is['hide'] = True
            _is['inWidget'] = False
            __hidePopover(True)

        widget.enterEvent = showPopover
        widget.leaveEvent = hidePopover

    @staticmethod
    def __setPopoverInClick(
        widget: QWidget, popoverWidget: QWidget, properties: dict = {}
        , PopoverClass: ClassVar['ElePyPopover'] = None
        , createPopover: Callable[
            [Any, QWidget, dict], 'ElePyPopover'
        ] = None
    ):
        widget.popover = None
        sourceMousePressEvent = widget.mousePressEvent

        def changePopoverStatus(event: QtGui.QMouseEvent):
            sourceMousePressEvent(event)
            if event.buttons() == Qt.LeftButton:
                if widget.popover is None:
                    if createPopover is None:
                        widget.popover = PopoverClass(widget, properties)
                    else:
                        widget.popover = createPopover(PopoverClass, widget, properties)
                    widget.popover.setWidget(popoverWidget)
                widget.popover.invertVisible(widget)

                widget.repaint(); widget.update()

        widget.mousePressEvent = changePopoverStatus

    @staticmethod
    def setPopover(
        widget: QWidget, popoverWidget: QWidget, properties: dict = {}
        , PopoverClass: ClassVar['ElePyPopover'] = None
        , createPopover: Callable[
            [Any, QWidget, dict], 'ElePyPopover'
        ] = None
    ):
        if PopoverClass is None: PopoverClass = ElePyPopover

        triggerMode = properties.get('popover-trigger', 'hover')
        {
            'hover': ElePyPopover.__setPopoverInHover,
            'click': ElePyPopover.__setPopoverInClick,
        }.get(triggerMode, ElePyPopover.__setPopoverInHover)(
            widget, popoverWidget, properties
            , PopoverClass, createPopover
        )

    @staticmethod
    def setPopoverWithBackground(
        widget: QWidget, popoverWidget: QWidget, properties: dict = {}
        , dealMainWidget: Callable = None, setting: dict = {}
        , PopoverClass: ClassVar['ElePyPopover'] = None
        , createPopover: Callable[
            [Any, QWidget, dict], 'ElePyPopover'
        ] = None
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

        properties['with-triangle'] = True
        ElePyPopover.setPopover(
            widget, mainWidget, properties
            , PopoverClass, createPopover
        )
