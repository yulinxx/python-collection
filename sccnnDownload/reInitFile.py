# -*- coding:utf-8 -*-
"""
将素材解压后,进行重命名,并移动位置
"""

import os
import shutil

rootdir = 'D:/xx/Pictures/Matter/'

if __name__ == "__main__":
    for root, dirs, files in os.walk(rootdir):
        mainName = dirs

        for file in files:
            pathX = os.path.join(root, file).replace('\\', '/')
            lists = pathX.split('/')
            print(lists[-3])

            index = file.rfind('.')
            ext = file[index:]
            try:
                oldPath = os.path.join(root, file)
                newPath = os.path.join(root, lists[-3] + ext)
                os.rename(oldPath, newPath)
                shutil.move(newPath, rootdir)
            except:
                print(os.path.join(root, file))
                pass
