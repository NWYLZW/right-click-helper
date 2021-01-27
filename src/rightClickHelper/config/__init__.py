#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import toml

from src.rightClickHelper.config import envs
from src.rightClickHelper.tool.pathTool import PathTool

tomlData = toml.load(fr"{PathTool.appPath()}\pyproject.toml")
tomlConfig = tomlData['tool']['poetry']

configData = {
    'appName':     tomlConfig['appName'],
    'appVersion':  tomlConfig['version'],
    'environment': envs.data['name']
}
configData['appMode'] = f'[{configData["environment"]}]'
