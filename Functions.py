import datetime
#Imported for providing file object type in functions help documentation (-> io.TextIOWrapper)
import io
import os

#Global Constants
FULLDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
TIME = ("Breakfast", "Lunch", "Dinner")

STORENAMES = ("Mini Wok", "Vegetarian Food", "Cantonese Roast Duck", "Malay BBQ", "KFC")
IMGNAMES = ("MiniWok", "Vegetarian", "Cantonese", "MalayBBQ", "KFC")


def OpenFile(sFileName : str) -> io.TextIOWrapper:
    # Code done by Chua Zhi Loon James
    '''Check whether file exists in directory before opening'''
    
    if os.path.exists(sFileName):
        return open(sFileName)

    print(sFileName + " cannot be found!")
    return None


def VerifyFile(cFile : io.TextIOWrapper) -> bool:
    # Code done by Chua Zhi Loon James
    '''To verify text files that are supposed to work with the program'''
    
    #Strip to remove newline at the end
    return cFile.readline().strip() == "Northspine Canteen Directory"


def GetDataLine(sFileLine : str) -> list:
    # Code done by Chua Zhi Loon James
    '''Split a file line into a list of items based on the tab separator'''

    #The file lines have been added with extra spaces for better look, need to strip them off
    return [sItem.strip() for sItem in sFileLine.split("\t")]


def VerifyWaitingTime(sWaitingTime : str) -> bool:
    # Code done by Chua Zhi Loon James
    '''To verify that the waiting times in database file are valid'''

    lWaitingTime = sWaitingTime.split()

    try:
        if len(lWaitingTime) != 2 or lWaitingTime[1] not in ("min", "mins"):
            raise ValueError
        
        nWaitingTime = int(lWaitingTime[0])
        return True
        
    except ValueError:
        return False


def VerifyPrice(sPrice : str) -> bool:
    # Code done by Chua Zhi Loon James
    '''To verify the prices in database file are valid'''
    
    try:
        if sPrice[0] != "$":
            raise ValueError
        
        fPrice = float(sPrice[1:])
        return True
    
    except ValueError:
        return False


def VerifyDayTime(sDayTime : str) -> bool:
    # Code done by Chua Zhi Loon James
    '''To verify the days and times in database file are valid'''

    if sDayTime == "All_Day":
        return True

    lDayTime = sDayTime.split("_")

    if len(lDayTime) not in (1, 2):
        return False
    
    lCheckList = TIME if lDayTime[0] in TIME else DAYS
    
    for sIndividualDayTime in lDayTime:
        if sIndividualDayTime not in lCheckList:
            return False

    return True


def DataBase(sFileName : str) -> dict:
    # Code done by Sean Dai Yun Shan
    '''Read from menu database file and store into a dictionary format {(Store1, WaitingTime1): {Food1: (Price, Time, Day), Food2: (Price, Time, Day), ...}
                                                                        (Store2, WaitingTime2): ... }'''

    dDataBase = {}
    tStoreKey = None

    cDataFile = OpenFile(sFileName)

    if not cDataFile:
        return dDataBase

    if not VerifyFile(cDataFile):
        print("Invalid File Format!")
        return dDataBase
        
    for sFileLine in cDataFile:
        lData = GetDataLine(sFileLine)

        #To check it is not currently on an empty line
        if lData[0]:
            #The whole store is not added if this line is not in the correct format
            if lData[0] == "Store:":
                #Verify store line is in correct format
                if len(lData) == 6 and VerifyWaitingTime(lData[2]) and lData[3] == "Price" and lData[4] == "Time" and lData[5] == "Day":
                    tStoreKey = (lData[1], int(lData[2].split()[0]))
                        
                    if tStoreKey not in dDataBase:
                        dDataBase[tStoreKey] = {}

            elif tStoreKey:
                #Verify food item line is in correct format
                if len(lData) == 4 and VerifyPrice(lData[1]) and VerifyDayTime(lData[2]) and VerifyDayTime(lData[3]):
                    dDataBase[tStoreKey][lData[0]] = (float(lData[1][1:]), lData[2], lData[3])
                else:
                    print("Invalid Line in File: " + sLine)
                    
        else:
            #To prevent items added to the wrong store in case the next store is not registered properly
            tStoreKey = None
                
    cDataFile.close()
    return dDataBase


def VerifyTime(sTime : str) -> bool:
    # Code done by Chua Zhi Loon James
    '''To verify the times in operating hours file are valid'''

    if sTime == "Not Operating":
        return True

    #Properly dissect the time components into a list
    lTimeComponents = sTime.split(":")
    lTimeComponents = [lTimeComponents[0]] + lTimeComponents[1].split()

    #Verify the time is in correct format
    if len(lTimeComponents) == 3 and lTimeComponents[2] in ("AM", "PM"):
        #Try to convert hours and minutes into integers
        try:
            if 0 <= int(lTimeComponents[0]) <= 12 and 0 <= int(lTimeComponents[1]) <= 59:
                return True
                
        except ValueError:
            pass

    return False


def GetTimeFromFile(sTime : str) -> tuple:
    # Code done by Chua Zhi Loon James
    '''Convert times in operating hours file into a tuple (Hour, Minutes, Seconds)'''

    #Properly dissect the time components into a list
    lTimeComponents = sTime.split(":")
    lTimeComponents = [int(lTimeComponents[0])] + lTimeComponents[1].split()

    #Add 12 to hour if PM, add 12 when hour is 12 so that 12 AM and 12 PM corresponds to 0 and 12 hours respectively
    return ((lTimeComponents[0] + (0 if lTimeComponents[2] == "AM" else 12) + (12 if lTimeComponents[0] == 12 else 0)) % 24, int(lTimeComponents[1]), 0 if lTimeComponents[1][1] == "0" else 59)

    
def OperatingHours(sFileName : str) -> dict:
    # Code done by Sean Dai Yun Shan
    '''Read from operating hours file and store into a dictionary format {(Store1, Store2, ...): {Day or Time: (StartTime, EndTime), ...
                                                                          (Store3, ...): ...}'''
    
    dOperatingHours = {}
    tStores = None

    cDataFile = OpenFile(sFileName)

    if not cDataFile:
        return dOperatingHours

    if not VerifyFile(cDataFile):
        print("Invalid File Format!")
        return dOperatingHours

    for sFileLine in cDataFile:
        lData = GetDataLine(sFileLine)

        #To check it is not on an empty line
        if lData[0]:
            #The whole list of stores will not be added if this line is not in the correct format
            if lData[0] == "Store:":
                #Verify that there is at least one store
                if len(lData) > 1:
                    tStores = tuple(lData[nIndex] for nIndex in range(1, len(lData)))

                    if tStores not in dOperatingHours:
                        dOperatingHours[tStores] = {}

            elif tStores:
                #Verify line is in correct format
                if len(lData) in (2, 3) and VerifyDayTime(lData[0]) and VerifyTime(lData[1]) and (VerifyTime(lData[2]) if len(lData) == 3 else True):
                    lData[0] = lData[0].split("_")
                    
                    lCheckList = TIME if lData[0][0] in TIME else DAYS
                        
                    nStartIndex = lCheckList.index(lData[0][0])
                    #To prevent index accessing error in case of only one item
                    nEndIndex = nStartIndex if len(lData[0]) == 1 else lCheckList.index(lData[0][1])

                    #To add multiple entries with the same timings or just one entry
                    while True:
                        if lData[1] == "Not Operating":
                            dOperatingHours[tStores][lCheckList[nStartIndex]] = lData[1]
                        else:
                            dOperatingHours[tStores][lCheckList[nStartIndex]] = (GetTimeFromFile(lData[1]), GetTimeFromFile(lData[2]))

                        if nStartIndex == nEndIndex:
                            break

                        #Loop through the list back from the start or increment index
                        nStartIndex = 0 if nStartIndex == len(lCheckList) else nStartIndex + 1
        else:
            #To prevent items added to the wrong store list in case the next store list is not registered properly
            tStores = None
                    
    cDataFile.close()
    return dOperatingHours


def GetOHString(sFileName : str) -> str:
    # Code done by Chua Zhi Loon James
    '''Read from operating hours file and store into a string format for display'''

    sOHString = ""

    bStoresExist = False

    cDataFile = OpenFile(sFileName)

    if not cDataFile:
        return sOHString

    if not VerifyFile(cDataFile):
        print("Invalid File Format!")
        return sOHString

    for sFileLine in cDataFile:
        lData = GetDataLine(sFileLine)

        #To check it is not on an empty line
        if lData[0]:
            if lData[0] == "Store:":
                #Verify that there is at least one store
                if len(lData) > 1:
                    bStoresExist = True
                    sOHString += "\n"
                    
                    for nIndex in range(1, len(lData)):
                        sOHString += lData[nIndex] + (", " if nIndex != len(lData) - 1 else "")

                    sOHString += "\n"

            elif bStoresExist:
                #Verify line is in correct format
                if len(lData) in (2, 3) and VerifyDayTime(lData[0]) and VerifyTime(lData[1]) and (VerifyTime(lData[2]) if len(lData) == 3 else True):
                    lData[0] = lData[0].split("_")

                    if lData[0][0] in DAYS:
                        sLine = FULLDAYS[DAYS.index(lData[0][0])] + (" - " + FULLDAYS[DAYS.index(lData[0][1])] if len(lData[0]) == 2 else "")

                        #To pad the line with spaces so display is neater
                        sLine += " " * (22 - len(sLine)) + "|  " + lData[1] + (" - " + lData[2] if len(lData) == 3 else "") + "\n"

                        sOHString += sLine
                        
        else:
            #To prevent items added to the wrong store list in case the next store list is not registered properly
            bStoresExist = False
                    
    cDataFile.close()
    return sOHString


def FormatPriceToStr(fPrice : float) -> str:
    # Code done by Chua Zhi Loon James
    '''To format the price with two decimal places'''

    sPrice = "$" + str(fPrice)
    
    if sPrice.index(".") == len(sPrice) - 2:
        sPrice += "0"

    return sPrice
    

def GetFullMenu(dDataBase : dict) -> dict:
    # Code done by Chua Zhi Loon James
    '''Obtain the full menu in the database'''
    
    dFullMenu = {}
    
    for tStoreKey, dStoreMenu in dDataBase.items():
        if tStoreKey[0] not in dFullMenu:
            dFullMenu[tStoreKey[0]] = {}

        for sFood, tFoodData in dStoreMenu.items():
            dFullMenu[tStoreKey[0]][sFood] = FormatPriceToStr(tFoodData[0])

    return dFullMenu


def CheckDayInRange(sDay : str, sDaysRange : str) -> bool:
    # Code done by Chua Zhi Loon James
    '''Check given day is inside the range of days'''

    lDaysRange = sDaysRange.split("_")

    nStartIndex = DAYS.index(lDaysRange[0])
    #To prevent index accessing error in case of only one item
    nEndIndex = nStartIndex if len(lDaysRange) == 1 else DAYS.index(lDaysRange[1])

    while True:
        if sDay == DAYS[nStartIndex]:
            return True

        if nStartIndex == nEndIndex:
            return False

        #Loop through the list back from the start to include days after sunday for the checking range
        nStartIndex = 0 if nStartIndex == len(DAYS) else nStartIndex + 1
            

def ConvertTimeToSeconds(tTime : tuple) -> int:
    # Code done by Chua Zhi Loon James
    '''Convert tuple (Hour, Minutes, Seconds) to integer seconds for easy comparison'''

    return 3600 * tTime[0] + 60 * tTime[1] + tTime[2]


def CheckTimeInRange(tTime : tuple, tTimesRange : tuple) -> bool:
    # Code done by Chua Zhi Loon James
    '''Check given time is inside the start and end timings'''

    return ConvertTimeToSeconds(tTimesRange[0]) <= ConvertTimeToSeconds(tTime) <= ConvertTimeToSeconds(tTimesRange[1])


def CheckFoodAvailableAtDayTime(dStoreOperatingHours : dict, tFoodData : tuple, tDayTime : tuple) -> bool:
    # Code done by Chua Zhi Loon James
    '''Check that the food is available on the day and time'''

    if CheckDayInRange(tDayTime[0], tFoodData[2]) and CheckTimeInRange(tDayTime[1], dStoreOperatingHours[tDayTime[0]]):
        if tFoodData[1] == "All_Day":
            return True

        lTimesRange = tFoodData[1].split("_")
        for sIndividualTime in lTimesRange:
            if CheckTimeInRange(tDayTime[1], dStoreOperatingHours[sIndividualTime]):
                return True

    return False


def GetMenuByDayTime(dDataBase : dict, dOperatingHours : dict, tDayTime : tuple) -> dict:
    # Code done by Chua Zhi Loon James
    '''Obtain the menu in the database by day and time'''

    dMenu = {}

    for tStoreKey, dStoreMenu in dDataBase.items():
        for tStores in dOperatingHours:
            if tStoreKey[0] in tStores:
                break
        
        for sFood, tFoodData in dStoreMenu.items():
            if CheckFoodAvailableAtDayTime(dOperatingHours[tStores], tFoodData, tDayTime):
                if tStoreKey[0] not in dMenu:
                    dMenu[tStoreKey[0]] = {}

                dMenu[tStoreKey[0]][sFood] = FormatPriceToStr(tFoodData[0])

    return dMenu


def CalculateWaitingTime(dDataBase : dict, nNumberOfPeople : int, sStoreName : str) -> str:
    # Code done by Chua Zhi Loon James
    '''To calculate the waiting time for each store based on number of people already queueing'''

    nWaitingTime = 0
    
    for tStoreKey in dDataBase:
        if sStoreName == tStoreKey[0]:
            nWaitingTime = nNumberOfPeople * tStoreKey[1]
            break

    return str(nWaitingTime) + " mins"


def GetDayTime(sDateTime : str) -> tuple:
    # Code done by Chua Zhi Loon James
    '''To convert datetime of string "YYYY-MM-DD HH:MM:SS" into a tuple format (Day, (Hour, Minutes, Seconds))'''

    #Properly dissect the dates and times
    lDateTime = sDateTime.split()
    lDateTime = lDateTime[0].split("-") + lDateTime[1].split(":")

    lDateTime = [int(sItem) for sItem in lDateTime]

    return (DAYS[datetime.date(lDateTime[0], lDateTime[1], lDateTime[2]).weekday()], (lDateTime[3], lDateTime[4], lDateTime[5]))



