class jobManager:
    def __init__(self, userList, monthData, schedule_days):
        self._userList = userList  # 人员列表
        self._monthData = monthData  # 月历数据

        self._curPersonIndex = 0
        self._curPersonDays = 0

        self._ScheduleDays = schedule_days

        # k/v  人员/安排的时间
        self._userDataDict = {}
        for user in userList:
            self._userDataDict[user] = []


    def SetUser(self, userList):
        """设置参与排班的用户列表"""
        self._userList = userList
        self._userDataDict = {user: [] for user in userList}

    def SetMonthData(self, monthData):
        """设置这个月需要排班的日期"""
        self._monthData = monthData
        self._userDataDict = {user: [] for user in self._userList}
        self._dateDict = {}

    def get_schedule(self):
        """获取排了班的数据"""
        date_schedule = {}
        for user_data in self._userDataDict.items():
            for i in user_data[1]:
                date_schedule[i] = user_data[0]
        return date_schedule

    def getCurPersonIndex(self):
        """查询分配的人员索引"""
        return self._curPersonIndex
    
    def getCurPersonDays(self):
        """查询分配的人员分配了多少天"""
        return self._curPersonDays

    def setCurPersonIndex(self, index):
        """设置分配的人员索引"""
        self._curPersonIndex = index

    def setCurPersonDays(self, day):
        """查询分配的人员分配了多少天"""
        self._curPersonDays = day

    def Do(self, indexPerson: int=0):
        """设置排班日期"""

        curDayIndex = 0  # 当前分配的日期索引

        # 第一次分配,特殊处理
        # 判断上次是否有人员分配未完整
        curUser = self._userList[indexPerson]  # 当前分配的人员
        if self._curPersonDays > 0:  # 上次有人只分配了 N 天
            # 该人还需分配的天数6
            needDays = self._ScheduleDays - self._curPersonDays

            countDays = len(self._monthData)
            if countDays > needDays:  # 若该月的天数够用
                temp = self._monthData[0:needDays]
                self._userDataDict[curUser].extend(self._monthData[0:needDays])  # 补上个月剩余的天数
                curDayIndex += needDays
                indexPerson += 1
            else:  # 不够用
                self._userDataDict[curUser].extend(self._monthData[0:])  # 补上个月剩余的天数
                self._curPersonIndex = indexPerson
                self._curPersonDays += countDays  # 再追加该月的天数
                return

        loopUser = True
        while loopUser:  # 遍历用户
            for user in self._userList[indexPerson:]:
                if len(self._monthData[curDayIndex:]) >= self._ScheduleDays:
                    self._userDataDict[user].extend(self._monthData[curDayIndex:curDayIndex + self._ScheduleDays])
                    curDayIndex += self._ScheduleDays

                    indexPerson += 1

                    # indexPerson %= len(self._userList)

                    if indexPerson > len(self._userList) - 1:
                        indexPerson = 0

                    self._curPersonDays = 0  # 还需要分配的天数

                else:  # 剩余所有的月份分配给指定人员
                    self._userDataDict[user].extend(self._monthData[curDayIndex:])

                    self._curPersonDays = len(self._monthData[curDayIndex:])  # 当前只分配了N天
                    self._curPersonIndex = indexPerson  # 保存当前分配的人员索引

                    loopUser = False
                    break

        return self.get_schedule()

    ####################################################
    def SetScheduleDays(self, days: int = 7):
        self._ScheduleDays = days

    def GetScheduleDays(self):
        return self._ScheduleDays

    def AddUser(self, user):
        """添加单个排班人员"""
        # self._userList.append(user)
        pass

    def DelUser(self, user):
        """删除排班人员"""
        # self._userList.delete(user)
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
