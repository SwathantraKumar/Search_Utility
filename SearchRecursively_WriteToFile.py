#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os

#This method searches the string within the provided file.
# input - file name, and search string
# output - list of files where the search string
def searchCallFiles(fileName,search_string):
    absolutefileName = getTheFilePathFromName(fileName,'D:\swathant1_ibv1ilwin1027v_6974\depot\infolease\il\il.10.6.3.tiger\proglib')
    if absolutefileName is None:
        absolutefileName = 'Dummy'
    if os.path.exists(absolutefileName):
        fo = open(absolutefileName)
        line = 'xx'   
        while line != '':
            line = fo.readline()
            line = line.upper()
            index = line.find(search_string)
            if index != -1 :
                callFileName = getCalledProgramNameFromLine(line)
                if(isUnwanted(callFileName) or callFileName is None or (callFileName in callFileNames)) :
                    continue
                else:
                    print(callFileName)
                    callFileNames.append(callFileName)
                    callFileNames.append(searchCallFiles(callFileName,search_string))
        fo.close()
    return callFileNames

#This method gets complete path of a file
#input - name of the file, base directory like 'D:'
#output - full path of the file
def getTheFilePathFromName(fileName, baseDirectory):
    for root, dirs, files in os.walk(baseDirectory):
        if fileName in files:
            return os.path.join(root, fileName)

#This method extracts the Called file name within a line provided
#input - line of a file
#output - Name of the called program
def getCalledProgramNameFromLine(line):
    split_list = line.split('CALL ')
    for item in split_list:
        if '(' in item:
            return item.split('(')[0]

#This method checks if the file is worth searching or not
def isUnwanted(callFileName):
    localCallFileName = str(callFileName)
    localCallFileName = localCallFileName.strip()
    UnwantedCallFiles = ['IDS.READ','IDS.WRITE','IDS.MATREAD','IDS.MATWRITE','FILE.OPEN','XML.APPEND','GNM.GET.MAX.ERROR','CHNG.LOG.SUB',
                        'GNM.LOAD','XML.PARSER','GET.MSG','IF', 'IF NOT','SEARCH.CALL.STACK','GET.MSG.WEBIL', 'SOCKET.WRITE', 'OSOPEN.SUB',
                         'PCPERFORM.SUB','GNM.BUILD','BCI.EXECUTE.SELECT','SOCKET.READ','NUM.DOTS','CHECK.MSG','PRINT.MSG','API.FILE.OPEN',
                         'IDS.READV','FILE.OPEN.OK','FILE.CLOSE','BCI.GET.BPI','IDS.WRITEV','IDS.DELETE','IF ','GET.SCREEN','CMAINT.OPENS','DISPLAY.MSG',
                         'ALPHA.SEARCH','GET.WHO','ALPHA.NUM.FIELD','SOUNDEX.SUB','IDS.CLEARFILE','SDX.MENU','MLCODED.DISPLAY','LOG.ERROR','INPUT.LINE',
                         'DISPLAY.PROMPT','MLCODED.FIELD','@UATB.PGM','READ.WF','MATREAD.WF','GET.CODES','ENCRYPT.SUB','IDS.READU','SECURE.CHECK','PHANTOM.LOGON',
                         'TABLE.FIELD','RECORD.LOCK.SUB','TABLE.FIELD.INITIALIZE','ALPHA.NUM.SUB','TABLE.FIELD.SETUP','INTEGER.FIELD',
                         'DELETE.FILE.SUB','SET.COPIES','MLCODED.CHANGE','APPEND.CODES','PRINTER.SUB','SET.PRTR.LOCK','PRINT.ERROR','GET.SPOOLER.INFO','SET.SP.ASSIGN',
                         'SP.ASSIGN','GET.CURRENT.DIR','OSREAD.SUB','OS.CHG.DIR','GET.MSG','TRANSLATE.SUB','MLCODED.FORMAT','MATWRITE.WF','WRITE.WF','BREAK.KEY',
                         'INTERNAL.DATE.SUB','IDS.EXECUTE.ANSI.SQL','IDS.EXECUTE.ANSI.SQL.ERROR','IDS.MATREADU','DATE.FIELD','GET.MSG','START.TRANSACTION','COMMIT.TRANSACTION',
                         'UNLOCK.MULTIPLE.RECORDS','GET.PORT.DESC','IDS.WRITE.PARAMETER','IDS.RELEASE','IDS.DELETE.PARAMETER','CREATE.FILE.SUB','CMAINT.WORK.FILE.OPENS',
                         'GET.SYSTEM.TYPE','NJS.PRINT.ERROR','ASSET.WORK.FILE.OPENS','TRANS.START.SUB','TRANS.COMMIT.SUB','IL.WEB.ISO.TO.INTERNAL.DATE','GET.CALLING.PROGRAM','  IF ',
                         '		IF ','GNM.INIT','API.GET.PORT','XML.WELLFORMED','REMOVE.WHITESPACE','GET.FILE.INFO','CATALOG.PROGRAM','NET.LOCALGROUP','DB.CONNECT','READ.DBCONFIG',
                         'CONNECT.TO.DB','API.FE','    IF ','	IF ','PYMT.SCR.MESSAGES','ML.HEADING','BATCH.SUB','DEFAULT.SET.COPIES','ROLLBACK.TRANSACTION'
                         ]
    if (callFileName in UnwantedCallFiles) or (localCallFileName.find(' ') != -1):
        return 1
    else:
        return 0

#This method scans each line in the file for the search string and writes the searched lines onto a file
def findUsagesOfItem(fileName,SearchString,resultFile,baseProgramDirectory, resultDirectory):
    absolutefileName = getTheFilePathFromName(fileName,baseProgramDirectory)
    usages =[]
    lineNumber = 0
    if absolutefileName is None:
        absolutefileName = 'Dummy'
    if os.path.exists(absolutefileName):
        writeFileName = resultDirectory+'\Results_{}'.format(resultFile)
        fileToWrite = open(writeFileName,'w')
        fo = open(absolutefileName)
        line = 'xx'
        print('finding '+SearchString+' in '+absolutefileName)
        fileToWrite.write('finding '+SearchString+' in '+absolutefileName)
        while line != '':
            line = fo.readline()
            lineNumber += 1
            line = line.upper()
            SearchString = SearchString.upper()
            index = line.find(SearchString)
            if index != -1 :
                line ='Line Number = '+str(lineNumber) +', SearchString = '+SearchString+', File Name = '+fileName+' , and Line = '+line
                usages.append(line)
        fo.close()
        fileToWrite.close()
    return usages

#Check if passed on directory is valid.
def validateDirectory(directories):
    invalidDirectories = []
    for directory in directories:
        if os.path.exists(directory):
            pass
        else:
            invalidDirectories.append('invalid directory  - {}'.format(directory))
    return invalidDirectories


#Main execution...
callFileNames = []
callFileName = ''
StartingProgram = input('Enter the starting program : ')
filterFilesOnString = input('Enter the search string to filter the called files : ')
BaseProgramDirectory = input('Enter the base directory path to search in : ')
resultDirectory = input('Enter the result directory path to store the results : ')
searchStrings = input('Enter the search string or hit enter to do default string search : ')
if searchStrings == '':
    print('Searching default items...')
    searchStrings = ['MONTHEND.DATES','PARAM.CHNG.LOG.RECORDS','AGING.TYPE','PYMT.BATCHES','MISC.BUYOUT.SUSP.ACCT.NO','TRUE.VAL.TAX.METH','INVOICE.RUN.CODE',
                 'INVOICE.FROM.DATE','INVOICE.TO.DATE','AGING.RUN.CODE','PASTDUE.FROM.DATE','PASTDUE.TO.DATE','CURRENT.MONTH','MONTHEND.CODE','PRINT.HEADER.PAGE',
                 'LESSORS','OUTSOURCE.INSUR','RCPT.TYPE','END.PMT.GL.CODE','PYMT.SUSPENSE.ACCT.NO','ASSET.DEFAULT','BUYOUT.SUSPENSE.ACCT.NO','PREV.CURRENT.MONTH',
                 'CREDIT.LIMIT.REQUIRED','DEF.CUST.CREDIT.CODE','APP.SUSPENSE.ACCT.NO','INTERIM.GL.CODE','CASH.ACCT.NO','CORR.PYMTS.UNAPP.SUSP','UNAPP.SUSP.ACCT.NO',
                 'ACCRUAL.BILL.DUE','STATE.UT.GL.CODE','CNTY.UT.GL.CODE','CITY.UT.GL.CODE','TCNTY.UT.GL.CODE','TCITY.UT.GL.CODE','DEALER.UT.GL.CODE','DISP.OL.METHOD',
                 'INTERCO.ACCT.NO','VAR.PYMT.CODE','THIRD.PARTY.MISC.GL','SALE.LESSEE.MISC.GL','MATURITY.DAYS','CANADIAN.POST.CODE','RCPT.TIMING.CODE',
                 'PROG.PYMT.SUSP.ACCT.NO','PAYDOWN.REASON.CODE','CLOSING.DAY','MULTIPLE.CURRENCY','STARTING.DAY','RCPT.CREATION','FIELD.LEVEL.SEC','PDC.CHECK.DUP',
                 'PDC.CLR.RTN.SCR','PDC.CHECK.FEE.ENTRY','PDC.PYMT.BATCH.TIMING','PDC.COMPLETION','PDC.MANUAL.PAY.IN','CHECK.FEE.GL.CODE','REPO.WORKLISTS','PAST.DUE.RCVB',
                 'SAVE.FINANCIAL.HISTORY','RA.OUTSTANDING.BAL.CALC','ALLOW.AS.UNAPP.SUSP']
else:
    print('Searching item - {}'.format(searchStrings))

directoryList = [BaseProgramDirectory,resultDirectory]
invalidDirectoryErrors =  validateDirectory(directoryList)
if len(invalidDirectoryErrors) != 0 :
    for errorMessage in invalidDirectoryErrors:
        print(errorMessage)
    print('Exiting the program execution')
else:
    ListOfFiles = searchCallFiles(StartingProgram,filterFilesOnString)
    ListOfFiles.append(StartingProgram)
    searchResults = []
    print('Printing Search Results, please wait...')
    print('***************************************')
    for eachSearchString in searchStrings:
        for eachFile in ListOfFiles:
            usages  = findUsagesOfItem(eachFile, eachSearchString,StartingProgram,BaseProgramDirectory, resultDirectory)
            if len(usages) != 0:
                searchResults.append(findUsagesOfItem(eachFile, eachSearchString,StartingProgram,BaseProgramDirectory, resultDirectory))

    writeFileName = 'D:\Python Projects\SearchResults\Results_{}'.format(StartingProgram)
    fileToWrite = open(writeFileName,'a')
    for eachSearchedResult in searchResults:
        for each in eachSearchedResult:
            print(each)
            fileToWrite.write(each)

    fileToWrite.close()
    


# In[ ]:




