import os
from shutil import copyfile


class HandleFile:
    def __init__(self, origin_dir, txt_list, new_dir, ignore_dir, add_suffix, bin_list=[]):
        self.__originDir = origin_dir
        self.__txtList = txt_list
        self.__binList = bin_list
        self.__newDir = new_dir
        self.__ignoreDir = ignore_dir
        self.__addSuffix = add_suffix

    def copyFiles(self):
        """
            这个是函数的帮助说明文档，help时会显示\n
            将文件夹中的文件复制至新文件中,并添加后缀名,只处理列表中的文件类型\n
            param1 - 要处理的文件夹  param2 -  要处理的文件类型\n
            param3 - 存储的文件夹    param4 - 新文件要添加的后缀名\n
            Returns:  共处理的文件数量\n
        """
        # 在这里,将老目录去掉strFind = {str} '\\'
        countIndex = 0
        parentPath = '@'
        pathLen = len(self.__originDir)
        errorList = []

        # 当前文件夹的路径 子目录列表  当前路径下的所有文件
        for rootDir, dirName, fileNames in os.walk(originDir):
            strFind = '\\'
            rootDir = rootDir.replace('\\', '/')
            nPos = rootDir.rfind('/')
            curDir = rootDir[nPos + len(strFind):]  # 当前文件夹路径中的最后的文件夹名称
            if curDir in self.__ignoreDir:  # 忽略的文件夹不复制
                parentPath = rootDir  # 保存当前路径,防止子目录继续遍历
                continue

            subPos = rootDir.find(parentPath)
            if subPos >= 0:
                continue

            parentPath = '@'

            # 若目录不存在,则创建新的目录进行文件存储
            # mkDir = rootDir.replace(self.__originDir, self.__newDir)
            mkDir = self.__newDir + '/' + rootDir[pathLen:]
            if not os.path.exists(mkDir):
                try:
                    os.mkdir(mkDir)
                except:
                    continue
                    pass

            for strFileName in fileNames:  # 遍历当前文件夹下所有的文件
                countIndex += 1

                originFile = os.path.join(rootDir, strFileName)
                fInfo = os.path.splitext(originFile)

                fileSuffix = fInfo[-1].lower()
                if fileSuffix in self.__binList:  # 二进制文件的读写复制
                    try:
                        binOpen = open(originFile, 'rb')
                        binCont = binOpen.read()
                        binOpen.close()

                        newFileName = mkDir + '/' + strFileName + self.__addSuffix
                        newFile = open(newFileName, 'wb')
                        e = newFile.write(binCont)
                        newFile.close()
                    except:
                        print(f"\nxxxError {fileSuffix} -> {originFile} to {newFileName}\n")
                        errorList.append(f"\nxxxError {fileSuffix} -> {originFile} to {newFileName}\n")
                    finally:
                        print(f"{fileSuffix} -- {originFile} ---> {newFileName}")

                elif fileSuffix in self.__txtList:  # 符合的后缀文件进行后缀改写复制
                    newFileName = mkDir + '/' + strFileName + self.__addSuffix
                    # 新路径 + 源文件名称 + 新增后缀
                    with open(originFile, 'r', encoding='utf-8') as f:
                        with open(newFileName, 'w', encoding='utf-8') as newFile:
                            try:
                                newFile.write(f.read())
                            except:
                                print(f"\nxxxError {newFileName} -> {originFile}\n")
                            finally:
                                print(f"{fileSuffix} -- {newFileName} ---> {countIndex}")
                else:  # 若不存在列表中(未加密的文件),则直接进行复制
                    newFileName = mkDir + '/' + strFileName
                    copyfile(originFile, newFileName)
                    print(f"{fileSuffix} -- {newFileName} ---> {countIndex}")

        print('copyFile Process: ' + str(countIndex) + ' files')
        for e in errorList:
            print(e)

    def rnameSuffix(self):

        """
            将文件夹中的文件名去掉指定的后缀\n
            param1 - 要处理的文件夹     param2 - 要去掉的后缀名\n
            Returns:  共处理的文件数量\n
        """
        removeLen = len(self.__addSuffix)
        countIndex = 0

        for root, dirname, filename in os.walk(self.__newDir):
            for f in filename:
                # 取得文件名的后面的字符(数量和增加的后缀一致)
                strSuffix = f[-removeLen:]

                # 判断文件后面的字符 是否是 新增的后缀
                # 若是新增的后缀,则去掉, 否则,不作处理
                if strSuffix == self.__addSuffix:
                    fileName = os.path.join(root, f)
                    newName = fileName[:-removeLen]
                    if not os.path.exists(newName):
                        os.rename(fileName, newName)
                    else:
                        os.remove(fileName)

                countIndex += 1
                print('rnameSuffix Process: ' + str(countIndex) + ' files')


if __name__ == '__main__':
    print('-------------------------')
    print('----------Begin----------')

    # optCopy = True
    optCopy = False
    originDir = r'C:/CAD/xxx/'  # 源路径

    newDir = r'E:/RD/CAD20221230'  # 新路径 或 要还原的路径

    ignoreDir = ['.vs', '.vscode', '.ide', 'build', 'CMake-build', 'x64']
    binList = ['.idx']  # 以二进制复制的文件后缀

    addSuffix = r'_xx'  # 添加后缀
    txtFileList = ['.h', '.cpp', '.txt', '.hpp', '.inl', '.py', '.c', '.cxx',
                   '.cmake', '.rc', '.ui', '.qrc', '.pro', '.pri', '.sln']  # 文件类型

    HandleObj = HandleFile(originDir, txtFileList, newDir, ignoreDir, addSuffix, binList)

    if optCopy:
        if not os.path.exists(originDir):
            print('......路径有问题:')
            raise OSError
        print('......开始复制文件:')
        HandleObj.copyFiles()
    else:
        if not os.path.exists(newDir):
            print('......路径有问题:')
            raise OSError
        print('......开始还原文件:')
        HandleObj.rnameSuffix()

    print('......The End......')
