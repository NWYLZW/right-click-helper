#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QLineF, pyqtSignal
from PyQt5.QtGui import QPaintEvent, QPainter, QColor
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget

from src.rightClickHelper.component.elePyWidget import ElePyWidget, watchProperty, LifeStage
from src.rightClickHelper.component.popover.elePyMenuPopover import ElePyMenuPopover, MenuPopoverMode, PopoverMenuItem
from src.rightClickHelper.tool.widgetTool import WidgetTool

class ElePySelect(
    ElePyWidget
):
    """
    signal: {
        change: {
            param: (PopoverMenuItem, [int], [PopoverMenuItem]),
            command : '所选项改变时触发，参数分别为(选择的菜单项，菜单已选index列表，所有菜单项列表)',
        }
    },
    properties: {
        placeholder: {
            type    : str,
            default : '请选择',
            command : '未选择事默认展示的文字',
        },
        disabled: {
            type    : bool,
            default : false,
            command : '控制是否为禁用状态',
        },
        select-type: {
            type     : str,
            default  : '请选择',
            candidate: ['single', 'multiple'],
            command  : '选择类型',
        },
        select-menu-items: {
            type     : [PopoverMenuItem],
            default  : [],
            command  : '待选菜单选项',
        },
        sel-index-list: {
            type     : [int],
            default  : [],
            command  : '默认选择的菜单项列表, 当select-type属性为single时只会选择第一个',
        },
    }
    """
    change = pyqtSignal(PopoverMenuItem, list, list)

    def __init__(
        self, parent=None, properties: dict = {}
    ):
        self._menuPopover = None
        self.__transformProperties = {
            'animation-type': 'fadeInOut'
        }
        super().__init__(parent, {
            'disabled': False,
            **properties
        })

    def drawRightIcon(self, event: QPaintEvent):
        painter = QPainter(self.rightIcon)

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(QColor(202, 208, 212))

        unit = 6; offset0 = (2, 2); offset1 = (3, 3)

        painter.drawLines([
            QLineF(0    + offset0[0], 0    + offset0[1], unit   + offset0[0], unit + offset0[1]),
            QLineF(unit + offset1[0], unit + offset1[1], 2*unit + offset1[0], 0    + offset1[1])
        ])

    def _initUi(self):
        self.setLayout(QHBoxLayout())
        content = QWidget(self)
        content.setObjectName('ElePySelect-content')
        self.layout().addWidget(content)
        content.setStyleSheet('''\
        #ElePySelect-content {
            border: 1px solid rgb(220, 223, 230);
            border-radius: 5px;
            background-color: rgb(255, 255, 255);
        }
        #ElePySelect-content:hover {
            border: 1px solid rgb(192, 196, 204);
        }''')
        content.setLayout(QHBoxLayout())
        content.layout().setContentsMargins(5, 5, 5, 5)

        self.label = QLabel(content)
        WidgetTool.setFont(self.label)
        content.layout().addWidget(self.label)

        self.rightIcon = QWidget(content)
        content.layout().addWidget(self.rightIcon)
        self.rightIcon.setFixedSize(16, 12)
        self.rightIcon.paintEvent = self.drawRightIcon

        self.popoverContent = content
        ElePyMenuPopover.setMenu(
            self.popoverContent, [], mode=WidgetTool.getProperty(
                'select-mode', MenuPopoverMode.LIGHT
            )(self), createPopover=self.setMenuPopover
        )

    def updateLabel(self):
        placeholder = WidgetTool.getProperty(
            'placeholder', '请选择'
        )(self)        # type: str
        menuItems   = WidgetTool.getProperty(
            'select-menu-items', []
        )(self)  # type: list[PopoverMenuItem]

        selItems = []   # type: list[PopoverMenuItem]
        for index in self.selIndexList:
            if index < 0 or index >= len(menuItems): continue
            selItems.append(menuItems[index])

        dim = False
        if len(self.selIndexList) == 0 or len(selItems) == 0:
            self.label.setText(placeholder)
        else:
            self.label.setText(', '.join([selItem.title for selItem in selItems]))

        dim = dim or WidgetTool.getProperty('disabled', False)(self)
        self.label.setStyleSheet(f'''\
        QLabel {{
            color: {'rgb(192, 196, 204)' if dim else 'rgb(0, 0, 0)'};
        }}''')

        if self.maximumWidth() == 16777215:
            selfWidth = WidgetTool.getTextWidth(self.label) + self.rightIcon.width() + 40
        else:
            selfWidth = self.maximumWidth()
        if selfWidth < self.minimumWidth():
            selfWidth = self.minimumWidth()

        self.setFixedWidth(selfWidth)
        self.popoverContent.setFixedWidth(selfWidth - self.rightIcon.width())

        self.parent().repaint(); self.parent().update()

    @watchProperty({
        'select-menu-items': {'type': list}
    })
    def selectMenuItemsChange(self, newVal, oldVal, propertyName):
        self.__transformProperties['menu-popover-items'] = newVal

    @watchProperty({
        'disabled': {'type': bool}
    })
    def disableChange(self, newVal, oldVal, propertyName):
        if newVal:
            self.setCursor(Qt.ForbiddenCursor)
        else:
            self.setCursor(Qt.PointingHandCursor)

        if self._menuPopover is None:
            self.__transformProperties['forbiddenShow'] = newVal
        else:
            self._menuPopover.setProperty('forbiddenShow', newVal)

    @watchProperty({
        'sel-index-list': {'type': list}
    })
    def selIndexListChange(self, newVal, oldVal, propertyName):
        self.selIndexList = newVal
        if self._lifeStage in [
            LifeStage.INIT_DATA_BEFORE,
            LifeStage.INITED,
        ]: self.updateLabel()

    def currentText(self):
        return self.label.text()

    def menuPopover(self):
        return self._menuPopover

    def indexOfMenuItem(
        self, menuItem: PopoverMenuItem
    ) -> int:
        menuItems   = WidgetTool.getProperty(
            'select-menu-items', []
        )(self)  # type: [PopoverMenuItem]
        for index in range(len(menuItems)):
            if menuItem is menuItems[index]: return index
        return -1

    def isSel(
        self, menuItem: PopoverMenuItem
    ) -> bool:
        if self.indexOfMenuItem(menuItem) in self.selIndexList:
            return True
        return False

    def setMenuPopover(self, PopoverClass: ElePyMenuPopover, widget: QWidget, properties: dict):
        properties = {
            **properties,
            **self.__transformProperties
        }
        self._menuPopover = PopoverClass(widget, properties)    # type: ElePySelect

        def itemClicked(menuItem, menuItemWidget):
            selectType = WidgetTool.getProperty('select-type', 'single')(self)
            index = self.indexOfMenuItem(menuItem)
            if index != -1:
                if not self.isSel(menuItem):
                    if selectType == 'single':
                        self.selIndexList = []
                    self.selIndexList.append(index)
                    self.change.emit(menuItem, self.selIndexList, WidgetTool.getProperty(
                        'select-menu-items', []
                    )(self))
                else:
                    if selectType == 'multiple':
                        self.selIndexList.remove(index)

            self.updateLabel()

        self._menuPopover.itemClicked.connect(itemClicked)
        self._menuPopover.hided.connect(lambda: self.setFocus())

        return self._menuPopover
