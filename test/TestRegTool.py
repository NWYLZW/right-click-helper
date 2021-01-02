#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, unittest

from src.rightClickHelper.tool.regTool import RegTool, RegEnv, RegType

class TestRegTool(unittest.TestCase):
    def test_setVal(self):
        testVal = {
            'name': 'test',
            'content': 'test2'
        }
        RegTool.setVal(
            RegEnv.HKEY_CLASSES_ROOT, r'\Directory\shell\AnyCode',
            testVal['name'], testVal['content'], RegType.REG_SZ
        )
        addRegVal = RegTool.getVal(
            RegEnv.HKEY_CLASSES_ROOT, r'\Directory\shell\AnyCode', testVal['name']
        )
        self.assertEqual(
            addRegVal.type, RegType.REG_SZ
            , 'Value type setting error'
        )
        self.assertEqual(
            addRegVal.val, testVal['content']
            , 'Value content setting error'
        )
        RegTool.delVal(
            RegEnv.HKEY_CLASSES_ROOT, r'\Directory\shell\AnyCode', testVal['name']
        )
        try:
            RegTool.getVal(
                RegEnv.HKEY_CLASSES_ROOT, r'\Directory\shell\AnyCode', testVal['name']
            )
        except Exception as regValNotFoundError:
            self.assertEqual(
                isinstance(regValNotFoundError, FileNotFoundError), True
                , 'Registry value deletion failed'
            )
            self.assertEqual(
                regValNotFoundError.__str__(), 'Reg val not found.'
                , 'Registry value deletion failed'
            )

    def test_createKey(self):
        RegTool.createKey(
            RegEnv.HKEY_CLASSES_ROOT, r'*\shell\wow\foo', 'bar'
        )
        self.assertEqual('wow' in RegTool.listKey(
            RegEnv.HKEY_CLASSES_ROOT, r'*\shell'
        ), True, 'Path create failed')
        self.assertEqual('foo' in RegTool.listKey(
            RegEnv.HKEY_CLASSES_ROOT, r'*\shell\wow'
        ), True, 'Path create failed')
        self.assertEqual('bar' in RegTool.listKey(
            RegEnv.HKEY_CLASSES_ROOT, r'*\shell\wow\foo'
        ), True, 'Key create failed')

        RegTool.delKey(
            RegEnv.HKEY_CLASSES_ROOT, r'*\shell\wow\foo', 'bar'
        )
        self.assertEqual('bar' in RegTool.listKey(
            RegEnv.HKEY_CLASSES_ROOT, r'*\shell\wow\foo'
        ), False, 'Key delete failed')

        RegTool.delKey(
            RegEnv.HKEY_CLASSES_ROOT, r'*\shell\wow'
        )
        self.assertEqual('wow' in RegTool.listKey(
            RegEnv.HKEY_CLASSES_ROOT, r'*\shell'
        ), False, 'path delete failed')

    def test_writeRegData(self):
        writeData = {
            '__path__': (RegEnv.HKEY_CLASSES_ROOT.value, r'*\shell\testRegData'),
            '__val__': {
                '': ('test reg data write', RegType.REG_SZ.value)
            }
            , 'child-0': {
                '__path__': (RegEnv.HKEY_CLASSES_ROOT.value, r'*\shell\testRegData\child-0'),
                '__val__': {
                    '': ('test reg data child-0 write', RegType.REG_SZ.value)
                }
                , 'child-0-0': {
                    '__path__': (RegEnv.HKEY_CLASSES_ROOT.value, r'*\shell\testRegData\child-0\child-0-0'),
                    '__val__': {
                        '': ('test reg data child-0-0 write', RegType.REG_SZ.value)
                    }
                }
            }
            , 'child-1': {
                '__path__': (RegEnv.HKEY_CLASSES_ROOT.value, r'*\shell\testRegData\child-1'),
                '__val__': {
                    '': ('test reg data child-1 write', RegType.REG_SZ.value)
                }
            }
        }

        RegTool.writeKey(writeData)
        self.assertEqual(
            RegTool.recursion(
                *(RegEnv.HKEY_CLASSES_ROOT, r'*\shell')
            )['testRegData'] == writeData, True
            , 'Data write failed'
        )
        RegTool.delKey(
            RegEnv.HKEY_CLASSES_ROOT, r'*\shell\testRegData'
        )
        self.assertEqual(
            RegTool.recursion(
                *(RegEnv.HKEY_CLASSES_ROOT, r'*\shell')
            ).get('testRegData', {}) == writeData, False
            , 'Data delete failed'
        )

        RegTool.writeKeyByStr(json.dumps(writeData))
        self.assertEqual(
            RegTool.recursion(
                *(RegEnv.HKEY_CLASSES_ROOT, r'*\shell')
            )['testRegData'] == writeData, True
            , 'Data write failed'
        )
        RegTool.delKey(
            RegEnv.HKEY_CLASSES_ROOT, r'*\shell\testRegData'
        )
        self.assertEqual(
            RegTool.recursion(
                *(RegEnv.HKEY_CLASSES_ROOT, r'*\shell')
            ).get('testRegData', {}) == writeData, False
            , 'Data delete failed'
        )

    def test_cpRegData(self):
        writeData = {
            '__path__': (RegEnv.HKEY_CLASSES_ROOT.value, r'*\shell\testRegData'),
            '__val__': {
                '': ('test reg data write', RegType.REG_SZ.value)
            }
            , 'child-0': {
                '__path__': (RegEnv.HKEY_CLASSES_ROOT.value, r'*\shell\testRegData\child-0'),
                '__val__': {
                    '': ('test reg data child-0 write', RegType.REG_SZ.value)
                }
                , 'child-0-0': {
                    '__path__': (RegEnv.HKEY_CLASSES_ROOT.value, r'*\shell\testRegData\child-0\child-0-0'),
                    '__val__': {
                        '': ('test reg data child-0-0 write', RegType.REG_SZ.value)
                    }
                }
            }
            , 'child-1': {
                '__path__': (RegEnv.HKEY_CLASSES_ROOT.value, r'*\shell\testRegData\child-1'),
                '__val__': {
                    '': ('test reg data child-1 write', RegType.REG_SZ.value)
                }
            }
        }

        RegTool.writeKey(writeData)
        self.assertEqual(
            RegTool.recursion(
                *(RegEnv.HKEY_CLASSES_ROOT, r'*\shell')
            )['testRegData'] == writeData, True
            , 'Data write failed'
        )
        source = (RegEnv.HKEY_CLASSES_ROOT, r'*\shell\testRegData')
        target = (RegEnv.HKEY_CLASSES_ROOT, r'*\shell\testRegData-mv-new')
        RegTool.cpKey(source, target)

        def replacePath(regData: {}):
            regData['__path__'] = (
                target[0].value,
                regData['__path__'][1].replace(source[1], target[1])
            )
            for key, regDataChild in regData.items():
                if key[:2] != '__':
                    replacePath(regDataChild)
            return regData
        self.assertEqual(
            RegTool.recursion(
                *(RegEnv.HKEY_CLASSES_ROOT, r'*\shell')
            )['testRegData-mv-new'] == replacePath(writeData), True
            , 'Data write failed'
        )
        RegTool.delKey(*source)
        RegTool.delKey(*target)

    def test_mvRegData(self):
        writeData = {
            '__path__': (RegEnv.HKEY_CLASSES_ROOT.value, r'*\shell\testRegData'),
            '__val__': {
                '': ('test reg data write', RegType.REG_SZ.value)
            }
            , 'child-0': {
                '__path__': (RegEnv.HKEY_CLASSES_ROOT.value, r'*\shell\testRegData\child-0'),
                '__val__': {
                    '': ('test reg data child-0 write', RegType.REG_SZ.value)
                }
                , 'child-0-0': {
                    '__path__': (RegEnv.HKEY_CLASSES_ROOT.value, r'*\shell\testRegData\child-0\child-0-0'),
                    '__val__': {
                        '': ('test reg data child-0-0 write', RegType.REG_SZ.value)
                    }
                }
            }
            , 'child-1': {
                '__path__': (RegEnv.HKEY_CLASSES_ROOT.value, r'*\shell\testRegData\child-1'),
                '__val__': {
                    '': ('test reg data child-1 write', RegType.REG_SZ.value)
                }
            }
        }

        RegTool.writeKey(writeData)
        self.assertEqual(
            RegTool.recursion(
                *(RegEnv.HKEY_CLASSES_ROOT, r'*\shell')
            )['testRegData'] == writeData, True
            , 'Data write failed'
        )
        source = (RegEnv.HKEY_CLASSES_ROOT, r'*\shell\testRegData')
        target = (RegEnv.HKEY_CLASSES_ROOT, r'*\shell\testRegData-mv-new')
        RegTool.mvKey(source, target)

        def replacePath(regData: {}):
            regData['__path__'] = (
                target[0].value,
                regData['__path__'][1].replace(source[1], target[1])
            )
            for key, regDataChild in regData.items():
                if key[:2] != '__':
                    replacePath(regDataChild)
            return regData
        self.assertEqual(
            RegTool.recursion(
                *(RegEnv.HKEY_CLASSES_ROOT, r'*\shell')
            )['testRegData-mv-new'] == replacePath(writeData), True
            , 'Data write failed'
        )
        RegTool.delKey(*target)
