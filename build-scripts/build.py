#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, shutil

if __name__ == '__main__':
    shutil.rmtree('./dist/')
    os.system(
        'pyinstaller ./start.spec'
    )
