#!/usr/bin/env python
# -*- encoding: utf-8 -*-

def main():
    curChangeLog = []
    with open('./CHANGELOG.zh-CN.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        flag = False
        for line in lines:
            if line[:3] == '## ':
                if flag: break
                flag = not flag
            if flag: curChangeLog.append(line)
    with open('./latestChangeLog.md', 'w', encoding='utf-8') as f:
        f.write(''.join(curChangeLog))
    print('The latest changes are generated successfully.')


if __name__ == '__main__':
    main()
