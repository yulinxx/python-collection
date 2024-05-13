import os
from shutil import copyfile


class HandleFile:
    def __init__(self, origin_dir, new_dir, ignore_dir):
        self.origin_dir = origin_dir
        self.new_dir = new_dir
        self.ignore_dir = ignore_dir
        self.add_suffix = '_aprilxx'

    def __is_txt_file(self, fileName:str):
        #return True
        try:
            with open(fileName, 'r', encoding='utf-8') as file:
                for line in file:
                    break
            return True
        except UnicodeDecodeError:
            #print(f'\n!!!!!!!!!!!! {fileName} xError UnicodeDecodeError \n')
            return False
        except Exception as e:
            #print(f'\n!!!!!!!!!!!! {fileName} xError: {e}\n')
            return False

    def copy_files(self):
        """
        """
        # 在这里,将老目录去掉 strFind = {str} '\\'
        countIndex = 0
        parentPath = '@'
        pathLen = len(self.origin_dir)
        errorList = []

        # 当前文件夹的路径 子目录列表  当前路径下的所有文件
        for rootDir, dirName, fileNames in os.walk(self.origin_dir):
            strFind = '\\'
            rootDir = rootDir.replace('\\', '/')
            nPos = rootDir.rfind('/')
            curDir = rootDir[nPos + len(strFind):]  # 当前文件夹路径中的最后的文件夹名称
            if curDir in self.ignore_dir:  # 忽略的文件夹不复制
                parentPath = rootDir  # 保存当前路径,防止子目录继续遍历
                continue

            subPos = rootDir.find(parentPath)
            if subPos >= 0:
                continue

            parentPath = '@'

            # 若目录不存在,则创建新的目录进行文件存储
            # mkDir = rootDir.replace(self.origin_dir, self.new_dir)
            mkDir = self.new_dir + '/' + rootDir[pathLen:]
            if not os.path.exists(mkDir):
                try:
                    os.mkdir(mkDir)
                except:
                    continue

            for strFileName in fileNames:  # 遍历当前文件夹下所有的文件
                countIndex += 1

                originFile = os.path.join(rootDir, strFileName)
                fInfo = os.path.splitext(originFile)

                fileSuffix = fInfo[-1].lower()

                if self.__is_txt_file(originFile)  or fileSuffix.lower() == ".idx":
                    try:
                        binOpen = open(originFile, 'rb')
                        binCont = binOpen.read()
                        binOpen.close()

                        newFileName = mkDir + '/' + strFileName + self.add_suffix
                        newFile = open(newFileName, 'wb')
                        e = newFile.write(binCont)
                        newFile.close()
                    except:
                        print(f"\n!!!!!!!!!!!! xError {fileSuffix} -> {originFile} to {newFileName}\n")
                        errorList.append(f"\n!!!!!!!!!!!! xxx xError {fileSuffix} -> {originFile} to {newFileName}\n")
                    finally:
                        if len(fileSuffix) < 1:
                            fileSuffix = "        "

                        print(f"{fileSuffix} -- {originFile} ---> {newFileName}")
                        
                else:  # 不是文本文件,则直接进行复制
                    newFileName = mkDir + '/' + strFileName
                    dst = copyfile(originFile, newFileName)
                    if dst:
                        print(f"{fileSuffix} -- copy: {newFileName} ---> {countIndex}")
                    else:
                        errorList.append(f"\n!!!!!!!!!!!! Copy xError {fileSuffix} -> {originFile} to {newFileName}\n")
                        print(f"{fileSuffix} -- copy: {newFileName} ---> {countIndex}")

        print('copyFile: ' + str(countIndex) + ' files')
        for e in errorList:
            print(e)
            
    def rnameSuffix(self):

        """
            将文件夹中的文件名去掉指定的后缀\n
        """
        removeLen = len(self.add_suffix)
        countIndex = 0

        errorList = []

        for root, dirname, filename in os.walk(self.new_dir):
            for f in filename:
                # 取得文件名的后面的字符(数量和增加的后缀一致)
                strSuffix = f[-removeLen:]

                # 判断文件后面的字符 是否是 新增的后缀
                # 若是新增的后缀,则去掉, 否则,不作处理
                if strSuffix == self.add_suffix:
                    fileName = os.path.join(root, f)
                    newName = fileName[:-removeLen]
                    if not os.path.exists(newName):
                        os.rename(fileName, newName)
                    else:
                        os.remove(fileName)

                    print(f"{fileName} -- copy: {newName} ---> {countIndex}")

                countIndex += 1
                


if __name__ == '__main__':
    print('-------------------------')
    print('----------Begin----------')

    origin_dir = r'C:/CAD/MantiSoft/'  # 源路径
    new_dir = r'E:/MantiSoft'  # 新路径 或 要还原的路径

    ignore_dir = ['.vs', '.vscode', '.ide', 'build', 'CMake-build']

    handle_obj = HandleFile(origin_dir, new_dir, ignore_dir)

    opt_copy = True
    #opt_copy = False
    
    if opt_copy:
        if not os.path.exists(origin_dir):
            print('......路径有问题:')
            raise OSError

        print('......开始复制文件:')
        handle_obj.copy_files()
    else:
        if not os.path.exists(new_dir):
            print('......路径有问题:')
            raise OSError
            
        print('......开始还原文件:')
        handle_obj.rnameSuffix()
        
    print('\n......The End......')
