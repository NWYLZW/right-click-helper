#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os, toml
import shutil

from src.rightClickHelper.config import env
from src.rightClickHelper.tool.pathTool import PathTool

tomlPath = fr'{PathTool.appPath()}\pyproject.toml'
dataPath = fr'{PathTool.appPath()}\.data'
userDataPath = fr'{PathTool.appPath()}\.data\user.json'

if not os.path.exists(dataPath):
    os.mkdir(dataPath)
if not os.path.exists(userDataPath):
    shutil.copy(os.path.join(
        PathTool.appPath(), 'src/resource/template/user.json'
    ), dataPath + r'\user.json')

tomlData = toml.load(tomlPath)
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
    'environment':     env.data['name'],
}

with open(userDataPath, 'r') as f:
    content = f.read()
    if content == '': content = '{}'
    configData['userData'] = json.loads(content)
configData['saveUserData'] = lambda: json.dump(
    configData['userData'], open(userDataPath, 'w')
    , indent=2
)
