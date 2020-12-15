#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys,os

class PathTool:
    @staticmethod
    def appPath():
        """Returns the application run path."""
        if hasattr(sys, 'frozen'):
            return os.path.dirname(sys.executable)
        return os.getcwd()

    @staticmethod
    def tempPath():
        """Returns the application temp path."""
        if hasattr(sys, 'frozen'):
            return sys._MEIPASS
        return os.getcwd()
