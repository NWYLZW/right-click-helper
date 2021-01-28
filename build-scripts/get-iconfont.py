#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json, requests

ttfUrlFormat = 'http://at.alicdn.com/t/font_{project-id}_{version}.ttf'
ttfSavePath  = '../src/resource/font'

def loadFonts(fonts: list):
    for font in fonts:
        response = requests.get(ttfUrlFormat.format(**font))
        if response.status_code == 200:
            path = f'{ttfSavePath}/{font["name"]}.ttf'
            print(f'{font["name"]}下载成功, 正在保存至文件{path}.')
            with open(path, 'wb') as f:
                f.write(response.content)
        else:
            print(f'{font["name"]}下载失败.')


if __name__ == '__main__':
    with open('.data/fonts.json', 'r') as f:
        fonts = json.load(f)
        loadFonts(fonts)
