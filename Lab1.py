
class Proceed :

    def __init__(self, proceedNum = None, timeArrived = None, timeRun = None, level = None, slot = None, numArrived = None, timeBegin = None, timeEnd = None) :
        self.proceedNum = proceedNum
        self.timeArrived = timeArrived
        self.timeRun = timeRun
        self.level = level
        self.slot = slot
        self.numArrived = numArrived
        self.timeBegin = timeBegin
        self.timeEnd = timeEnd

def FCFS(NowList):
    timeNow = 0
    ordered = 1
    for items in NowList :
        if items.timeArrived > timeNow :
            timeNow = items.timeArrived
        items.timeBegin = timeNow
        items.timeEnd = timeNow + items.timeRun
        timeNow = items.timeEnd
        proceedStr = str(ordered) + '/' + str(items.proceedNum) + '/' + str(items.timeBegin) + '/' + str(items.timeEnd) + '/' + str(items.level)
        print proceedStr
        ordered += 1

def SJF(NowList):
    RunList = list()
    RunList.append(NowList[0])
    del NowList[0]
    timeNow = 0
    if RunList[0].timeArrived > timeNow :
        timeNow  = RunList[0].timeArrived
    RunList[0].timeBegin = timeNow
    RunList[0].timeEnd = timeNow + RunList[0].timeRun
    timeNow = RunList[0].timeEnd
    proceedStr = str(1) + '/' + str(RunList[0].proceedNum) + '/' + str(RunList[0].timeBegin) + '/' + str(RunList[0].timeEnd) + '/' + str(RunList[0].level)
    print proceedStr
    RunList = RunList [:0]
    ordered = 2
    while (len(NowList)):
        for items in NowList:
            if items.timeArrived > timeNow:
                break
            RunList.append(items)
        for items in RunList :
            NowList.remove(items)
        sortList = [[item.timeRun,item.numArrived,item] for item in RunList]
        sortList.sort()
        RunList_order = [item[2] for item in sortList]
        for items in RunList_order:
            items.timeBegin = timeNow
            items.timeEnd = timeNow + items.timeRun
            timeNow = items.timeEnd
            proceedStr = str(ordered) + '/' + str(items.proceedNum) + '/' + str(items.timeBegin) + '/' + str(items.timeEnd) + '/' + str(items.level)
            print proceedStr
            ordered += 1
        RunList = RunList [:0]
            
def SRTF(NowList):
    allTimeBegin = NowList[0].timeArrived
    timeNow = allTimeBegin
    ordered = 1
    numAll = len(NowList)
    num = 0
    RunList = list()
    deleteList = list()
    proceedNow = None
    while num < numAll :
        for items in NowList :
            if items.timeArrived <= timeNow :
                RunList.append(items)
                deleteList.append(items)
        for items in deleteList :
            NowList.remove(items)
        deleteList = deleteList[:0]
        sortList = [[item.timeRun, item.timeArrived,item.proceedNum, item] for item in RunList]
        sortList.sort()
        RunList = [ item[3] for item in sortList]
        if timeNow == allTimeBegin :
            proceedNow = RunList[0]
            proceedNow.timeBegin = timeNow
        elif RunList[0] != proceedNow :
            if proceedNow.timeRun != -1 :
               proceedStr = str(ordered) +'/'+ str(proceedNow.proceedNum) +'/'+ str(proceedNow.timeBegin) +'/'+ str(timeNow) +'/'+ str(proceedNow.level)
               print proceedStr
               ordered += 1
            else :
                timeNow -= 1

            proceedNow = RunList[0]
            proceedNow.timeBegin = timeNow
        elif proceedNow.timeRun == 0:
            proceedStr = str(ordered) +'/'+ str(proceedNow.proceedNum) +'/'+ str(proceedNow.timeBegin) +'/'+ str(timeNow) +'/'+ str(proceedNow.level)
            print proceedStr
            RunList.remove(proceedNow)
            ordered += 1
            num += 1

        timeNow += 1
        proceedNow.timeRun -= 1


def RR(NowList):
    timeNow = NowList[0].timeArrived
    ordered = 1
    numAll= len(NowList)
    num = 0
    RunList = list()
    deleteList = list()
    appendList = list()
    flag = 1
    while num< numAll:
        if len(NowList) != 0 and timeNow >= NowList[0].timeArrived:
            for items in NowList :
                if items.timeArrived <= timeNow :
                    RunList.append(items)
                    deleteList.append(items)
            for items in deleteList :
                NowList.remove(items)
            deleteList = deleteList [:0]

        RunList.extend(appendList)

        if len(NowList) != 0 and len(appendList) == 0 and timeNow < NowList[0].timeArrived and ordered != 1:
            timeNow = NowList[0].timeArrived
            continue
        appendList = appendList[:0]
        
        for items in RunList :
            if items.timeRun > items.slot:
                proceedStr = str(ordered) + '/' + str(items.proceedNum) + '/' +str(timeNow) +'/'+ str(timeNow+items.slot) +'/' +str(items.level)
                print proceedStr
                timeNow += items.slot
                items.timeRun -= items.slot
                appendList.append(items)
                ordered += 1
            else :
                proceedStr = str(ordered) +'/' + str(items.proceedNum) +'/' +str(timeNow) +'/'+ str(timeNow + items.timeRun) +'/' + str(items.level)
                print proceedStr
                timeNow += items.timeRun
                num += 1
                ordered += 1
        RunList = RunList[:0]
            

def DPS(NowList):
    timeNow = NowList[0].timeArrived
    ordered = 1
    RunList = list()
    numAll = len(NowList)
    num = 0
    deleteList = list()
    while num < numAll :
        for items in NowList:
            if items.timeArrived <= timeNow:
                if items.timeArrived < timeNow and items.level > 0 :
                    items.level -= 1
                RunList.append(items)
                deleteList.append(items)
        for items in deleteList :
            NowList.remove(items)
        deleteList = deleteList[:0]

        sortList = [[item.level,item.timeArrived,item.proceedNum,item] for item in RunList]
        sortList.sort()
        RunList = [item[3] for item in sortList]
        
        RunList[0].timeBegin = timeNow
        RunList[0].level += 3
        if RunList[0].timeRun <= RunList[0].slot:
            proceedStr = str(ordered) +'/'+ str(RunList[0].proceedNum) +'/'+ str(timeNow) +'/'+ str(timeNow+RunList[0].timeRun) +'/'+ str(RunList[0].level)
            print proceedStr
            timeNow += RunList[0].timeRun
            ordered += 1
            num += 1
            del RunList[0]
        else :
            proceedStr = str(ordered) +'/'+ str(RunList[0].proceedNum) +'/'+ str(timeNow) +'/'+ str(timeNow+RunList[0].slot) +'/'+ str(RunList[0].level)
            print proceedStr
            timeNow += RunList[0].slot
            ordered += 1
            RunList[0].level += 1
            RunList[0].timeRun -= RunList[0].slot
        for items in RunList:
            if items.level >0 :
                items.level -= 1
        if len(RunList) == 0 and len(NowList) != 0 and timeNow < NowList[0].timeArrived:
            timeNow = NowList[0].timeArrived

dispatchAction = {
    1 : FCFS,   
    2 : SJF,      
    3 : SRTF,   
    4 : RR,     
    5 : DPS,   
    }

dispatch = int( raw_input() )
proceedList = list()
numArrived = 1
proceedStr = raw_input()
while True:
    value = proceedStr.split('/')
    newProceed = Proceed (int(value[0]), int(value[1]), int(value[2]), int(value[3]), int(value[4]), int(numArrived))
    numArrived += 1
    proceedList.append(newProceed)
    try:
        proceedStr = raw_input()
    except EOFError :
        break
sortList = [[item.timeArrived,item.numArrived,item] for item in proceedList]
sortList.sort()
NowList = [item[2] for item in sortList]
dispatchAction.get(dispatch)(NowList)
