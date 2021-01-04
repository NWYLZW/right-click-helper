#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from typing import Callable, ClassVar, Any

from PyQt5.QtCore import QPoint, Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPolygon, QPainterPath, QPolygonF, QPaintEvent, QMouseEvent
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

    def invertVisible(self, widget: QWidget, event: QMouseEvent = None):
        self.hide() if self.isVisible() else self.show(widget, event)

    def show(self, widget: QWidget = None, event: QMouseEvent = None) -> None:
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
        if WidgetTool.getProperty(
            'popover-show-pos', ''
        )(widget) != 'withMouseClickPos':
            targetPoint = QPoint(
                pos.x() + targetOffset[self.position]['x'][0],
                pos.y() + targetOffset[self.position]['y'][0]
            )
        else:
            targetPoint = QPoint(
                pos.x() + event.x() - self.width()/2, pos.y() + event.y()
            )
        animationType = WidgetTool.getProperty(
            'animation-type', 'transform'
        )(self)
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
        animationType = WidgetTool.getProperty(
            'animation-type', 'transform'
        )(self)
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
        self, event: QPaintEvent
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
        , createdPopover: Callable[['ElePyPopover'], Any] = None
    ):
        """
        挂载一个被鼠标移动在某个widget上方展示的popover
        :param widget:          被挂载的widget实例
        :param popoverWidget:   放在popoverDockWindow中的widget实例
        :param properties:      传递给popover构造函数的properties字典
        :param PopoverClass:    popover的构造函数
        :param createPopover:   创建popover的函数，必须返回一个popover实例 具体参数调用，查看上方范型
        :param createdPopover:  创建完popover触发该回调钩子，传入创建好的popover对象
        :return: 无返回值
        """
        widget.popover = None
        sourceEnterEvent = widget.enterEvent
        sourceLeaveEvent = widget.leaveEvent

        _is = {
            'hide': True,
            'inWidget': False
        }

        def showPopover(event):
            def __showPopover(must: bool = False):
                if not _is['inWidget']: return
                if must or not _is['hide']:
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
                    if createdPopover is not None:
                        createdPopover(widget.popover)
                widget.popover.show(widget)

                widget.repaint(); widget.update()
                _is['hide'] = False
            _is['inWidget'] = True
            __showPopover(True)

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
        , createdPopover: Callable[['ElePyPopover'], Any] = None
    ):
        """
        挂载一个被鼠标点击在某个widget上方展示的popover
        :param widget:          被挂载的widget实例
        :param popoverWidget:   放在popoverDockWindow中的widget实例
        :param properties:      传递给popover构造函数的properties字典
        :param PopoverClass:    popover的构造函数
        :param createPopover:   创建popover的函数，必须返回一个popover实例 具体参数调用，查看上方范型
        :param createdPopover:  创建完popover触发该回调钩子，传入创建好的popover对象
        :return: 无返回值
        """
        widget.popover = None
        sourceMousePressEvent = widget.mousePressEvent

        def changePopoverStatus(event: QMouseEvent):
            sourceMousePressEvent(event)
            btns = {
                'left': [Qt.LeftButton],
                'right': [Qt.RightButton],
            }
            triggerClickBtns = btns.get(WidgetTool.getProperty(
                'trigger-click-btns', 'left'
            )(widget), btns['left'])
            trigger = False
            for triggerClickBtn in triggerClickBtns:
                if event.buttons() == triggerClickBtn:
                    trigger = True
            if trigger:
                if widget.popover is None:
                    if createPopover is None:
                        widget.popover = PopoverClass(widget, properties)
                    else:
                        widget.popover = createPopover(PopoverClass, widget, properties)
                    widget.popover.setWidget(popoverWidget)
                    if createdPopover is not None:
                        createdPopover(widget.popover)
                widget.popover.invertVisible(
                    widget, event
                )
            else:
                if widget.popover is not None and widget.popover.isVisible():
                    widget.popover.hide()

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

        def createdPopover(popover: 'ElePyPopover'):
            pass
        {
            'hover': ElePyPopover.__setPopoverInHover,
            'click': ElePyPopover.__setPopoverInClick,
        }.get(properties.get('popover-trigger', 'hover'), ElePyPopover.__setPopoverInHover)(
            widget=widget, popoverWidget=popoverWidget, properties=properties
            , PopoverClass=PopoverClass
            , createPopover=createPopover
            , createdPopover=createdPopover
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
        popoverWidget.setParent(mainWidget)
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
