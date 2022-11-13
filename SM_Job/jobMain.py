from jobCalender import jobCalender
from jobManager import jobManager

if __name__ == '__main__':
    print("\n\n\n")
    calenderObj = jobCalender()

    calenderObj.SetStartTime(2022, 11, 5)
    resData = calenderObj.Start()
    print(f"-----------\n2022 11:\n{resData}")

    userList = ["A", "B", "C"]
    jobM = jobManager(userList=userList, monthData=resData)

    jobM.SetScheduleDays(7)
    jobM.Set()
    jobM.ShowData()
    # print(jobM)

    #/////////////////////

    calenderObj.SetStartTime(2022, 12)
    resData = calenderObj.Start()
    print(f"-----------\n2022 12:\n{resData}")

    #jobM = jobManager(userList=userList, monthData=resData)
    jobM.SetData(userList=userList, monthData=resData)
    personIndex = jobM.GetCurrentPersonIndex()
    jobM.Set(personIndex)
    jobM.ShowData()
    # print(jobM)


    # calenderObj.SetStartTime(2022, 12)
    # resData = calenderObj.Start()
    # print(f"resData:\n{resData}")
    #
    #
    # calenderObj.SetStartTime(2022, 13)
    # resData = calenderObj.Start()
    # print(f"resData:\n{resData}")

