# coding:utf-8

import os
import os.path

rubbext = ['.tmp', '.bak', '.old', '.wbk', '.xlk', '._mp',
           '.log', '.gid', '.chk', '.syd', '.$$$', '.@@@', '.~*']


def ScanRubbish(path):
    global rubbext
    total = 0
    filesize = 0
    infos = []
    for root, dirs, files in os.walk(path):
        try:
            for file in files:
                filesplit = os.path.splitext(file)
                if '' == filesplit[1]:
                    continue
                try:
                    if rubbext.index(filesplit[1]) >= 0:
                        fname = os.path.join(os.path.abspath(root), file)
                        total += 1
                        filesize += os.path.getsize(fname)
                        infos.append(fname)

                except ValueError:
                    pass

        except:
            pass
    print("发现%s个垃圾，共占用%.2fMB的空间！" % (total, filesize / 1024 / 1024))
    return infos


def Remove(fname):
    for i in fname:
        try:
            print("正在删除 %s..." % i)
            os.remove(i)
        except:
            pass
    print("清理完毕...")

if __name__ == "__main__":
    path = "C:/"
    rmfiles = ScanRubbish(path)
    Remove(rmfiles)
    os.system('\npause')
