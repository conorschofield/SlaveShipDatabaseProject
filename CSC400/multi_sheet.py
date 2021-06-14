import mysql.connector
from mysql.connector import connection
from mysql.connector import errorcode
from datetime import datetime
import string
import json
import pandas as pd
import mysql
import csv

f = open("exceptions.txt", "w")
exceptions = []

def makeConnection():
    try:
        print("HELO")
        cnx = mysql.connector.connect(user='root',
                                        password='SeniorProject2021',
                                        host='localhost',
                                        database='SeniorProject')
        print("YO")
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("connection")
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
def get_captors(cursor):
    statement = "SELECT * FROM Captor;"
    result = runQuery(cursor, statement)
    rows = cursor.fetchall()
    print(rows)

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


def add_captor(cnx, cursor, captor, ident, row):
    statement = ("INSERT INTO Captor VALUES (%s, '%s');" % (ident, captor))        #
    print(statement)
    try:
        cursor.execute(statement)
        cnx.commit()
    except mysql.connector.Error as err:
        write_ex(f, row, err)
        #print(err)
        #exit(1)

def add_location(cnx, cursor, location, ident, row):
    statement = ("INSERT INTO Location VALUES (%s, '%s');" % (ident, location))
    print(statement)
    try:
        cursor.execute(statement)
        cnx.commit()
    except mysql.connector.Error as err:
        write_ex(f, row, err)
        #print(err)
        #exit(1)


def add_stat(cnx, cursor, row):
    total = int(row["men"]) + int(row["women"]) + int(row["boys"]) + int(row["girls"])
    statement = ("INSERT INTO SlaveStats VALUES ('%s', %s, %s, %s, %s, %s, %s);"
            % (row["key"],
                row["men"],
                row["women"],
                row["boys"],
                row["girls"],
                0,
                total)) #TODO this is going to take some tinkering
    try:
        cursor.execute(statement)
        cnx.commit()
        print(statement)
    except mysql.connector.Error as err:
        write_ex(f, row, err)
        #print("SLAVES#################################################")
        #exceptions.append((row, err, row["volume"]))
        #print(err)
        #exit(1)

def add_case(cnx, cursor, row, captor, loc):
    statement = ("INSERT INTO Cases (Uniq, RedNumber, Volume, StartPage, EndPage, CaseN, Court, Mixed, Register, Captor, Location, Notes, ) VALUES " +
                "(%s, '%s', %d, %d, %d, '%s', '%s', '%s', '%s', %d, %d, '%s');"
                % (row["key"],
                    (row["red number"]),
                    (row["vol."]),
                    (row["start page"]),
                    (row["end page"]),
                    (row["case (ship)"]),
                    (row["court"]),
                    (row["mixed commission?"]),
                    (row["register?"]),
                    (captor),
                    (loc),
                    row["notes"]))
   # statement = ("INSERT INTO Cases VALUES " +
   #             "('%s', '%s', '%s')" %
   #             (str(rn),
   #             str(-1),
   #             str(row["Red number"])))
    #print(statement)
    try:
        print(statement)
        cursor.execute(statement)
        cnx.commit()
    except mysql.connector.Error as err:
        write_ex(f, row, err)
        #print(err)
        #exit(1)


# this function writes an exception to output csv
def write_ex(f, ex, err):
    #write out issues
    f.write("volume, start page , Case(Ship), Court, Red Number, Mixed, Date of Adjudication, " +
            "Date of Capture, Capturing Ship/Captor, Place of Capture, Number of Slaves," +
            "Men, Women, Boys, Girls, Register?, Notes, error\n")
    f.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" %
            (str(ex["volume"]),
             str(ex["start page"]),
             str(ex["case (ship)"]),
             str(ex["court"]),
             str(ex["red number"]),
             str(ex["mixed commission?"]),
             str(ex["date of adjudication"]),
             str(ex["date of capture"]),
             str(ex["capturing ship/captor"]),
             str(ex["place of capture"]),
             str(ex["number of slaves"]),
             str(ex["men"]),
             str(ex["women"]),
             str(ex["boys"]),
             str(ex["girls"]),
             str(ex["register?"]),
             str(ex["notes"]).replace(",", ""),
             str(err).replace(",", "")))
    #f.write(ex.to_csv(index=True).replace("\n", ","))
    #f.write(str(err))
    #f.write("\n")

def main():
    # initialize variables
    captors = []
    captor_count = 0
    push_captor = 0
    locations = []
    location_count = 0
    push_location = 0
    volume = 0
    exceptions = []
    key = 1

    # make connection to database
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="SeniorProject2021",
      database="SeniorProject"
    )
    cursor = mydb.cursor()

    # begin parsing data
    xls = pd.ExcelFile("HCA35_Index_clean.xlsx")
    for sheet in xls.sheet_names:
        volume += 1
        print("new sheet")
        df = pd.read_excel("HCA35_Index_clean.xlsx")
        df.fillna(0, inplace=True)
        df.columns = map(str.lower, df.columns)
        df.columns = map(str.rstrip, df.columns)
        f.write(str(list(df.iloc[0].keys())) + "\n")

        print(df.iloc[0].keys())
        for i in range (len(df)):
            # get the next row in file
            row = df.iloc[i]
            row["volume"] = volume
            row["key"] = key
            key += 1
            print("new row")

            # check if Captor has been seen
            if (row["capturing ship/captor"] not in captors):
                captors.append(row["capturing ship/captor"])
                add_captor(mydb, cursor, row["capturing ship/captor"], len(captors), row)
            # check if Location has been seen
            if (row["place of capture"] not in locations):
                locations.append(row["place of capture"])
                add_location(mydb, cursor, row["place of capture"], len(locations), row)

            # make compound red number
            # unnecessary, I changed the key values of the data base
            #rn = str(row["red number"]).translate(str.maketrans('', '', string.punctuation))


            # add to Cases
            add_case(mydb, cursor, row,
                    int(captors.index(row["capturing ship/captor"])+1),
                    int(locations.index(row["place of capture"])+1))

            # add to SlaveStats
            add_stat(mydb, cursor, row)

            if(len(exceptions) != 0):
                print("BITCHINNNNNNNNNNN")
        #for (ex, err, volume) in exceptions:
        #    print(ex)
        #    write_ex(f, ex, err)
            #f.write(ex.to_csv(index=False).replace("\n", ","))
            #f.write(str(err))
            #f.write("\n")
        #case_key = s.translate(str.maketrans('', '', string.punctuation))

    #get all current captors
    #get_captors(cursor)
    #xls = pd.ExcelFile("HCA.xlsx")
    #for sheet in xls.sheet_names:
    #    df = pd.read_excel("HCA.xlsx", sheet_name=sheet, index_col=0,
    #            skiprows=1)
        #print(df.iloc[0:1])
    #df_hca = pd.read_excel('HCA.xlsx', index_col=0)
    #print(df_hca.iloc[0])
    print(len(exceptions))
    #f = open("exceptions.txt", "w")
    #f.write(str(list(row.keys())) + "")
    #f.close()
    #cnx.close()

if __name__ == '__main__':
    main()
