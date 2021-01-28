#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys, os

from src.rightClickHelper.config.envs import data as envsData

class PathTool:
    @staticmethod
    def appPath(isTest: bool = False):
        """
        Returns the application run path.
        :param isTest: 是否为测试环境
        :return: 返回运行目录
        """
        if hasattr(sys, 'frozen'):
            path = os.path.dirname(sys.executable)
        else:
            path = os.getcwd()
        if isTest or envsData['name'] == 'test':
            path = os.path.join(path, '../../')
        return path

    @staticmethod
    def tempPath():
        """Returns the application temp path."""
        if hasattr(sys, 'frozen'):
            return sys._MEIPASS
        return os.getcwd()
