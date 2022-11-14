# from jobCalender import jobCalender
# from jobManager import jobManager
#
# from WordGeneration import WordGeneration
# from ExcelGeneration import ExcelGeneration
#
# """ 用于存储结果的配置文件: cfg.ini
# # 已生成报表的月份
# [gen_data]
# 2022.11
#
# # 报表文件保存路径
# [report_file]
# /home/x/report/2022-11.xls
#
# # 生成排班时,最后排到的人员索引
# [last_person_index]
# 2
# # 最后排班的人,已排的天数
# [last_person_days]
# 4
# """
#
# if __name__ == '__main__':
#     print("\n\n\n")
#
#     # 查询ini
#     dateRes = getIniDate() # 得到配置文件的中的日期 gen_data
#     # 今天的月份 和 已生成排班的月份 是否一致
#
#
#     if(today.month() == dateRes.month())    # 若一至,则进行查询
#         reportFile = getIniReportFile()  # 得到配置文件的中的排班表文件 [report_file]
#         # 根据当前日期,查询排班报表, 打印当天值班的人
#         person = getReportPerson(today, reportFile)
#         print("Today is: {person}")
#     else    # 不一致, 则需要生成报表,并查询
#         # 排班算法
#         jobObj = doJobManager()
#         jobObj.do(startDay, personList) # 生成排班
#         jobData = jobObj.getData()
#
#         # 将排班算法生成报表
#         excelObj = excelClass()
#         excelObj.do(jobData) # 生成排班报表
#
#
#         personIndex = jobObj.getLastPersonIndex()  # 获取该月排班到的人员索引
#         personDays = jobObj.getLastPersonDays() # 获取该月排班到的人员,排了多少天班,便于下个月继续排班
#         excelFile = excelObj.getReportFile()  # 获取排班报表的保存文件
#
#         # 生成配置文件
#         iniObj = iniClass()
#         iniObj.Save(today.year, today.month, excelFile, personIndex, personDays )
#
#
#
#
#
#
#
#
#
#
#
#     calenderObj = jobCalender()  # 构建一个日历对象
#
#     calenderObj.SetStartTime(2022, 11, 5)
#     resData = calenderObj.GenData()
#     print(f"-----------\n2022 11:\n{resData}")
#
#     userList = ["A", "B", "C"]
#     jobManagerObj = jobManager(userList=userList, monthData=resData)  # 构建一个人员管理对象
#
#     jobManagerObj.SetScheduleDays(7)
#     jobManagerObj.Do()
#     jobManagerObj.ShowData()
#     # print(jobManagerObj)
#
#     #######################################
#
#     calenderObj.SetStartTime(2022, 12)
#     resData = calenderObj.GenData()
#     print(f"-----------\n2022 12:\n{resData}")
#
#     jobManagerObj = jobManager(userList=userList, monthData=resData)
#     # jobManagerObj.SetData(userList=userList, monthData=resData)
#     jobManagerObj.SetMonthData(monthData=resData)
#     personIndex = jobManagerObj.GetCurrentPersonIndex()
#
#     jobManagerObj.Do(personIndex)
#     jobManagerObj.ShowData()
#
#     # jobManagerObj2 = jobManager(userList=userList, monthData=resData)
#     # jobManagerObj2.SetStartPersonIndex(3)
#     # jobManagerObj2.SetStartPersonNeedDays(6)
#     # jobManagerObj2.Do()
#
#     # calenderObj.SetStartTime(2022, 12)
#     # resData = calenderObj.Start()
#     # print(f"resData:\n{resData}")
#     #
#     #
#     # calenderObj.SetStartTime(2022, 13)
#     # resData = calenderObj.Start()
#     # print(f"resData:\n{resData}")
#
#     # 生成报表
#     # officeObj = WordGeneration()
#     officeObj = ExcelGeneration()
#
#     officeObj.SetData("aaa")
#     officeObj.Do()


from configparser import ConfigParser

config = ConfigParser()


# config['zhangsan'] = {'name': '张三', 'age': 18}
# config['lisi'] = {'name': '李四', 'age': 19}
#
# with open('test.ini', 'w', encoding='utf-8')as f:
#     config.write(f)

config.read('test.ini', encoding='utf-8')
config.set('zhangsan', 'sex', '男')
