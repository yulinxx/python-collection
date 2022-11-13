class jobManager:
    def __init__(self, userList, monthData):
        self.__userList = userList  # 人员列表
        self.__monthData = monthData  # 月历数据

        self._curPersonIndex = 0
        self._curPersonDays = 0

        self._ScheduleDays = 7

        # k/v  人员/安排的时间
        self._userDataDict = {}
        for user in userList:
            self._userDataDict[user] = []

    def SetData(self, userList, monthData):
        self.__userList = userList
        self.__monthData = monthData

        self._userDataDict = {user: [] for user in userList}



    # def __str__(self):
    def ShowData(self):
        """print"""
        for key in self._userDataDict:
            print(key)

            v = self._userDataDict[key]
            print(v)
            # for l in v:
            #     print(l)

    def GetCurrentPersonIndex(self):
        """查询分配的人员索引"""
        return self._curPersonIndex

    def Set(self, indexPerson: int = 0):
        """设置排班日期"""

        curDayIndex = 0  # 当前分配的日期索引

        # 第一次分配,特殊处理
        # 判断上次是否有人员分配未完整
        curUser = self.__userList[indexPerson]  # 当前分配的人员
        if self._curPersonDays > 0:  # 上次有人只分配了 N 天
            # 该人还需分配的天数6
            needDays = self._ScheduleDays - self._curPersonDays

            countDays = len(self.__monthData)
            if countDays > needDays:    # 若该月的天数够用
                temp = self.__monthData[0:needDays]
                self._userDataDict[curUser].extend(self.__monthData[0:needDays])  # 补上个月剩余的天数
                curDayIndex += needDays
                indexPerson += 1
            else:   # 不够用
                self._userDataDict[curUser].extend(self.__monthData[0:])  # 补上个月剩余的天数
                self._curPersonIndex = indexPerson
                self._curPersonDays += countDays # 再追加该月的天数
                return

        loopUser = True
        while loopUser:  # 遍历用户
            for user in self.__userList[indexPerson:]:
                if len(self.__monthData[curDayIndex:]) >= self._ScheduleDays:
                    self._userDataDict[user].extend(self.__monthData[curDayIndex:curDayIndex + self._ScheduleDays])
                    curDayIndex += self._ScheduleDays

                    indexPerson += 1

                    # indexPerson %= len(self.__userList)

                    if indexPerson > len(self.__userList) - 1:
                        indexPerson = 0

                    self._curPersonDays = 0

                else:   # 剩余所有的月份分配给指定人员
                    self._userDataDict[user].extend(self.__monthData[curDayIndex:])

                    self._curPersonDays = len(self.__monthData[curDayIndex:])  # 当前只分配了N天
                    self._curPersonIndex = indexPerson  # 保存当前分配的人员索引

                    loopUser = False
                    break

        print("End of While")

    ####################################################
    def SetScheduleDays(self, days: int = 7):
        self._ScheduleDays = days

    def GetScheduleDays(self):
        return self._ScheduleDays

    def SetUser(self, userList):
        """设置排班人员"""
        self.__userList = userList

    def AddUser(self, user):
        """添加单个排班人员"""
        # self.__userList.append(user)
        pass

    def DelUser(self, user):
        """删除排班人员"""
        # self.__userList.delte(user)
        pass

    def SortUserUp(self, user):
        """将该排班人员上移"""
        self.__SortUserUp(user, True)

    def SortUserDown(self, user):
        """将该排班人员下移"""
        self.__SortUserUp(user, False)

    def __SortUserUp(self, user, up=True):
        """排序人"""
        # if(up)
        #     list(user).up
        # else
        #     list(user).down
        pass
