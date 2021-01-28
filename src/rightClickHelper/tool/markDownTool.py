#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
from enum import Enum

import markdown

from src.rightClickHelper.tool.pathTool import PathTool

class MarkDownTool:
    class Theme(Enum):
        TYPO = os.path.join(
            PathTool.appPath(), 'src/resource/css/markdown/typo.css'
        )

    @classmethod
    def getThemeStyle(cls, theme: Theme):
        with open(theme.value, 'r') as f:
            return f'<style type="text/css">{f.read()}</style>\n'

    @classmethod
    def generate(cls, md: str, theme: Theme = Theme.TYPO):
        template = f'''\
<html>
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type" />
        {cls.getThemeStyle(theme)}
    </head>
    <body style=" font-family: 'SimSun'; font-size:9pt; font-weight:400; font-style:normal;">
        {markdown.markdown(md, extras=['code-friendly', 'fenced-code-blocks', 'footnotes','tables','code-color','pyshell','nofollow','cuddled-lists','header ids','nofollow'])}
    </body>
</html>'''
        return template
