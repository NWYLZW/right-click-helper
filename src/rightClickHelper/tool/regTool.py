#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, winreg
from enum import Enum
from src.rightClickHelper.tool.systemTool import SystemTool

class CommandFlag(Enum):
    NONE = 0X00000000
    HIDE = 0X00000008

class RegEnv(Enum):
    # https://docs.microsoft.com/en-us/troubleshoot/windows-server/performance/windows-registry-advanced-users
    HKEY_CLASSES_ROOT    = winreg.HKEY_CLASSES_ROOT     # Contains the root of the configuration information for the user who is currently logged on.
                                                        # The user's folders, screen colors, and Control Panel settings are stored here.
                                                        # This information is associated with the user's profile.
                                                        # This key is sometimes abbreviated as HKCU.
    HKEY_CURRENT_USER    = winreg.HKEY_CURRENT_USER     # Contains all the actively loaded user profiles on the computer.
                                                        # HKEY_CURRENT_USER is a subkey of HKEY_USERS.
                                                        # HKEY_USERS is sometimes abbreviated as HKU.
    HKEY_LOCAL_MACHINE   = winreg.HKEY_LOCAL_MACHINE    # Contains configuration information particular to the computer (for any user).
                                                        # This key is sometimes abbreviated as HKLM.
    HKEY_USERS           = winreg.HKEY_USERS            # Is a subkey of HKEY_LOCAL_MACHINE\Software.
                                                        # The information that is stored here makes sure that the correct program opens when you open a file by using Windows Explorer.
                                                        # This key is sometimes abbreviated as HKCR.
                                                        # Starting with Windows 2000, this information is stored under both the HKEY_LOCAL_MACHINE and HKEY_CURRENT_USER keys.
                                                        # The HKEY_LOCAL_MACHINE\Software\Classes key contains default settings that can apply to all users on the local computer.
                                                        # The HKEY_CURRENT_USER\Software\Classes key contains settings that override the default settings and apply only to the interactive user.
                                                        # The HKEY_CLASSES_ROOT key provides a view of the registry that merges the information from these two sources.
                                                        # HKEY_CLASSES_ROOT also provides this merged view for programs that are designed for earlier versions of Windows.
                                                        # To change the settings for the interactive user, changes must be made under HKEY_CURRENT_USER\Software\Classes instead of under HKEY_CLASSES_ROOT.
                                                        # To change the default settings, changes must be made under HKEY_LOCAL_MACHINE\Software\Classes.
                                                        # If you write keys to a key under HKEY_CLASSES_ROOT, the system stores the information under HKEY_LOCAL_MACHINE\Software\Classes.
                                                        # If you write values to a key under HKEY_CLASSES_ROOT, and the key already exists under HKEY_CURRENT_USER\Software\Classes,
                                                        # the system will store the information there instead of under HKEY_LOCAL_MACHINE\Software\Classes.
    HKEY_CURRENT_CONFIG  = winreg.HKEY_CURRENT_CONFIG   # Contains information about the hardware profile that is used by the local computer at system startup.

    @staticmethod
    def find(val):
        for item in RegEnv:
            if item.value == val:
                return item
        raise ValueError('RegEnv not found.')

class RegType(Enum):
    # https://docs.microsoft.com/en-us/windows/win32/sysinfo/registry-value-types
    REG_BINARY              = winreg.REG_BINARY                 # 任何形式的二进制数据.
    REG_DWORD               = winreg.REG_DWORD                  # 一个32位数字.
    REG_DWORD_LITTLE_ENDIAN = winreg.REG_DWORD_LITTLE_ENDIAN    # 小尾数格式的32位数字.Windows被设计为在小端计算机体系结构上运行.因此,此值在Windows头文件中定义为REG_DWORD.
    REG_DWORD_BIG_ENDIAN    = winreg.REG_DWORD_BIG_ENDIAN       # big-endian格式的32位数字.一些UNIX系统支持big-endian体系结构.
    REG_EXPAND_SZ           = winreg.REG_EXPAND_SZ              # 以空值结尾的字符串,其中包含对环境变量（例如,"％PATH％"）的未扩展引用.
                                                                # 根据您使用的是Unicode还是ANSI函数,它将是Unicode或ANSI字符串.要扩展环境变量引用,请使用ExpandEnvironmentStrings函数.
    REG_LINK                = winreg.REG_LINK                   # 一个以空值结尾的Unicode字符串,其中包含符号链接的目标路径,
                                                                # 该符号链接是通过使用REG_OPTION_CREATE_LINK调用RegCreateKeyEx函数创建的.
    REG_MULTI_SZ            = winreg.REG_MULTI_SZ               # 由空字符串(\0)终止的以null终止的字符串序列.
    REG_NONE                = winreg.REG_NONE                   # 没有定义的值类型.
    REG_QWORD               = winreg.REG_QWORD                  # 一个64位数字.
    REG_QWORD_LITTLE_ENDIAN = winreg.REG_QWORD_LITTLE_ENDIAN    # 小尾数格式的64位数字.
                                                                # Windows被设计为在小端计算机体系结构上运行.因此,此值在Windows头文件中定义为REG_QWORD.
    REG_SZ                  = winreg.REG_SZ                     # 空终止的字符串.根据您使用的是Unicode还是ANSI函数,这将是Unicode或ANSI字符串.

    @staticmethod
    def find(val):
        for item in RegType:
            if item.value == val:
                return item
        raise ValueError('RegType not found.')

class RegVal:
    def __init__(self, _type, val):
        self.type = None
        for regType in RegType:
            if regType.value == _type:
                self.type = regType
        if self.type is None:
            self.type = RegType.REG_NONE
        self.val = val

class RegTool:
    @staticmethod
    def pathExist(
        env: RegEnv, path: str
    ) -> bool:
        try:
            winreg.CloseKey(
                winreg.OpenKey(env.value, path)
            )
            return True
        except: return False

    @staticmethod
    def keyExist(
        env: RegEnv, path: str, key: str
    ) -> bool:
        return RegTool.pathExist(env, path + '\\' + key)

    @staticmethod
    def createPath(
        env: RegEnv, path: str
    ):
        if path == '': raise ValueError('Path cannot be empty.')
        if RegTool.pathExist(env, path):
            return winreg.OpenKey(env.value, path)

        return winreg.CreateKey(env.value, path)

    @staticmethod
    def createKey(
        env: RegEnv, path: str, key: str
    ):
        if path == '' or key == '':
            raise ValueError('Path cannot be empty.')
        if RegTool.keyExist(env, path, key):
            return winreg.OpenKey(env.value, path + '\\' + key)

        return RegTool.createPath(env, path + '\\' + key)

    @staticmethod
    def delKey(
        env: RegEnv, path: str, key: str = ''
    ):
        if path == '' or not RegTool.pathExist(env, path):
            raise ValueError('Path not found.')
        if key != '' and not RegTool.keyExist(env, path, key):
            raise ValueError('Key not found.')

        def reduceDel(path):
            subKeys = RegTool.listKey(env, path)
            for subKey in subKeys:
                reduceDel(path + '\\' + subKey)
            winreg.DeleteKey(env.value, path)
        reduceDel(path)

    @staticmethod
    def listKey(
        env: RegEnv, path: str
    ) -> list:
        with winreg.OpenKey(env.value, path) as regKey:
            regCount = winreg.QueryInfoKey(regKey)[0]
            regKeys = []
            for i in range(int(regCount)):
                name = winreg.EnumKey(regKey, i)
                regKeys.append(name)
        return regKeys

    @staticmethod
    def recursion(
        env: RegEnv, startPath: str, depth: int = 1000
    ) -> {}:
        if depth == 0: return {}
        if startPath == '' or not RegTool.pathExist(env, startPath):
            raise ValueError('Path not found.')

        originData = {}
        originList = RegTool.listKey(env, startPath)

        for item in originList:
            originData[item] = RegTool.recursion(env, startPath + '\\' + item, depth - 1)

        originData['__path__'] = (env.value, startPath)
        originData['__val__'] = RegTool.listVal(env, startPath)
        return originData

    @staticmethod
    def writeKeyByStr(regDataStr: str):
        return RegTool.writeKey(
            json.loads(regDataStr)
        )

    @staticmethod
    def writeKey(regData: dict):
        if regData == {}: return

        regEnvVal, path = regData['__path__']
        regEnv = RegEnv.find(regEnvVal)
        if not RegTool.pathExist(regEnv, path):
            RegTool.createPath(regEnv, path)

        for key, regDataChild in regData.items():
            if key[:2] != '__':
                RegTool.writeKey(regDataChild)
        for valueName, (valueContent, valueTypeVal) in regData['__val__'].items():
            RegTool.setVal(
                regEnv, path, valueName, valueContent
                , RegType.find(valueTypeVal)
            )

    @staticmethod
    def listVal(
        env: RegEnv, path: str
    ) -> dict:
        with winreg.OpenKey(env.value, path) as regKey:
            i = 0
            regVals = {}
            try:
                while True:
                    name, val, type = winreg.EnumValue(regKey, i)
                    regVals[name] = (val, type)
                    i += 1
            finally:
                return regVals

    @staticmethod
    def setVal(
        env: RegEnv, path: str,
        valueName: str, valueContent, regType: RegType = RegType.REG_SZ
    ):
        if not SystemTool.isAdmin():
            raise PermissionError('Not started with administrator rights.')

        with winreg.OpenKey(
            env.value, path, access=winreg.KEY_SET_VALUE
        ) as regKey:
            winreg.SetValueEx(regKey, valueName, 0, regType.value, valueContent)

    @staticmethod
    def delVal(
        env: RegEnv, path: str, valueName: str
    ):
        if not SystemTool.isAdmin():
            raise PermissionError('Not started with administrator rights.')

        try:
            with winreg.OpenKey(
                env.value, path, access=winreg.KEY_SET_VALUE
            ) as regKey:
                winreg.DeleteValue(regKey, valueName)
        except: pass

    @staticmethod
    def getVal(
        env: RegEnv, path: str, valueName: str
    ) -> RegVal:
        if not SystemTool.isAdmin():
            raise PermissionError('Not started with administrator rights.')

        with winreg.OpenKey(
            env.value, path, access=winreg.KEY_QUERY_VALUE
        ) as regKey:
            try:
                val, _type = winreg.QueryValueEx(regKey, valueName)
                return RegVal(_type, val)
            except:
                raise FileNotFoundError('Reg val not found.')

    @staticmethod
    def mvKey(
        source: (RegEnv, str),
        target: (RegEnv, str)
    ):
        def replacePath(regData: {}):
            regData['__path__'] = (
                target[0].value,
                regData['__path__'][1].replace(source[1], target[1])
            )
            for key, regDataChild in regData.items():
                if key[:2] != '__':
                    replacePath(regDataChild)
        try:
            sourceRegData = RegTool.recursion(*source)
            replacePath(sourceRegData)
            RegTool.writeKey(sourceRegData)
        except Exception as e: raise e
        RegTool.delKey(*source)

CURRENT_USER_USER_SHELL_FOLDERS = (
    RegEnv.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'
)
systemDir = {
    'pictures': RegTool.getVal(
        *CURRENT_USER_USER_SHELL_FOLDERS, valueName='My Pictures'
    ).val,
    'desktop': RegTool.getVal(
        *CURRENT_USER_USER_SHELL_FOLDERS, valueName='Desktop'
    ).val,
    'documents': RegTool.getVal(
        *CURRENT_USER_USER_SHELL_FOLDERS, valueName='Personal'
    ).val
}

class MenuItem:
    def __init__(self, name: str, regData: dict):
        self.regData = regData
        self._name   = name
        self.__name  = ''

        regDataVal = regData.get('__val__', {})
        commandVal = regData.get('command', {
            '__val__': {}
        }).get('__val__', {})

        self.title      = regDataVal.get('', [''])[0]
        if self.title == '':
            self.title = regDataVal.get('MUIVerb', [''])[0]
        # type: str
        self.icon       = regDataVal.get('Icon', [''])[0]
        # type: str
        self.command    = commandVal.get('', [''])[0]
        # type: str

        self.isPackage  = regDataVal.get('SubCommands', [False])[0] == ''
        # type: bool
        # 二级菜单
        self.isHide     = regDataVal.get('CommandFlags', [CommandFlag.NONE.value])[0] == CommandFlag.HIDE.value
        # type: bool
        # 隐藏
        self.isShift    = regDataVal.get('Extended', [False])[0] == ''
        # type: bool
        # 按下shift时
        self.isExplorer = regDataVal.get('OnlyInBrowserWindow', [False])[0] == ''
        # type: bool
        # 文件浏览器中
        self.isNotWorkingDir = regDataVal.get('NoWorkingDirectory', [False])[0] == ''
        # type: bool
        # 不以当前目录为打开的工作目录

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self.__name = newName

    def saveToReg(self, mv: bool = True):
        if self.regData.get('__val__', {}) == {}:
            self.regData['__val__'] = {}
        valRegData = self.regData['__val__']
        valRegData[''] = (self.title, RegType.REG_SZ.value)
        valRegData['MUIVerb'] = (self.title, RegType.REG_SZ.value)
        valRegData['Icon'] = (self.icon, RegType.REG_SZ.value)
        self.regData['__path__'] = (
            self.regData['__path__'][0], '\\'.join([
                *self.regData['__path__'][1].split('\\')[:-1],
                self.name
            ])
        )
        path = self.regData['__path__']

        def bool2Create(
            boolValue,
            valName, valContent, valType: RegType = RegType.REG_SZ,
            valPath: (RegEnv, str) = (RegEnv.find(path[0]), path[1])
        ):
            if boolValue:
                RegTool.setVal(
                    valPath[0], valPath[1]
                    , valName, valContent, valType
                )
            else:
                RegTool.delVal(
                    valPath[0], valPath[1]
                    , valName
                )

        if not self.isPackage:
            if self.regData.get('command', {}) == {}:
                self.regData['command'] = {
                    '__path__': (path[0], path[1] + r'\command'),
                    '__val__': {}
                }
            commandValRegData = self.regData['command']['__val__']
            commandValRegData[''] = (self.command.replace('/', '\\'), RegType.REG_SZ.value)
        else:
            if self.regData.get('shell', {}) == {}:
                self.regData['shell'] = {
                    '__path__': (path[0], path[1] + r'\shell'),
                    '__val__': {}
                }

        for child in self.children:
            child.saveToReg(False)
        RegTool.writeKey(
            self.regData
        )

        if not self.isPackage:
            bool2Create(self.isNotWorkingDir, 'NoWorkingDirectory', '')
        bool2Create(self.isHide,     'CommandFlags',        CommandFlag.HIDE.value, RegType.REG_DWORD)
        bool2Create(self.isPackage,  'SubCommands',         '')
        bool2Create(self.isShift,    'Extended',            '')
        bool2Create(self.isExplorer, 'OnlyInBrowserWindow', '')

        regEnv = RegEnv.find(
            self.regData['__path__'][0]
        )
        if mv:
            sourcePath = (regEnv, self.regData['__path__'][1])
            targetPath = (
                regEnv, '\\'.join([
                    *self.regData['__path__'][1].split('\\')[:-1],
                    self.__name
                ])
            )
            if sourcePath != targetPath:
                RegTool.mvKey(sourcePath, targetPath)
            self._name = self.__name

    @property
    def children(self) -> []:
        if not self.isPackage:
            return []

        returnChildren = []
        envVal, path = self.regData.get('__path__')

        if not RegTool.keyExist(
            RegEnv.find(envVal), path, 'shell'
        ): return []
        regDataTree = RegTool.recursion(
            RegEnv.find(envVal), path + '\\shell', 3
        )
        for key, val in regDataTree.items():
            if key[:2] != '__':
                returnChildren.append(
                    MenuItem(key, regDataTree[key])
                )
        return returnChildren

    def __str__(self):
        return json.dumps(self.regData, sort_keys=False, indent=2, separators=(',', ':'))
