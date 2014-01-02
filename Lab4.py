# -*- coding: utf-8 -*-
import os
import pickle

#文件夹类
class Folder :
    def __init__( self, folderName = None, folderParent = None, folderContent = list() ):
        self.folderName = folderName
        self.folderParent = folderParent
        self.folderContent = folderContent

#文件类
class File :
    def __init__( self, fileName = None, fileParent = None, fileInodeNo = None ):
        self.fileName = fileName
        self.fileParent = fileParent
        self.fileInodeNo = fileInodeNo

#i节点信息类
class inodeInfo :
    def __init__ (self, totalByte = None, block = None ):
        self.totalByte = totalByte
        self.block = block


#当文件夹结构发生变化，对文件系统就行修改
def cDirectory():
    fileSysNow = open(fileSysName, 'r')
    fileSysContent = fileSysNow.read()
    fileSysNow.close()
    directoryStr = pickle.dumps(rootFolder)
    directoryLen = '00000000' + str(len(directoryStr))
    directoryLen = directoryLen[-8:]
    uselessLen = int(fileSysContent[:8])+8
    fileSysContent = directoryLen + directoryStr + fileSysContent[uselessLen:]
    fileSysNow = open(fileSysName, 'w')
    fileSysNow.write(fileSysContent)
    fileSysNow.close()

#当文件信息发生变化，对文件系统就行修改
def cInode ():
    cDirectory()
    fileSysNow = open(fileSysName, 'r')
    fileSysContent = fileSysNow.read()
    fileSysNow.close()
    inodeStr = pickle.dumps(inodeDict)
    inodeLen = '00000000' + str(len(inodeStr))
    inodeLen = inodeLen[-8:]
    directoryLen = int(fileSysContent[:8])
    uselessLen = int(fileSysContent[8+directoryLen:16+directoryLen])
    fileSysContent = fileSysContent[:8+directoryLen]+inodeLen+ inodeStr + fileSysContent[16+directoryLen+uselessLen:]
    fileSysNow = open(fileSysName, 'w')
    fileSysNow.write(fileSysContent)
    fileSysNow.close()

#新建文件系统
def newFileSys ():
    global rootFolder
    global folderNow
    global fileSysName
    global inodeDict
    fileSysName = str(orderList[1]) + '.jk'
    if fileSysName in os.listdir(os.getcwd()):      #判断是否已存在同名文件系统
        noteStr = 'Error !\n'+fileSysName + ' Exists !'
        print noteStr
    else :
        fileSysNow = open(fileSysName,'w')
        rootFolder = Folder( '/',None,list() )
        folderNow = rootFolder
        directoryStr = pickle.dumps(rootFolder)
        directoryLen = '00000000' + str(len(directoryStr))     #最多8位数字来表示字节数
        directoryLen = directoryLen[-8:]
        inodeStr = pickle.dumps(inodeDict)
        inodeLen = '00000000' + str(len(inodeStr))
        inodeLen = inodeLen[-8:]
        fileSysContent = directoryLen+ directoryStr + inodeLen+inodeStr+'\n'
        fileSysNow.write(fileSysContent)
        noteStr = 'Success! \nYou have created a new file system named '+fileSysName +' \nIt is located in '+str(os.getcwd())+' !'
        print noteStr
        fileSysNow.close()

#打开文件系统
def openFileSys ():
    global rootFolder
    global fileSysName
    global folderNow
    global inodeDict
    fileSysName = str(orderList[1]) + '.jk'
    if fileSysName in os.listdir(os.getcwd()):
        fileSysNow = open(fileSysName, 'r')
        fileSysContent = fileSysNow.read()
        fileSysNow.close()
        directoryLen = int(fileSysContent[:8])
        directoryStr = fileSysContent[8:8+directoryLen]
        rootFolder = pickle.loads(directoryStr)        #由文件系统读出目录树信息
        folderNow = rootFolder
        inodeLen = int(fileSysContent[8+directoryLen:16+directoryLen])
        inodeStr = fileSysContent[16+directoryLen:16+directoryLen+inodeLen]
        inodeDict = pickle.loads(inodeStr)             #由文件系统读出i节点信息
        noteStr = 'Success!\nYou have opened the file system named ' + fileSysName+'\nIt is located in ' +str(os.getcwd()) + '!'
        print noteStr
    else :
        noteStr = 'Error!\nThere is no file system named ' + fileSysName + '!'
        print noteStr
        fileSysName = None

#退出文件系统
def exitFileSys ():
    global fileSysName
    if fileSysName != None :
        noteStr = 'Success!\nYou have exited the file system  named ' +fileSysName+'!'
        print noteStr
        fileSysName = None
    else :
        noteStr = 'Sorry, It seems you haven\'t opened a file system !'
        print noteStr

#新建文件夹
def mkdir ():
    global rootFolder
    global fileSysName
    if fileSysName == None:
        noteStr = 'Sorry, You should open or new a file system first !'
        print noteStr
    else :
        newFolderName = orderList[1]
        flag = False
        for item in folderNow.folderContent :          #判断是否已存在同名文件夹
            if isinstance(item, Folder) and  item.folderName == newFolderName:
                flag = True
        if flag == True :
            noteStr = 'Error !\n' + newFolderName +' Exist !'
            print noteStr
        else :
            newFolder = Folder( newFolderName, folderNow, list() )
            folderNow.folderContent.append (newFolder)
            cDirectory()
            noteStr = 'Success !\nYou have created a new folder named ' + newFolderName
            print noteStr

#删除文件夹
def rmdir ():
    global fileSysName
    global rootFolder
    if fileSysName == None :
        noteStr = 'Sorry, You should open or new a file system first !'
        print noteStr
    else :
        removeFolderName = orderList[1]
        flag = False
        for item in folderNow.folderContent :
            if isinstance(item, Folder) and  item.folderName == removeFolderName:
                folderNow.folderContent.remove(item)
                noteStr = 'Success !\nYou have removed the folder named ' + removeFolderName +' !'
                print noteStr
                cDirectory()
                flag = True
                break
        if flag ==False:
            noteStr = 'No such folder named ' +removeFolderName +' !'
            print noteStr

#现实当前目录下文件及文件夹信息
def showDirectory ():
    if fileSysName == None :
        noteStr = 'Sorry, You should open or new a file system first !'
        print noteStr
    else :
        for items in folderNow.folderContent:
            if isinstance( items, Folder):
                print items.folderName +'/'
            else :
                print items.fileName

#更改当前目录
def changeDirectory ():
    global folderNow
    if fileSysName == None :
        noteStr = 'Sorry, You should open or new a file system first !'
        print noteStr
    else :
        if len(orderList) == 1:  #缺省命令表示退出到根目录
            folderNow = rootFolder
        elif orderList[1] == '..':    # .. 命令表示返回上一级目录
            if folderNow != rootFolder:
                folderNow = folderNow.folderParent
        else :
            folderInto = orderList[1]
            flag = False
            for item in folderNow.folderContent :
                if isinstance(item, Folder) and item.folderName == folderInto :
                    folderNow = item
                    flag = True
                    break
            if flag == False :
                noteStr = 'Sorry, No such folder named ' + folderInto +' !'
                print noteStr

#新建文件
def createFile ():
    global inodeDict
    global rootFolder
    if fileSysName == None :
        noteStr  = 'Sorry, You should open or new a file system first !'
        print noteStr
    else :
        newFileName = orderList[1]
        flag = False
        for item in folderNow.folderContent :   #判断是否已存在同名文件
            if isinstance(item, File) and  item.fileName == newFileName:
                flag = True
        if flag == True :
            noteStr = 'Error !\n' + newFileName +' Exist !'
            print noteStr
        else :
            fileSysNow = open(fileSysName, 'r')
            fileSysContent = fileSysNow.read()
            fileSysNow.close()
            inodeNo = max(inodeDict.keys())+1
            fileBlock = inodeDict[inodeNo - 1].block + inodeDict[inodeNo - 1].totalByte
            inodeDict[inodeNo] = inodeInfo(0, int(fileBlock))
            newFile = File(newFileName, folderNow, inodeNo)
            folderNow.folderContent.append(newFile)
            cInode()
            noteStr = 'Success !\nYou have created a new file named ' + newFileName +' !'
            print noteStr

#打开文件
def openFile ():
    global inodeNow
    fileOpenName = orderList[1]
    flag = False
    for item in folderNow.folderContent :
        if isinstance(item, File ) and item.fileName == fileOpenName :
            flag = True
            inodeNow = item.fileInodeNo
            noteStr = 'Success !\nYou have Opened the file named ' + fileOpenName +' !'
            print noteStr
            break
    if flag == False:
        noteStr = 'Error !\nNo such file named ' +fileOpenName +' !'
        print noteStr

#关闭文件
def closeFile ():
    global inodeNow
    if inodeNow == None or fileSysName == None:
        noteStr = 'Error !\nNo File Opened !'
        print noteStr
    else :
        inodeNow = None
        noteStr = 'File closed !'
        print noteStr

#读取文件内容
def readFile():
    if inodeNow == None or fileSysName == None :
        noteStr = 'Error !\nNo File Opened !'
        print noteStr
    else :
        fileTotalByte = inodeDict[inodeNow].totalByte
        fileBlock = inodeDict[inodeNow].block
        fileSysNow = open(fileSysName, 'r')
        fileSysContent = fileSysNow.read()
        fileSysNow.close()
        if len(orderList) == 1 or int(orderList[1]) >= fileTotalByte :
            fileReadStr = fileSysContent[-(fileBlock+fileTotalByte): -fileBlock]
            print fileReadStr
        elif int(orderList[1]) < 0 :
            noteStr = 'Error !\nThe byte to read need to be bigger than zero .'
            print noteStr
        else :
            fileReadStr = fileSysContent[-(fileBlock+orderList[1]):-fileBlock]
            print fileReadStr

#写文件
def writeFile ():
    global inodeDict
    global rootFolder
    if inodeNow == None or fileSysName == None :
        noteStr = 'Error !\nNo File Opened !'
        print noteStr
    else :
        print 'Please Enter the Content :'
        senWrite = ''
        while True :                   #获取写入信息
            try :
                writeStr = str(raw_input())
                senWrite = senWrite + writeStr +'\n'
            except EOFError :
                break
        modeWrite = orderList[1]
        numBlockAdd = len(senWrite)
        fileTotalByte = inodeDict[inodeNow].totalByte
        fileBlock = inodeDict[inodeNow].block
        fileSysNow = open(fileSysName, 'r')
        fileSysContent = fileSysNow.read()
        fileSysNow.close()
        fileStr = fileSysContent[-(fileBlock+fileTotalByte):-fileBlock]
        flag = True
        if modeWrite == 'begin':             #命令为 begin 时，写入信息到文件开始处
            fileStr = senWrite + fileStr
        elif modeWrite == 'end':             #命令为 end 时，写入信息到文件结尾处
            fileStr = fileStr + senWrite
        else:                                #命令为数字时，将信息写入到文件中
            try :
                modeWrite = int(modeWrite)
                if modeWrite > inodeDict[inodeNow].totalByte :
                    flag = False
                    noteStr = 'Error !\nMode Number Out of Range !'
                    print noteStr
                else :
                    fileStr = fileStr[:modeWrite] +senWrite + fileStr[modeWrite:]
            except :
                flag = False
                noteStr = 'Error !\nCheck the Mode !'
                print noteStr
        if flag == True :
            fileSysContent = fileSysContent[:-(fileBlock+fileTotalByte)] +fileStr+fileSysContent[-fileBlock :]
            fileSysNow = open(fileSysName, 'w')
            fileSysNow.write(fileSysContent)
            fileSysNow.close()
            inodeDict[inodeNow].totalByte = len(fileStr)
            for key in inodeDict.keys():
                if key > inodeNow:
                    inodeDict[key].block += numBlockAdd
            cInode()
            print 'Success !'

#删除文件
def deleteFile ():
    global fileSysName
    global rootFolder
    if fileSysName == None or fileSysName == None :
        noteStr = 'Sorry, You should open or new a file system first !'
        print noteStr
    else :
        removeFileName = orderList[1]
        flag = False
        for item in folderNow.folderContent :
            if isinstance(item, File) and  item.fileName == removeFileName:
                folderNow.folderContent.remove(item)
                noteStr = 'Success !\nYou have removed the file named ' + removeFileName +' !'
                print noteStr
                cDirectory()
                flag = True
                break
        if flag == False:
            noteStr = 'No such file named ' +removeFileName +' !'
            print noteStr

def showHelp ():
    print helpStr

#命令菜单
dispatchAction = {
    'new' : newFileSys,
    'sfs' : openFileSys,
    'exit' : exitFileSys,
    'mkdir' : mkdir,
    'rmdir' : rmdir,
    'ls' : showDirectory,
    'cd' : changeDirectory,
    'create' : createFile,
    'open' : openFile,
    'close' : closeFile,
    'read' : readFile,
    'write' : writeFile,
    'delete' : deleteFile,
    'help' : showHelp,
    }
    
welcomeStr = '------------------------------------------------------------------------------\nWelcome to use the Simple File System created by JinKe   \n\tEntry help to find some infomation\n\t    Visit jinke.me to reach me\n------------------------------------------------------------------------------'
byeStr = '------------------------------------------------------------------------------\n' + 'Goodbye !\n' + 'Visit jinke.me to Find More Infomation \n------------------------------------------------------------------------------'
helpStr = 'You can use the following command :\n'+'\tnew\tNew a File System\n'+'\tsfs\tOpen a File System\n'+'\texit\tExit a File System\n'+\
          '\tmkdir\tMake a New Folder\n'+'\trmdir\tRemove a Folder\n'+\
          '\tls\tShow Directory\n'+'\tcd\tChange Directory\n'+\
          '\tcreate\tCreate a New File\n'+'\topen\tOpen a File\n' + '\tclose\tClose a File\n'+\
          '\tread\tShow the Content of the File\n' + '\twrite\tWrite Something Into the File\n'+'\tdelete\tDelete a File\n'+\
          '\tquit\tQuit the System'

print welcomeStr


fileSysName = None
orderList = list()
inodeDict = dict()
folderNow = None
rootFolder = None
inodeNow = None
inodeDict={0 : inodeInfo(1,0)}

#获取命令输入
while True :
    try :
        orderStr = raw_input()
    except :
        print byeStr
        break
    orderList = orderStr.split( ' ' )
    for item in orderList :
        if item == '' :
            orderList.remove(item)
    if len(orderList) == 0 :
        continue
    if orderList[0] == 'quit' :
        print byeStr
        break
    
    try :
        dispatchAction.get(orderList[0])()
    except :
        print 'Error !\nCheck Your Order !'
