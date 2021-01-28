#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import shutil
from contextlib import closing
from os import PathLike
from typing import Callable, Any, Optional, TextIO, Union

import requests
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QObject, QTimer


class RequestTool:
    class DownLoadThread(QThread):
        destroy = pyqtSignal()
        getData = pyqtSignal(bytes, int, int, bool)

        def __init__(
            self, url: str
            , parent=None
            , chunkSize: int = 1024
            , fileOption: list[Union[str, bytes, PathLike[str], PathLike[bytes], int]] = None
        ):
            super(RequestTool.DownLoadThread, self).__init__(parent)
            self.isStop    = False              # type: bool
            self.url       = url                # type: str
            self.chunkSize = chunkSize          # type: int
            if fileOption is not None:
                self.file = open(*fileOption)  # type: TextIO
            else:
                self.file = None  # type: TextIO
            self.req = None
            self.session = requests.session()

            self._mutex = QMutex()

        def destroyed(self, object: Optional[QObject] = ...) -> None:
            self._mutex.lock()
            if self.file: self.file.close()
            if self.req:  self.req.close()
            self.session.close()
            self._mutex.unlock()

        def chunkDownload(self):
            curDownloadSize = 0

            self._mutex.lock()
            self.req = requests.get(self.url, stream=True)
            self._mutex.unlock()

            with closing(self.req) as response:
                contentSize = int(response.headers['content-length'])
                allStr = b''
                for data in response.iter_content(chunk_size=self.chunkSize):
                    self._mutex.lock()
                    if self.isStop: return None
                    curDownloadSize += self.chunkSize
                    allStr += data
                    self.getData.emit(data, contentSize, curDownloadSize, False)
                    self._mutex.unlock()

                self._mutex.lock()
                self.getData.emit(data, contentSize, curDownloadSize, True)
                self._mutex.unlock()

        def bindFile(self, *args):
            self._mutex.lock()
            self._mutex.unlock()

        def run(self) -> None:
            if self.chunkSize == -1:
                response = requests.get(self.url)
                if response.status_code == 200:
                    self.getData.emit(
                        response.content, response.headers['content-length'], response.headers['content-length']
                        , True
                    )
            else:
                self.chunkDownload()

    downLoadThreads = []    # type: list[DownLoadThread]

    @classmethod
    def downloadFile(
        cls, url: str
        , dealData: Callable[[bytes, int, int, bool], Any]
        , chunkSize: int = -1
        , fileOption: list[Union[str, bytes, PathLike[str], PathLike[bytes], int]] = None
    ) -> 'DownLoadThread':
        t = RequestTool.DownLoadThread(
            url, chunkSize=chunkSize, fileOption=fileOption
        )
        t.getData.connect(dealData)
        t.start()
        cls.downLoadThreads.append(t)
        t.destroy.connect(lambda: cls.downLoadThreads.remove(t))
        return t

    @classmethod
    def downloadFileToPath(
        cls, url: str, savePath: str
        , dealData: Callable[[bytes, int, int, bool], Any]
        , chunkSize: int = -1
    ) -> 'DownLoadThread':
        tempPath = savePath + '.temp'
        index = len(cls.downLoadThreads)

        def fun(
            data: bytes, contentSize: int, curDownloadSize: int
            , isEnd: bool
        ):
            t = cls.downLoadThreads[index]
            if dealData is not None: dealData(data, contentSize, curDownloadSize, isEnd)
            if isEnd:
                t.destroyed()
                if curDownloadSize < contentSize:
                    raise FileNotFoundError('File download is not complete.')
                else:
                    shutil.move(tempPath, savePath)
            else:
                t.file.write(data)

        t = cls.downloadFile(
            url, fun, chunkSize
            , fileOption=[savePath + '.temp', 'wb']
        )
        return t
