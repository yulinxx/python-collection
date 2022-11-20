import ast
import configparser
import datetime
import os
import pathlib

from duty.jobCalender import jobCalender
from duty.jobManager import jobManager


def gen_leader_schedule(user_list: list, schedule_days: int, year: int, month: int, day: int = 1,
                        person_index: int = None, person_days: int = None, ):
    """
    生成值班长排班

    :param user_list: 参与排班的用户列表
    :param schedule_days: 排班的周期
    :param year: 开始排班的年
    :param month: 开始排班的月
    :param day: 开始排班的日
    :param person_days: 当前的人已经排了多少天
    :param person_index: 当前排到的人的索引
    :return:date_schedule:dict 日期为键,值班的人为值, person_index:int 上一次排班排到了谁, person_days:int 上一次排班的人已经排了的天数
    """
    calenderObj = jobCalender()  # 构建一个日历对象
    # 设置开始排班的日期
    calenderObj.SetStartTime(year, month, day)
    # 得到当月需要排班的日期
    resData = calenderObj.GenData()
    # 构建排班的对象
    jobManagerObj = jobManager(userList=user_list, monthData=resData, schedule_days=schedule_days)  # 构建一个人员管理对象

    # 排好班的字典
    if person_days is not None:
        jobManagerObj.setCurPersonDays(person_days)
    if person_index is not None:
        jobManagerObj.setCurPersonIndex(person_index)

    date_schedule = jobManagerObj.Do()
    person_index = jobManagerObj.getCurPersonIndex()
    person_days = jobManagerObj.getCurPersonDays()

    return date_schedule, person_index, person_days


###############################################################
if __name__ == '__main__':

    if True:
        name = '增加测试'
        # 参与排班的人员
        userList = ["王森鹏", "黄吉", "刘欢", "黄小敏"]
        userList.append(name)
        is_change = True
        is_add = True

    if False:
        # 需要传入删除的人的索引
        del_index = userList.remove('黄小敏')
        is_del = False

    schedule_days = 7

    # 开始排班日期的年月日,需要写全格式,年份为4位,月份和日为2位
    startY = 2022
    startM = 11
    startD = 14

    # ----------------------当前日期部分-------------------------------------------------------
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    # 当前年月如:2022-11
    current_year_month = f'{str(datetime.date.today())[:-3]}'

    # ----------------------配置文件部分-------------------------------------------------------
    # 配置文件的路径
    ini_path = pathlib.Path(__file__).parent.joinpath("schedule_setting.ini")
    # 构建配置对象
    configObj = configparser.ConfigParser()

    # 如果存在配置文件
    if os.path.exists(ini_path):

        # 先读取配置文件中生成的排班表的年月gen_data
        configObj.read(ini_path, encoding='utf-8')
        gen_data = configObj.get("init_settings", "gen_data")

        # 判断该日期与当前年月是否相等,如果相等则当前年月已经排班,只需要读取排班数据
        if gen_data == current_year_month:
            print("已有排班时----------")
            # 读取排班
            schedule = configObj.get("init_settings", "schedule")  # 字符串格式需要转成字典
            date_schedule = ast.literal_eval(schedule)

            # 假如修改了()人员列表人员,则需要从增加的次日开始,重新排班,并保存到配置文件中
            if is_change:
                today = datetime.date.today()
                # 今天及之前的排班数据都有效,可保存
                normal_schedule_dic = {k: v for k, v in date_schedule.items() if k <= today}

                # 今天之后的数据不正常需改写
                unnormal_schedule_dic = {k: v for k, v in date_schedule.items() if k > today}

                # 今天值班的人假设为C
                today_person = date_schedule[today]
                today_person_index = userList.index(today_person)

                # 默认C剩余排班为0
                need_days = 0

                # 往后查看,从明天开始排班为C的人有几天
                for date in sorted(unnormal_schedule_dic.keys()):
                    if unnormal_schedule_dic[date] == today_person:
                        need_days += 1
                    else:
                        # 只要一查到排班不是C的,立马不再往后查询
                        break

                # # 假如c已经排满了
                # if need_days == 0:
                #     if is_add:
                #         pass
                #     if is_del:
                #
                #     person_days = 0
                # # 假如C还有需要排的天数
                # else:
                #     pass

                # 假如增加了人员
                if is_add:
                    # 假如C还有需要排的天数,则开始排班的索引就是C,否则开始排班的索引为C的后一人
                    if need_days > 0:
                        person_index = today_person_index
                        person_days = schedule_days - need_days
                    else:
                        # C的后一人索引,假如C为最后一个人,则开始排班的人索引为0
                        # person_index = userList.index(today_person) + 1 if userList.index(today_person) + 1 < len(
                        #     userList) else 0
                        # person_days = 0
                        person_index += 1
                        person_index %= len(userList)  # 防止数组越界

                    # 重新生成后面不正常的排班数

                # 假如删除了人员
                # elif is_del:
                #     if del_index == today_person_index:
                #
                #     elif del_index < today_person_index:
                #         pass
                #     else:

                date_schedule, new_person_index, new_person_days = gen_leader_schedule(userList, current_year,
                                                                                       current_month,
                                                                                       datetime.date.today() + 1,
                                                                                       person_index=person_index,
                                                                                       person_days=person_days)
                # 将信息配置覆盖到ini文件
                # configObj.add_section("init_settings")
                configObj.set("init_settings", "gen_data", f"{current_year}-{current_month}")
                # configObj.set("init_settings", "user_list", str(userList))
                configObj.set("init_settings", "schedule", str(date_schedule))
                configObj.set("init_settings", "last_person_index", str(new_person_index))
                configObj.set("init_settings", "last_person_days", str(new_person_days))
                configObj.write(open(ini_path, 'w+', encoding='utf-8'))

            # if is_del:

            # 修改和删除都要获取今天上班的人,及他前面上了多少天班,这部分为公共代码

            # schedule = configObj.get("init_settings", "schedule")  # 字符串格式需要转成字典
            # date_schedule = ast.literal_eval(schedule)

        # 如果不相等,则需要根据当前年月重新生成排班数据
        else:
            print('进入新的月份需要重新排班时----------')
            person_index = int(configObj.get("init_settings", "last_person_index"))
            person_days = int(configObj.get("init_settings", "last_person_days"))

            date_schedule, new_person_index, new_person_days = gen_leader_schedule(userList, current_year,
                                                                                   current_month,
                                                                                   person_index=person_index,
                                                                                   person_days=person_days)
            # configObj.add_section("init_settings")
            configObj.set("init_settings", "gen_data", f"{current_year}-{current_month}")
            # configObj.set("init_settings", "user_list", str(userList))
            configObj.set("init_settings", "schedule", str(date_schedule))
            configObj.set("init_settings", "last_person_index", str(new_person_index))
            configObj.set("init_settings", "last_person_days", str(new_person_days))
            configObj.write(open(ini_path, 'w+', encoding='utf-8'))

            # todo 考虑是否需要将用户列表也加到配置文件中去

    # 第一次排班,不存在配置文件,则需要生成第一次排班的日期并生成配置文件
    else:
        print('没有配置文件时--------')
        date_schedule, new_person_index, new_person_days = gen_leader_schedule(userList, startY, startM, day=startD)

        configObj.add_section("init_settings")
        configObj.set("init_settings", "gen_data", f"{current_year}-{current_month}")
        # configObj.set("init_settings", "user_list", str(userList))
        configObj.set("init_settings", "schedule", str(date_schedule))
        configObj.set("init_settings", "last_person_index", str(new_person_index))
        configObj.set("init_settings", "last_person_days", str(new_person_days))
        configObj.write(open(ini_path, 'w+', encoding='utf-8'))

        # todo 考虑是否需要将用户列表也加到配置文件中去

        # 需要把参与排班的人员存进配置文件里
