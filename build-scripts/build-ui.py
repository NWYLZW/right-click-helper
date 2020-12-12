#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, re, time
from glob import glob
from tqdm import tqdm

config = {
    'force': False,
    'buildDataPath': '.data',
    'buildUiDataPath': '.data/build-ui-data.json'
}
toBeBuiltRcFile = [
    '../src/resource/main.qrc'
]
toBeBuiltUiFile = [
    *glob(r'../src/rightClickHelper/view/*.ui'),
    *glob(r'../src/rightClickHelper/view/management/*.ui')
]
ignoreFolders = [
]

def getBuildUiDict() -> {}:
    '''
    获取构建UI的数据字典，防止重复构建ui
    :return: 构建UI的数据字典
    '''
    buildUiDict = {
    }

    if not os.path.exists(config['buildDataPath']):
        os.mkdir(config['buildDataPath'])
    if not os.path.isfile(config['buildUiDataPath']):
        with open(config['buildUiDataPath'], 'w', encoding='utf-8') as f:
            f.write(json.dumps(buildUiDict))
    else:
        with open(config['buildUiDataPath'], 'r', encoding='utf-8') as f:
            buildUiDict = json.loads(f.read())
    return buildUiDict
buildUiDict = getBuildUiDict()

def buildUiFile(path):
    '''
    构建一个ui文件
    :param path: ui文件路径
    :return: 返回构建是否被忽略
    '''
    if path == '': raise ValueError

    uiPath = path + '.ui'
    filePreData = buildUiDict.get(uiPath, None)
    mtime = time.ctime(os.path.getmtime(uiPath))
    if filePreData \
        and filePreData == mtime \
        and not config['force']:
        return False
    else:
        buildUiDict[uiPath] = f'{mtime}'

    os.system('python -m PyQt5.uic.pyuic ' + uiPath + ' -o ' + path + '.py')

    with open(path + '.py', 'r+', encoding='utf-8') as file:
        content = file.read()
    regex = r'(?<!from\ \.[1-100]\ )import\ .*_rc'
    result = re.findall(regex, content)
    for r in result:
        content = re.sub(regex, 'from src.resource ' + r, content)
    with open(path + '.py', 'w+', encoding='utf-8') as file:
        file.write(content)

    return True

def buildUiFiles():
    '''
    构建上方设置的文件夹下所有ui文件
    '''
    ignoreCount = 0
    pBar = tqdm(total=len(toBeBuiltUiFile), ncols=150)
    for uiFilePath in toBeBuiltUiFile:
        uiFileName = uiFilePath.replace('.ui', '').replace('\\', '/')

        fileIsIgnore = False
        for ignoreFolder in ignoreFolders:
            if len(re.findall(ignoreFolder, uiFileName)) != 0:
                fileIsIgnore = True
                break
        if fileIsIgnore:
            ignoreCount += 1
            pBar.update(1)
            continue

        pBar.desc = f"正在构建 {uiFileName}.ui"
        if not buildUiFile(uiFileName):
            ignoreCount += 1
        pBar.update(1)

    print(f'{len(toBeBuiltUiFile)}个文件构建完成, {ignoreCount}个文件被忽略了')

    with open(config['buildUiDataPath'], 'w', encoding='utf-8') as f:
        f.write(json.dumps(buildUiDict))

if __name__ == '__main__':
    for rcFile in toBeBuiltRcFile:
        rcPyFileName = rcFile.replace('.qrc', '_rc.py')
        os.system(f'pyrcc5 {rcFile} -o {rcPyFileName}')
    buildUiFiles()
