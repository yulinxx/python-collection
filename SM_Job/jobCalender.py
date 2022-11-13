import calendar
from itertools import *


class jobCalender:
    def __init__(self):
        self.__monthData = None  # 保存月历数据
        self.__bInit = False  # 访类是否正确初始化

    def __del__(self):
        pass

    def __initStartDate(self, year: int = 2022, month: int = 11, day: int = 1):
        """ 保存日期数据 """
        self.__yearS = year
        self.__monthS = month
        self.__dayS = day

    def __genMonthData(self):
        """生成月历"""
        monthData = calendar.monthcalendar(self.__yearS, self.__monthS)
        dataList = list(chain.from_iterable(monthData))
        self.__monthData = [i for i in dataList if i != 0]
        self.__monthData = self.__monthData[self.__dayS - 1:]
        return self.__monthData

    def SetStartTime(self, year: int = 2022, month: int = 11, day: int = 1):
        """排班的开始日期"""
        # 判断输入的是否正确 以及时间是否在过去的时间
        if month < 0 or month > 12:
            self.__bInit = False
            return

        self.__bInit = True

        self.__initStartDate(year, month, day)

    def Start(self):
        """开始排班"""
        if self.__bInit:
            return self.__genMonthData()
        else:
            print("---Error: Init Error")
