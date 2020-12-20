#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.rightClickHelper.component.popover.popover import Popover

class MenuPopover(
    Popover
):
    def __init__(self, parent=None, properties: dict = {}):
        super(Popover).__init__(parent, properties)
