# coding:utf-8

import os
import os.path

rubbext = ['.tmp', '.bak', '.old', '.wbk', '.xlk', '._mp',
           '.log', '.gid', '.chk', '.syd', '.$$$', '.@@@', '.~*']


def clenRubb(path):
    global rubbext
    total = 0
    filesize = 0
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
                        try:
                            print("正在删除 %s" % fname)
                            os.remove(fname)
                        except:
                            pass
                except ValueError:
                    pass
        except:
            pass
    print("清理%s个垃圾，释放%.2fMB的空间！" % (total, filesize / 1024 / 1024))


if __name__ == "__main__":
    path = "C:/"
    clenRubb(path)
    os.system('pause')
