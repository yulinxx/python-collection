import os
import time
import exifread
from PyQt6.QtCore import QThread, pyqtSignal


class processExif(QThread):
    __index = 1
    __listName = []
    tipSignal = pyqtSignal(str)
    endSignal = pyqtSignal()

    def __init__(self, path):
        super(processExif, self).__init__()
        self.__photoPath = path

    def run(self):
        self.__listName = []
        # self.__funcTip("---------------------------------------------\n")
        start = time.time()
        # self.__funcTip("开始..." )
        self.process()

        end = time.time()
        # self.__funcTip("结束...%s 耗时" % (end - start))
        tmDuration = ('%.2f' % (end - start))
        self.tipSignal.emit("结束, 共耗时:%s " % tmDuration)
        # self.__funcTip("---------------------------------------------\n")
        self.tipSignal.emit("---------------------------------------------\n")

        # self.__funcEnd()
        self.endSignal.emit()

    def isImgType(self, filename):
        # 根据文件扩展名，判断是否是需要处理的文件类型
        filename_nopath = os.path.basename(filename)
        f, e = os.path.splitext(filename_nopath)
        if e.lower() in ['.jpg', '.png', '.mpg', '.thm', '.bmp',
                         '.jpeg', '.nef', '.crw', '.cr2']:
            return True
        else:
            return False

    def isVideoType(self, filename):
        # 根据文件扩展名，判断是否是需要处理的文件类型
        filename_nopath = os.path.basename(filename)
        f, e = os.path.splitext(filename_nopath)
        if e.lower() in ['.mp4', '.avi', '.mov']:
            return True
        else:
            return False

    def process(self):
        for curDir, subDirs, fileNames in os.walk(self.__photoPath):
            for fileName in fileNames:
                if self.isImgType(fileName):
                    self.__renameImg(curDir, fileName)
                elif self.isVideoType(fileName):
                    self.__renameVideo(curDir, fileName)

    def __renameImg(self, path, fileName):
        try:
            file = os.path.join(path, fileName)
            fileImg = open(file, 'rb')
            imgInfo = exifread.process_file(fileImg)
            fileImg.close()

            if 'Image Model' in imgInfo \
                    and 'Image Make' in imgInfo \
                    and 'EXIF DateTimeOriginal' in imgInfo:

                imageModel = imgInfo['Image Model']
                if imageModel is None:
                    return False

                imgMake = imgInfo['Image Make']
                if imgMake is None:
                    return False

                imgData = imgInfo['EXIF DateTimeOriginal']
                if imgData is None:
                    return False

                else:
                    strRename = str(imgData).replace(":", "_")
                    strRename = strRename.replace(" ", "_")

                    strRename = self.__uniqueName(strRename)
                    self.__listName.append(strRename)

                    ext = fileName[-4:]
                    strRename += fileName[-4:]
                    strLog = ""
                    if fileName != strRename:
                        os.rename(os.path.join(path, fileName), os.path.join(path, strRename))
                        strLog = "%s - %s  --命名为---> %s\n" % (path, fileName, strRename)
                    else:
                        strLog = "%s - %s --名称与日期一致,未未理\n" % (path, fileName)

                    self.tipSignal.emit(strLog)
                    return True
            else:
                strLog = "%s\%s 无拍摄信息\n" % (path, fileName)

                self.tipSignal.emit(strLog)
                return False
        except:
            pass

    def __renameVideo(self, path, filename):
        # 根据照片的拍照时间生成新的文件名（如果获取不到拍照时间，则使用文件的创建时间）
        fullName = os.path.join(path, filename)
        try:
            if os.path.isfile(fullName):
                vdFile = open(fullName, 'rb')
            else:
                raise "[%s] is not a file!\n" % fullName
        except:
            raise "unopen file [%s]\n" % fullName

        vdData = exifread.process_file(vdFile)
        vdFile.close()

        if vdData:
            # 取得照片的拍摄日期
            try:
                t = vdData['EXIF DateTimeOriginal']
                # 转换成 yyyymmdd_hhmmss的格式
                dateStr = str(t).replace(":", "")[: 10] + "_" + str(t)[11:].replace(":", "")
            except:
                pass
        else:
            # 如果没有取得exif信息，则用图像文件的创建日期作为拍摄日期
            state = os.stat(fullName)
            dateStr = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(state[-2]))

            dirname = os.path.dirname(fullName)
            filename_nopath = os.path.basename(fullName)

        f, e = os.path.splitext(filename_nopath)
        strLog = ''
        try:
            newFileName = os.path.join(dirname, dateStr + e)
            strRename = dateStr + e
            if filename != strRename:
                os.rename(os.path.join(path, filename), os.path.join(path, strRename))
                strLog = "%s - %s  --命名为---> %s\n" % (path, filename, strRename)
            else:
                strLog = "%s - %s --名称与日期一致,未未理\n" % (path, filename)
        except:
            strLog = 'Error'
            pass

        self.tipSignal.emit(strLog)

    def __uniqueName(self, fileName):
        if self.__CheckSame(fileName):  # 有重名文件
            if len(fileName) < 20:  # 原文件名为 年月日时分秒
                fileName += "_"
                fileName += str(self.__index)
                self.__index += 1

            self.__uniqueName(fileName)

        return fileName

    def __CheckSame(self, fileName):
        for file in self.__listName:
            if file == fileName:
                return True

        if len(fileName) < 20:
            self.__index = 1
        return False
