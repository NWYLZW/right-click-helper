#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import toml

from src.rightClickHelper.config import env
from src.rightClickHelper.tool.pathTool import PathTool

tomlData = toml.load(fr"{PathTool.appPath()}\pyproject.toml")
tomlConfig = tomlData['tool']['poetry']
projectConfig = tomlData['config']['project']

configData = {
    'appName':         projectConfig['appName'],
    'appDesc':         tomlConfig['description'],
    'appMode':         'Beta' if env.data['name'] == 'development' else '',
    'appVersion':      tomlConfig['version'],

    'homepage':        tomlConfig['homepage'],
    'repository':      tomlConfig['repository'],
    'raw-repository':  tomlConfig['repository'].replace('github.com', 'raw.githubusercontent.com'),
    'lastPublishDate': projectConfig['lastPublishDate'],
    'environment':     env.data['name']
}
