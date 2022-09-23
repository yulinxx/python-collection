import os
from shutil import copyfile

class HandleFile:
    def __init__(self, originDir, typeList, newDir, ignoreDir, addSuffix):
        self.originDir = originDir
        self.typeList = typeList
        self.newDir = newDir
        self.ignoreDir = ignoreDir
        self.addSuffix = addSuffix

    def copyFiles(self):
        """
            这个是函数的帮助说明文档，help时会显示\n
            将文件夹中的文件复制至新文件中,并添加后缀名,只处理列表中的文件类型\n

            param1 - 要处理的文件夹  param2 -  要处理的文件类型\n
            param3 - 存储的文件夹    param4 - 新文件要添加的后缀名\n

            Returns:  共处理的文件数量\n
        """
        # 在这里,将老目录去掉
        pathLen = len(self.originDir)
        countIndex = 0

        for root, dirname, filename in os.walk(originDir):
            for curDir in dirname:
                if curDir in self.ignoreDir:
                    continue
                else:
                    break

            mkDir = self.newDir + root[pathLen:]

            # 若目录不存在,则创建新的目录进行文件存储
            if not os.path.exists(mkDir):
                os.mkdir(mkDir)

            for strName in filename:
                countIndex += 1

                originFile = os.path.join(root, strName)
                fInfo = os.path.splitext(originFile)
                if fInfo[-1].lower() in typeList:
                    newFileName = mkDir + '/' + strName + self.addSuffix
                    # 新路径 + 源文件名称 + 新增后缀
                    with open(originFile, 'r', encoding='utf-8') as f:
                        with open(newFileName, 'w', encoding='utf-8') as newFile:
                            newFile.write(f.read())
                else:  # 若不存在列表中(未加密的文件),则直接进行复制
                    newFileName = mkDir + '/' + strName
                    copyfile(originFile, newFileName)

        print('copyFile Process: ' + str(countIndex) + ' files')

    def rnameSuffix(self):

        """
            将文件夹中的文件名去掉指定的后缀\n
            param1 - 要处理的文件夹     param2 - 要去掉的后缀名\n
            Returns:  共处理的文件数量\n
        """
        removeLen = len(self.addSuffix)
        countIndex = 0

        for root, dirname, filename in os.walk(self.newDir):
            for f in filename:
                # 取得文件名的后面的字符(数量和增加的后缀一致)
                strSuffix = f[-removeLen:]

                # 判断文件后面的字符 是否是 新增的后缀
                # 若是新增的后缀,则去掉, 否则,不作处理
                if strSuffix == self.addSuffix:
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

    originDir = r'E:/RD/GraphicsComponent_QtExamplexx20220701'  # 源路径
    newDir = r'E:/RD/GraphicsComponent_QtExamplexxx_2022.09.22'  # 新路径
    ignoreDir = ['.vs', '.vscode', '.ide', 'build']
    addSuffix = r'_xx'  # 添加后缀
    typeList = ['.h', '.cpp', '.txt', '.hpp', '.inl', '.py', '.qrc', '.c', '.cxx', '.ui', '.cmake', '.rc']  # 文件类型

    Handle = HandleFile(originDir, typeList, newDir, ignoreDir, addSuffix)
    print('......Step 1:')
    # Handle.copyFiles()

    print('......Step 2:')
    Handle.rnameSuffix()

    print('......The End......')
