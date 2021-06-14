from mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import json
import pandas as pd
import mysql
import csv

FL = 0
YEAR = 1
DATE = 2
LOC = 3
SEX = 4
AGE = 5
PUP = 6
NEWMARK = 7
MARK = 8
MARKPOS = 9
NEWTAG = 13
TAG1 = 14
TAGPOS = 15
NEWTAG2 = 16
TAG2 = 17
TAG2POS = 18
MOLT = 19
SEASON = 20
STLENGTH = 21
CRVLENGTH = 22
AXGIRTH = 23
MASS = 24
TARE = 25
MASSTARE = 26
RANGE = 29
COMMENTS = 30

def makeConnection():
    try:
        print("HELO")
        cnx = mysql.connector.connect(user='root',
                                        password='STr1pes250**',
                                        host='localhost',
                                        database='History')
        print("YO")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return cnx

## takes a table name to search, a value, and a column to find it in
## searches table and returns true if found
#def canFind(cursor, tableName, value, column):
#    check = "SELECT * FROM " + tableName + ";"
#    cursor.execute(check)
#    remaining_rows = cursor.fetchall()
#
#    if any(row[column] == value for row in remaining_rows):
#        return True # This is a resight
#    return False
#
## puts NULL where there is empty space and puts "'" around string values
#def swapNulls(row):
#    for index in range(len(row)):
#        if (row[index] == ""):
#            row[index] = "NULL"
#        elif (index not in [YEAR, DATE, MOLT, SEASON,
#            STLENGTH, CRVLENGTH, AXGIRTH, MASS, TARE, MASSTARE]):
#            row[index] = "'" + row[index] + "'"
#    # print row
#
def getTopObsv(cursor):
    statement = "SELECT * FROM Captor;"
    result = runQuery(cursor, statement)
    row = cursor.fetchone()
    print(row)

#def getTopMeasurement(cursor):
#    statement = "SELECT MAX(MeasurementID) FROM Measurements;"
#    result = runQuery(cursor, statement)
#    row = cursor.fetchone()
#    if row[0] is None:
#        return 0
#    else:
#        return int(row[0])
#
#def getDate(date):
#    print date
#    datetime_object = datetime.strptime(date, "%m/%d/%Y")
#    return datetime_object.date()
#
#def writeObsv(cnx, cursor, row, ID):
#    statement = ("INSERT INTO Observations VALUES ("
#                + str(ID) + ", "
#                + "'testEmail', "     # email
#                + row[SEX] + ", '"                # gender
#                + str(getDate(row[DATE]))+ "', "                # date
#                + row[MOLT] + ", '"                # molt
#                + row[COMMENTS].replace("'", "") + "', "                # comments
#                + row[AGE] + ", "                # Age
#                + row[YEAR] + ", "                # year
#                + row[LOC] + ", 1)")              # SLOCode
#    print(statement)
#    try:
#        cursor.execute(statement)
#        cnx.commit()
#    except mysql.connector.Error as err:
#        print(err)
#        return -5
#
#def pushQuery(cnx, cursor, query):
#    try:
#        print(query)
#        row = cursor.execute(query)
#        cnx.commit()
#    except mysql.connector.Error as err:
#        print(err)
#        exit(1)
#
def runQuery(cursor, query):
    try:
        print(query)
        cursor.execute(query)
    except mysql.connector.Error as err:
        print(err)
        exit(1)

## takes cursor and tag to look for
## returns obsID if found, -1 if not found
#def getMark(cursor, mark, year):
#    # print("mark, {:s} year {:s}".format(mark, year))
#    query = "SELECT MarkSeal FROM Marks WHERE Mark = {:s} and Year = {:s};".format(mark, year)
#    runQuery(cursor, query)
#    row = cursor.fetchone()
#    # print("getMark: ", row, mark)
#    if (row is None):
#        return -1
#    else:
#        return int(row[0])
#
#def addMark(cnx, cursor, row, ID, sealID):
#    pushMark(cnx, cursor, row, ID, sealID)
#    query = "SELECT MAX(MarkID) FROM Marks;"
#    runQuery(cursor, query)
#    row = cursor.fetchone()
#    markid = row[0]
#    observeMark(cnx, cursor, markid, ID)
#
#def observeMark(cnx, cursor, mark, ID):
#    statement = "INSERT INTO ObserveMarks VALUES ({:d}, {:d});".format(ID, mark)
#    pushQuery(cnx, cursor, statement)
#
## takes an observation from which to make a new mark
## updates table with the new mark, with error checks
#def pushMark(cnx, cursor, csvRow, obsID, sealID):
#    MARK    = 8
#    MARKPOS = 9
#    YEAR    = 1
#    statement = ("INSERT INTO Marks VALUES ("
#                + str(0) + ", "       # MarkID
#                + csvRow[MARK].replace(" ", "") + ", "        # mark
#                + csvRow[MARKPOS] + ", '"          # Year
#                + str(getDate(csvRow[2]))+ "', "          # date
#                + csvRow[YEAR] + ", "
#                + str(sealID) + ");")        #
#    print(statement)
#    try:
#        cursor.execute(statement)
#        cnx.commit()
#    except mysql.connector.Error as err:
#        print(err)
#        exit(1)
#
## returns obsID if found, -1 if not found
#def getTag(cursor, tag):
#    query = "SELECT TagSeal, TagNumber FROM Tags WHERE TagNumber = {:s}".format(tag)
#    runQuery(cursor, query)
#    row = cursor.fetchone()
#    print("getTag: ", row)
#    if (row is None):
#        return -1
#    else:
#        return int(row[0])
#
#
#def addTag(cnx, cursor, row, whichTag, obsID, sealID):
#    pushTag(cnx, cursor, row, whichTag, sealID)
#    tag = row[whichTag]
#    observeTag(cnx, cursor, tag, obsID)
#
#def observeTag(cnx, cursor, tag, ID):
#    getNewOTAG = "SELECT MAX(OTAG_ID) FROM ObserveTags;"
#    runQuery(cursor, getNewOTAG)
#    row = cursor.fetchone()
#    if(row[0] is not None):
#        OTAG_ID = int(row[0]) + 1
#    else:
#        OTAG_ID = 0
#    statement = "INSERT INTO ObserveTags VALUES ({:d}, {:d}, {:s});".format(OTAG_ID, ID, tag)
#    pushQuery(cnx, cursor, statement)
#
#def getColor(tag):
#    print ("tag: ", tag)
#    if tag == 'G':
#        return "'green'"
#    elif tag == "W":
#        return "'white'"
#    elif tag == "B":
#        return "'blue'"
#    elif tag == "Y":
#        return "'yellow'"
#    elif tag == "R":
#        return "'red'"
#    elif tag == "P":
#        return "'pink'"
#    elif tag == "V":
#        return "'violet'"
#    elif tag == "O":
#        return "'orange'"
#    else:
#        return "'unknown'"
#
## takes an observation from which to make a new mark
## updates table with the new mark, with error checks
#def pushTag(cnx, cursor, csvRow, whichTag, sealID):
#    TAGPOS  = 9
#    # print("pushTag {:s}".format(csvRow[2]))
#    print ("getColor: {:s}".format(getColor(csvRow[whichTag][0])))
#
#    statement = ("INSERT INTO Tags VALUES ("
#                + csvRow[whichTag] + ", "        # mark
#                + getColor(csvRow[whichTag][1]) + ", "          # TODO write getTagColor(row[whichTag][0])
#                + csvRow[TAGPOS] + ", '"
#                + str(getDate(csvRow[2])) + "', "
#                + str(sealID) + ");")        #
#    print(statement)
#    try:
#        cursor.execute(statement)
#        cnx.commit()
#    except mysql.connector.Error as err:
#        print(err)
#        exit(1)
#
#def pushMeasurement(cnx, cursor, obsID, row):
#    newID = getTopMeasurement(cursor) + 1
#
#    statement = "INSERT INTO Measurements VALUES ({:d}, {:d}, {:s}, {:s}, {:s}, {:s}, {:s});".format(newID, obsID,
#            row[AXGIRTH], row[MASS], row[TARE], row[CRVLENGTH], row[STLENGTH])
#    pushQuery(cnx, cursor, statement)
#
#def dropSeal(cnx, cursor, ID):
#    statement = "DELETE FROM Seals WHERE Seals.SealID = {:d};".format(ID)
#    pushQuery(cnx, cursor, statement);
#
#def updateMark(cnx, cursor, markID, newSeal):
#    statement = ("UPDATE Marks SET "
#            + "MarkSeal = {:d} WHERE MarkSeal = {:d};").format(newSeal, markID)
#    pushQuery(cnx, cursor, statement);
#
#def updateTag(cnx, cursor, tag, newSeal):
#    statement = ("UPDATE Tags SET "
#            + "TagSeal = {:d} WHERE TagSeal = {:d};").format(newSeal, tag)
#    pushQuery(cnx, cursor, statement);
#
#
#def updateObserveMark(cnx, cursor, old, new):
#    print("Update Observe Mark ", old, " to ", new)
#    statement = ("UPDATE ObserveMarks SET "
#                + "ObservationID = {:d} WHERE ObservationID = {:d};").format(new, old)
#    pushQuery(cnx, cursor, statement)
#
#def updateObserveTag(cnx, cursor, old, new):
#    print("Update Observe Tag ", old, " to ", new)
#    statement = ("UPDATE ObserveTags SET "
#                + "ObservationID = {:d} WHERE ObservationID = {:d};").format(new, old)
#    pushQuery(cnx, cursor, statement)
#
## consolidates a seal with tags/IDs that don't match on obsID
#def consolidate(cnx, cursor, sealID, tags, marks):
#    # print("tags: ", tags, "marks: ", marks)
#    seals = []
#    for ID in tags:
#        updateTag(cnx, cursor, ID, sealID)
#        updateMark(cnx, cursor, ID, sealID)
#        if ID not in seals:
#            seals.append(ID)
#        #updateObserveTag(cnx, cursor, ID, obsID)
#    for ID in marks:
#        #dropSeal(cnx, cursor, ID)
#        updateMark(cnx, cursor, ID, sealID)
#        updateTag(cnx, cursor, ID, sealID)
#        if ID not in seals:
#            seals.append(ID)
#        #updateObserveMark(cnx, cursor, ID, obsID)
#    for ID in seals:
#        updateObserveSeal(cnx, cursor, ID, sealID)
#        dropSeal(cnx, cursor, ID)
#
#def createSeal(cnx, cursor, row, oID):
#    getNewID = "SELECT MAX(SealID) FROM Seals;"
#    runQuery(cursor, getNewID)
#    result = cursor.fetchone()
#    ID = result[0]+1 if result[0] is not None else 0
#    statement = "INSERT INTO Seals VALUES ({:d}, {:d}, {:s}, FALSE)".format(ID, oID, row[SEX])
#    pushQuery(cnx, cursor, statement)
#    return ID
#
##adds all non-null tags/marks and then adds a seal
#def addSeal(cnx, cursor, row, obsID):
#    sealID = createSeal(cnx, cursor, row, obsID)
#    if(row[MARK] != "NULL"):
#        addMark(cnx, cursor, row, obsID, sealID)
#    if(row[TAG1] != "NULL"):
#        addTag(cnx, cursor, row, TAG1, obsID, sealID)
#    if(row[TAG2] != "NULL"):
#        addTag(cnx, cursor, row, TAG2, obsID, sealID)
#    return sealID
#
#def positiveMin(IDs):
#    mainID = 99999999999
#    if IDs[0] != -1:
#        mainID = IDs[0]
#    if IDs[1] != -1 and IDs[1] < mainID:
#        mainID = IDs[1]
#    if IDs[2] != -1 and IDs[2] < mainID:
#        mainID = IDs[2]
#    return mainID
#
#def observeSeal(cnx, cursor, sealID, obsID):
#    statement = "INSERT INTO ObserveSeal VALUES ({:d},{:d});".format(sealID, obsID)
#    pushQuery(cnx, cursor, statement)
#
#def updateObserveSeal(cnx, cursor, oldSeal, newSeal):
#    statement = "UPDATE ObserveSeal SET SealID = {:d} WHERE SealID = {:d};".format(newSeal, oldSeal)
#    pushQuery(cnx, cursor, statement)
#
## takes an observation and determines if the seal has been seen before
#def findSeal(cnx, cursor, row):
#    obsID = getTopObsv(cursor) + 1
#    writeObsv(cnx, cursor, row, obsID)
#
#    if(row[STLENGTH] != "NULL" or row[CRVLENGTH] != "NULL" or row[AXGIRTH] != "NULL" or row[MASS] != "NULL" or row[TARE] != "NULL" or row[MASSTARE] != "NULL"):
#        pushMeasurement(cnx, cursor, obsID, row)
#
#    divergentT = []
#    divergentM = []
#    merge = False
#
#    mID = getMark(cursor, row[MARK], row[YEAR])
#    t1ID = getTag(cursor, row[TAG1])
#    t2ID = getTag(cursor, row[TAG2])
#
#    mainID = positiveMin([mID, t1ID, t2ID])
#    # print "Positive min: {:d}".format(mainID)
#
#    if(mID == -1 and t1ID == -1 and t2ID == -1):
#        mainID = addSeal(cnx, cursor, row, obsID)
#    else:
#        if (mID == -1 and row[MARK] != "NULL"):
#            addMark(cnx, cursor, row, obsID, mainID)
#        if (t1ID == -1 and row[TAG1] != "NULL"):
#            addTag(cnx, cursor, row, TAG1, obsID, mainID)
#        if (t2ID == -1 and row[TAG2] != "NULL"):
#            addTag(cnx, cursor, row, TAG2, obsID, mainID)
#
#        if(mID != mainID and row[MARK] != "NULL" and mID != -1):
#            divergentM.append(mID)
#            merge = True
#        if(t1ID != mainID and row[TAG1] != "NULL" and t1ID != -1):
#            divergentT.append(t1ID)
#            merge = True
#        if(t2ID != mainID and row[TAG2] != "NULL" and t2ID !=  -1):
#            divergentT.append(t2ID)
#            merge = True
#        if(merge is True):
#            # print("divergents: ", divergentT, divergentM)
#            consolidate(cnx, cursor, mainID, divergentT, divergentM)
#    observeSeal(cnx, cursor, mainID, obsID)

def main():
    cnx = makeConnection()
    cursor = cnx.cursor()
    print("HELL YEAH!")
    getTopObsv(cursor)
    #filename = raw_input("Give file name: ")
    #f = open(filename)
    #line = f.read()
    #y = json.loads(line)
    xls = pd.ExcelFile("HCA.xlsx")
    for sheet in xls.sheet_names:
        df = pd.read_excel("HCA.xlsx", sheet_name=sheet, index_col=0,
                skiprows=1)
        print(df.iloc[0:1])
    #df_hca = pd.read_excel('HCA.xlsx', index_col=0)
    #print(df_hca.iloc[0])
    cnx.close()
if __name__ == '__main__':
    main()
