class dtool:
    daysInMonths = {
        0: 0,
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }

    daysInWeek = {
        "MONDAY":1,
        "TUESDAY":2,
        "WEDNESDAY":3,
        "THURSDAY":4,
        "FRIDAY":5,
        "SATURDAY":6,
        "SUNDAY":7
    }

    @staticmethod
    def deltaDay(beginDate, deltaTime, day):
        deltaTime = (deltaTime - (7-dtool.daysInWeek[day]))%7
        for key,value in dtool.daysInWeek.items():
            if value == deltaTime:
                return key
    @staticmethod
    def daysLeft(Date):
        daysInMonths = dtool.daysInMonths.copy()
        if Date["a"] % 4 == 0:
            daysInMonths[2]=29
        delta = daysInMonths[Date["m"]] - Date["d"]
        for i in range(Date["m"] + 1, 13):
            delta += daysInMonths[i]
        return delta

    @staticmethod
    def daysHad(Date):
        daysInMonths = dtool.daysInMonths.copy()
        delta = Date["d"]
        if Date["a"] % 4 == 0:
            daysInMonths[2]=29
        for i in range(Date["m"]):
            delta += daysInMonths[i]
        return delta

    @staticmethod
    def deltaTime(beginDate, endDate):
        deltaYear = endDate["a"] - beginDate["a"]
        if deltaYear == 0:
            return dtool.daysLeft(beginDate) - dtool.daysLeft(endDate)
        else:
            delta = dtool.daysLeft(beginDate) + dtool.daysHad(endDate)
            for i in range(1, deltaYear):
                delta += 365
                if (beginDate["a"] + i) % 4 == 0:
                    delta += 1
        return delta

    @staticmethod
    def deltAdd(beginDate, deltaTime):
        daysInMonths = dtool.daysInMonths.copy()
        Date = beginDate.copy()
        if Date["a"] % 4 == 0:
            daysInMonths[2]=29
        while deltaTime >= 365:
            Date["a"] += 1
            deltaTime -= 365
            if Date["a"] % 4 == 0:
                deltaTime -= 1
        if deltaTime + Date["d"] > daysInMonths[Date["m"]]:
            deltaTime -= daysInMonths[Date["m"]] - Date["d"]
            Date["m"] += 1
            while deltaTime > daysInMonths[Date["m"]]:
                deltaTime -= daysInMonths[Date["m"]]
                Date["m"] += 1
                if Date["m"] > 12:
                    Date["a"] += 1
                    Date["m"] = 1
                    if Date["a"] % 4 == 0:
                        daysInMonths[2]=29
                    else:
                        daysInMonths[2]=28
            Date["d"] = deltaTime
        else:
            Date["d"] += deltaTime
        return Date

    @staticmethod
    def calcEndDate(beginDate,hours,option,countd,holdayList):
        
        if option == "1":
            classDays = ["1","0","0","0","0","0","0"]
        elif option == "2":
            classDays = ["0","0","0","0","0","1","0"]
        elif option == "3":
            classDays = ["0","1","0","1","1","0","0"]
        elif option == "4":
            classDays = ["0","1","0","1","1","0","0"]
        elif option == "5":
            classDays = ["1","1","0","1","1","0","0"]

        if classDays[dtool.dayOfDate(beginDate)-1]=="1" and countd == True:
            taketd = True
            for holday in holdayList:
                if beginDate == holday:
                    taketd = False
            if taketd:
                if  "1" <= option <= "3":
                    hours -= 7       
                elif option == "4":
                    hours -= 3.5  
                elif option == "5":
                    hours -= 3

        endDate = dtool.rawEndDate(beginDate,hours,option,classDays)

        for holday in holdayList:
            if dtool.inDateRange(beginDate,dtool.dateToDict(holday),endDate,classDays,countd):
                if  "1" <= option <= "3":
                    hours += 7       
                elif option == "4":
                    hours += 3.5  
                elif option == "5":
                    hours += 3
                endDate = dtool.rawEndDate(beginDate,hours,option,classDays)
        return endDate
        
    @staticmethod
    def rawEndDate(beginDate,hours,option,classDays):
        if hours == 0:
            return beginDate
        elif option == "1":
            numSession = hours // 7
        elif option == "2":
            numSession = hours // 7
        elif option == "3":
            numSession = hours // 7
        elif option == "4":
            numSession = hours // 3.5
        elif option == "5":
            numSession = hours // 3

        deltaTime = 0
        for i in range(dtool.dayOfDate(beginDate),7):
            if numSession == 0:
                break
            elif classDays[i]=="1":
                numSession -= 1
            deltaTime += 1
        while numSession != 0:
            for i in range(7):
                if numSession == 0:
                    break
                elif classDays[i]=="1":
                    numSession -= 1
                deltaTime += 1
        return dtool.deltAdd(beginDate, deltaTime)
    
    @staticmethod
    def dayOfDate(date):
        yearDay = "MONDAY"
        deltaTime = dtool.daysHad(date)
        return dtool.daysInWeek["MONDAY"] + deltaTime % 7 - 1 if (dtool.daysInWeek["MONDAY"] + deltaTime % 7 - 1) != 0 else 7
    @staticmethod
    def inDateRange(beginDate,findDate,endDate,classDays,countd):
        if classDays[dtool.dayOfDate(findDate)-1] == "0":
            return False
        elif countd and not(dtool.daysHad(beginDate) <= dtool.daysHad(findDate) <= dtool.daysHad(endDate)):
                return False
        elif not(countd) and not(dtool.daysHad(beginDate) < dtool.daysHad(findDate) <= dtool.daysHad(endDate)):
            return False
        return True

    @staticmethod
    def countDay(beginDate,endDate,day1,day2):
        deltaTime=dtool.deltaTime(beginDate,endDate)
        deltaTime -= 7 - dtool.daysInWeek[day1]
        numdays = 0
        numdays += deltaTime // 7
        # this counts beginning day 
        if dtool.daysInWeek[day1] <= dtool.daysInWeek[day2]:
            numdays += 1

        if deltaTime % 7 >= dtool.daysInWeek[day2]:
            numdays += 1
        return numdays
    @staticmethod
    def dateToDict(Date):
        Date = Date.split("-")
        Date = [int(Date[i]) for i in range(3)]
        return {"a": Date[0], "m": Date[1], "d": Date[2]}

    @staticmethod
    def dictToDate(Date):
        return str(Date["a"])+"-"+str(Date["m"])+"-"+str(Date["d"])
    