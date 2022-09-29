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
        # 在这里,将老目录去掉
        pathLen = len(self.__originDir)
        countIndex = 0

        for rootDir, dirName, fileNames in os.walk(originDir):

            for curDir in dirName:
                if curDir in self.__ignoreDir:  # 忽略的文件夹不复制
                    continue
                else:
                    break

            # 若目录不存在,则创建新的目录进行文件存储
            mkDir = self.__newDir + rootDir[pathLen:]
            if not os.path.exists(mkDir):
                os.mkdir(mkDir)

            for strFileName in fileNames:
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
    originDir = r'C:\Users\april\Documents\cad\GraphicsComponent_QtExample'  # 源路径

    newDir = r'E:\RD\GraphicsComponent_QtExample_git'  # 新路径 或 要还原的路径

    ignoreDir = ['.vs', '.vscode', '.ide', 'build']
    addSuffix = r'_xx'  # 添加后缀
    txtFileList = ['.h', '.cpp', '.txt', '.hpp', '.inl', '.py', '.c', '.cxx',
                   '.cmake', '.rc', '.ui', '.qrc', '.pro', '.pri']  # 文件类型

    binList = ['.idx']

    HandleObj = HandleFile(originDir, txtFileList, newDir, ignoreDir, addSuffix, binList)

    if optCopy:
        print('......复制文件:')
        HandleObj.copyFiles()
    else:
        print('......还原文件:')
        HandleObj.rnameSuffix()

    print('......The End......')
