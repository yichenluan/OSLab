class Proceed :
    def __init__(self, orderNum = None, proceedNum = None, actionNum = None, volume = None):
        self.orderNum = orderNum
        self.proceedNum = proceedNum
        self.actionNum = actionNum
        self.volume = volume

def printAns(ramList, orderedNum):
    ansStr = str(orderedNum)
    addressNow = 0
    for items in ramList:
        if items[0] == None :
            proStr = '/'+str(addressNow) +'-'+str(addressNow + items[1] -1)+'.0'
        else :
            proStr = '/' +str(addressNow) + '-' + str(addressNow + items[1]-1)+'.1.'+str(items[0])
        addressNow += items[1]
        ansStr += proStr
    print ansStr
        
def merge (ramList):
    index = 0
    while index < len(ramList) - 1:
        if ramList[index][0] == None and ramList[index+1][0] == None:
            ramList[index+1][1] += ramList[index][1]
            del ramList[index]
        else :
            index += 1

def deletePro(ramList):
        for ram in ramList :
            if ram[0] == items.proceedNum :
                if ram[1] - items.volume == 0:
                    ramList.insert(ramList.index(ram), [None, items.volume])
                    ramList.remove(ram)
                else :
                    ramList.insert(ramList.index(ram), [None, items.volume])
                    ram[1] -= items.volume
                break

def FirstFit(proceedList, ramList) :
    global items
    for items in proceedList :
        orderedNum = items.orderNum
        if items.actionNum == 1:
            for ram in ramList :
                if ram[0] == None and ram[1] >= items.volume :
                    ramList.insert(ramList.index(ram) , [items.proceedNum, items.volume])
                    if ram[1] - items.volume == 0:
                        ramList.remove(ram)
                    else :
                        ram[1] -= items.volume
                    break
            printAns(ramList, orderedNum)
        else :
            deletePro(ramList)
            merge(ramList)
            printAns(ramList, orderedNum)
                
def BestFit(proceedList, ramList) :
    global items
    for items in proceedList :
        BestRam = 9999999
        indexNum = None 
        orderedNum = items.orderNum
        if items.actionNum == 1:
            for ram in ramList :
                if ram[0] == None and ram[1] >= items.volume and ram[1] < BestRam :
                    BestRam = ram[1]
                    indexNum = ramList.index(ram)
            if indexNum != None:
                ramList.insert(indexNum, [items.proceedNum, items.volume])
                if ramList[indexNum+1][1] - items.volume == 0 :
                    del ramList[indexNum+1]
                else :
                    ramList[indexNum+1][1] -= items.volume
            printAns(ramList, orderedNum)
        else :
            deletePro(ramList)
            merge(ramList)
            printAns(ramList, orderedNum)


def WorstFit(proceedList, ramList) :
    global items
    for items in proceedList :
        WorstRam = 0
        indexNum = None
        orderedNum = items.orderNum
        if items.actionNum == 1:
            for ram in ramList :
                if ram[0] == None and ram[1] >= items.volume and ram[1] > WorstRam :
                    WorstRam = ram[1]
                    indexNum = ramList.index(ram)
            if indexNum != None:
                ramList.insert(indexNum, [items.proceedNum, items.volume])
                if ramList[indexNum +1][1] - items.volume == 0:
                    del ramList[indexNum+1]
                else :
                    ramList[indexNum +1][1] -= items.volume
            printAns(ramList, orderedNum)
        else:
            deletePro(ramList)
            merge(ramList)
            printAns(ramList, orderedNum)
    
dispatchAction = {
    1 : FirstFit,
    2 : BestFit,
    3 : WorstFit
    }

dispatch = int(raw_input())
ramSize = int(raw_input())
proceedStr = raw_input()

proceedList = list()
global ramList
ramList = [[None,ramSize]]

while True :
    value = proceedStr.split('/')
    newProceed = Proceed(int(value[0]), int(value[1]), int(value[2]), int(value[3]))
    proceedList.append(newProceed)
    try :
        proceedStr = raw_input()
    except EOFError :
        break

dispatchAction.get(dispatch)(proceedList, ramList)
