#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys,os

class pathTool:
    @classmethod
    def appPath(cls):
        """Returns the application run path."""
        if hasattr(sys, 'frozen'):
            return os.path.dirname(sys.executable)
        return os.getcwd()
    @classmethod
    def tempPath(cls):
        """Returns the application temp path."""
        if hasattr(sys, 'frozen'):
            return sys._MEIPASS
        return os.getcwd()
