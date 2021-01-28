#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import toml

from src.rightClickHelper.config import envs
from src.rightClickHelper.tool.pathTool import PathTool

tomlData = toml.load(fr"{PathTool.appPath()}\pyproject.toml")
tomlConfig = tomlData['tool']['poetry']
projectConfig = tomlData['config']['project']

configData = {
    'appName':         projectConfig['appName'],
    'appDesc':         tomlConfig['description'],
    'appMode':         'Beta' if envs.data['name'] == 'development' else '',
    'appVersion':      tomlConfig['version'],

    'homepage':        tomlConfig['homepage'],
    'repository':      tomlConfig['repository'],
    'lastPublishDate': projectConfig['lastPublishDate'],
    'environment':     envs.data['name']
}
