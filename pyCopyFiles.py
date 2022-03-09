import os
from shutil import copyfile

def copyFiles(originDir, typeList, newDir, addSuffix):
    """
        这个是函数的帮助说明文档，help时会显示\n
        将文件夹中的文件复制至新文件中,并添加后缀名,只处理列表中的文件类型\n
        
        param1 - 要处理的文件夹  param2 -  要处理的文件类型\n
        param3 - 存储的文件夹    param4 - 新文件要添加的后缀名\n
        
        Returns:  共处理的文件数量\n
    """
    # 在这里,将老目录去掉
    pathLen = len(originDir)
    countIndex = 0

    for root, dirname, filename in os.walk(originDir):
        mkDir = newDir + root[pathLen:]

        # 若目录不存在,则创建新的目录进行文件存储
        if os.path.exists(mkDir) is False:
            os.mkdir(mkDir)

        for strName in filename:
            
            originFile = os.path.join(root, strName)            
            fInfo = os.path.splitext(originFile)
            if fInfo[-1] in typeList:
                newFileName = mkDir + '/' + strName + addSuffix

                # 新路径 + 源文件名称 + 新增后缀
                try:
                    with open(originFile, 'r', encoding='utf-8') as f:
                        # print('------检测文件是否能正常读取--------')
                        # print(originFile, ' --- ', f.readline())
                        with open(newFileName, 'w', encoding='utf-8') as newFile:
                            newFile.write(f.read())
                            countIndex += 1
                except:
                    print(originFile + ' Error -------')

            else:   # 若不存在列表中(未加密的文件),则直接进行复制
                newFileName = mkDir + '/' + strName
                copyfile(originFile, newFileName)
                countIndex += 1

    return countIndex


def rnameSuffix(processDir, removeSuffix):
    """
        将文件夹中的文件名去掉指定的后缀\n
        param1 - 要处理的文件夹     param2 - 要去掉的后缀名\n
        Returns:  共处理的文件数量\n
    """
    removeLen = len(removeSuffix)
    countIndex = 0

    for root, dirname, filename in os.walk(processDir):
        for f in filename:
            # 取得文件名的后面的字符(数量和增加的后缀一致)
            strSuffix = f[-removeLen:]

            # 判断文件后面的字符 是否是 新增的后缀
            # 若是新增的后缀,则去掉, 否则,不作处理
            if(strSuffix == removeSuffix):
                fileName = os.path.join(root, f)
                newName = fileName[:-removeLen]
                if not os.path.exists(fileName):
                    os.rename(fileName, newName)
                    countIndex += 1
    
    return countIndex


if __name__ == '__main__':
    print('-------------------------')
    print('----------Begin----------')

    originDir = r'E:/Proj/CAD' # 源路径
    newDir = r'F:/xxCAD/'    # 新路径
    addSuffix = r'_xx'  # 添加后缀
    typeList = ['.c', '.h', '.cpp', '.txt', '.hpp', '.inl', '.py'] # 文件类型

    print('......Step 1:')
    count = copyFiles(originDir, typeList, newDir, addSuffix)
    print('copyFile Process: ' + str(count) + ' files')
    
    # print('......Step 2:')
    # count = rnameSuffix(newDir, addSuffix)
    # print('rnameSuffix Process: ' + str(count) + ' files')

    print('-----------End-----------')
    print('-------------------------')


