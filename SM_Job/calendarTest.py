import calendar, datetime
print('---------- 1')
c = calendar.TextCalendar(calendar.MONDAY)
print('---------- 2')
# 返回日期星期几[0-6]
print(calendar.weekday(2021, 4, 12))
print('---------- 3')
# 用来判断是否时闰年
print(calendar.isleap(2021))
print('---------- 4')
# 两个年份之间的闰年有多少
print(calendar.leapdays(2000, 2050))
print('---------- 5')
# 返回星期对应缩写，参数代表缩写英文的长度
print(calendar.weekheader(2))
print('---------- 6')
# 返回一个月的日历矩阵
print(calendar.monthcalendar(2021, 4))
print('---------- 7')
# 将日期转换为时间戳
print(calendar.timegm(datetime.datetime(2021, 4, 3).timetuple()))
print('---------- 8')

# 返回当月日历
print(calendar.prmonth(2021, 4))
print('---------- 9')

# 返回整年日历
print(calendar.prcal(2021))
print('---------- 10')



#
#
#
# from itertools import *
# resData = calendar.monthcalendar(2022, 11, 11)
# # print(calendar.monthcalendar(2022, 11))
# print('---------- 11')
# dataList = list(chain.from_iterable(resData))
# print(dataList)
#
# resData = calendar.monthcalendar(2022, 12)
# # print(calendar.monthcalendar(2022, 12))
# print('---------- 12')
# dataList = list(chain.from_iterable(resData))
# print(dataList)

import calendar
from itertools import chain

resData = calendar.monthcalendar(2022, 10)

dataList = list(chain.from_iterable(resData))
print("""生成月历""")
dataList = [i for i in dataList if i != 0]
print(dataList)

# 每个人排班天数
schedule_day = 7

# 开始排班的日期
start_date = 15

# 参与排班的用户分别排了哪些日期
user_dict = {'A': [], 'B': [], 'C': []}

user_list = list(user_dict.keys())

# list2 = ['' for i in range(start_date-1)]

# 剩余未排满的天数
num = 0

# 从谁开始排班
user_index = 0

for user in user_list[user_index:]:
    # 假如开始排班的日期到月底的天数大于7天,则从开始排班的日期开始截取7个日期放到当前用户的排班日期列表里
    if len(dataList[(start_date - 1):]) > schedule_day:
        temp_list = dataList[(start_date - 1):(start_date + schedule_day - 1)]

        # 为开始日期重新赋值,这里就是22日重新开始排下一个人
        start_date = start_date + schedule_day
        # 当前用户已经排满一个班期,则从下一个人开始排班
        user_index = user_index + 1

    else:
        temp_list = dataList[start_date:]
    user_dict[user].extend(temp_list)

print(user_dict)
