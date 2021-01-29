#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, toml, shutil, zipfile

from tqdm import tqdm

def main():
    if os.path.exists('./dist/'):
        shutil.rmtree('./dist/')
    os.system(
        'pyinstaller ./start.spec'
    )
    config = toml.load('./pyproject.toml')['tool']['poetry']

    newZipFilePath = f"./releases/{config['name']}-{config['version']}.zip"
    latestZipFilePath = f"./releases/{config['name']}-latest.zip"
    if not os.path.exists('./releases'):
        os.mkdir('./releases')
    z = zipfile.ZipFile(newZipFilePath, 'w', zipfile.ZIP_DEFLATED)

    waitZipFiles = os.walk('./dist/Right Click Helper')
    pBar = tqdm(total=sum(1 for _ in waitZipFiles), ncols=150)
    for dirPath, dirNames, filenames in os.walk('./dist/Right Click Helper'):
        path = dirPath.replace('./dist/Right Click Helper', '')
        path = path and path + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirPath, filename), path + filename)
            pBar.desc = f'compressing: {filename}'
            pBar.update(0)
        pBar.update(1)
    z.close()
    print('compressed.')
    shutil.copy(newZipFilePath, latestZipFilePath)


if __name__ == '__main__':
    main()
