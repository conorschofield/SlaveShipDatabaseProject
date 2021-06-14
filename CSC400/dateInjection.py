import mysql.connector
from mysql.connector import connection
from mysql.connector import errorcode
import datetime
import string
import json
import pandas as pd
import mysql
import csv
import re

dateArr = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
abbrDates = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def addCaptureDate(cnx, cursor, caseid, date, row):
    statement = ("INSERT INTO CaptureDates (CaseId, DateOfCapture, RAW_DateofCapture) VALUES (%s, '%s', '%s');" % 
        (caseid, date, row["date of capture"]))
    print(statement)
    try:
        cursor.execute(statement)
        cnx.commit()
    except mysql.connector.Error as err:
        print(err)


def addAdjuDate(cnx, cursor, caseid, date, row):
    statement = ("INSERT INTO AdjudicationDates (CaseId, DateOfAdjudication, RAW_DateofAdjudication) VALUES (%s, '%s', '%s')" % 
        (caseid, date, row["date of adjudication"]))
    print(statement)
    try:
        cursor.execute(statement)
        cnx.commit()
    except mysql.connector.Error as err:
        print(err)

def main():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="SeniorProject2021",
      database="SeniorProject"
    )
    cursor = mydb.cursor()

    # begin parsing data
    df = pd.read_excel("HCA_Index_cleanDates.xlsx")
    df.fillna(0, inplace=True)
    df.columns = map(str.lower, df.columns)
    df.columns = map(str.rstrip, df.columns)
    defaultMonth = "1"
    defaultDay = "1"

    key = 1
    print(df.iloc[0].keys())
    for i in range (len(df)):
        # get the next row in file
        row = df.iloc[i]
        row["key"] = key
        key += 1
        #print(row["date of adjudication"])
        dateOfAdju = ""
        dateOfCapture = ""
        multDatesA = []
        multDatesC = []
        if (type(row["date of adjudication"]) == str):
            dateStr = row["date of adjudication"]
            #print(dateStr)
            multDatesA = re.split(" / ", dateStr)
            print(multDatesA)
        # go through each date of adjudication
        for dateA in multDatesA:
            dateOfAdju = dateA.strip().split()

            # correctly formatted date with day month and year
            if (len(dateOfAdju) >= 3):

                # month is long
                if(dateOfAdju[1] in dateArr):
                    datetime_object = datetime.datetime.strptime(dateOfAdju[1], "%B")
                    month_number = str(datetime_object.month)
                    # has a day
                    if (dateOfAdju[0].isdigit()):
                        sqlDate = dateOfAdju[2] + "-" + month_number + "-" + dateOfAdju[0]
                        addAdjuDate(mydb, cursor, key, sqlDate, row)
                    else: # day is not a number default to 1
                        sqlDate = dateOfAdju[2] + "-" + month_number + "-" + defaultDay
                        addAdjuDate(mydb, cursor, key, sqlDate, row)

                # month is abbreviatied
                elif(dateOfAdju[1] in abbrDates):
                    datetime_object = datetime.datetime.strptime(dateOfAdju[1], "%b")
                    month_number = str(datetime_object.month)
                    # has a day
                    if (dateOfAdju[0].isdigit()):
                        sqlDate = dateOfAdju[2] + "-" + month_number + "-" + dateOfAdju[0]
                        addAdjuDate(mydb, cursor, key, sqlDate, row)
                    else: # day is not a number default to 1
                        sqlDate = dateOfAdju[2] + "-" + month_number + "-" + defaultDay
                        addAdjuDate(mydb, cursor, key, sqlDate, row)
                # no month default to January
                else:
                    # vaild day
                    if (dateOfAdju[0].isdigit()):
                        sqlDate = dateOfAdju[2] + "-" + defaultMonth + "-" + dateOfAdju[0]
                        addAdjuDate(mydb, cursor, key, sqlDate, row)
                    # not parsable date
                    else:
                        addAdjuDate(mydb, cursor, key, None, row)

            # just month and year
            elif (len(dateOfAdju) == 2):
                # month is long
                if(dateOfAdju[0] in dateArr): 
                    datetime_object = datetime.datetime.strptime(dateOfAdju[0], "%B")
                    month_number = str(datetime_object.month)
                    sqlDate = dateOfAdju[1] + "-" + month_number + "-" + defaultDay
                    addAdjuDate(mydb, cursor, key, sqlDate, row)
                # month is short
                elif(dateOfAdju[0] in abbrDates):
                    datetime_object = datetime.datetime.strptime(dateOfAdju[0], "%b")
                    month_number = str(datetime_object.month)
                    sqlDate = dateOfAdju[1] + "-" + month_number + "-" + defaultDay
                    addAdjuDate(mydb, cursor, key, sqlDate, row)
                # not parsable date
                else:
                    addAdjuDate(mydb, cursor, key, None, row)
            # just year
            elif (len(dateOfAdju) == 1):
                # year is a number
                if (dateOfAdju[0].isdigit()):
                    sqlDate = dateOfAdju[0] + "-" + defaultMonth + "-" + defaultDay
                    addAdjuDate(mydb, cursor, key, sqlDate, row)
            else: # not parsable date
                addAdjuDate(mydb, cursor, key, None, row)

        if (type(row["date of capture"]) == str):
                dateStr = row["date of capture"]
                #print(dateStr)
                multDatesC = re.split(" / ", dateStr)
                print(multDatesC)
    # go through each date of capture for an entry
        for dateC in multDatesC:
            dateOfCapture = dateC.strip().split()

            # correctly formatted date with day month and year
            if (len(dateOfCapture) >= 3):

                # month is long
                if(dateOfCapture[1] in dateArr):
                    datetime_object = datetime.datetime.strptime(dateOfCapture[1], "%B")
                    month_number = str(datetime_object.month)
                    # has a day
                    if (dateOfCapture[0].isdigit()):
                        sqlDate = dateOfCapture[2] + "-" + month_number + "-" + dateOfCapture[0]
                        addCaptureDate(mydb, cursor, key, sqlDate, row)
                    else: # day is not a number default to 1
                        sqlDate = dateOfCapture[2] + "-" + month_number + "-" + defaultDay
                        addCaptureDate(mydb, cursor, key, sqlDate, row)

                # month is abbreviatied
                elif(dateOfCapture[1] in abbrDates):
                    datetime_object = datetime.datetime.strptime(dateOfCapture[1], "%b")
                    month_number = str(datetime_object.month)
                    # has a day
                    if (dateOfCapture[0].isdigit()):
                        sqlDate = dateOfCapture[2] + "-" + month_number + "-" + dateOfCapture[0]
                        addCaptureDate(mydb, cursor, key, sqlDate, row)
                    else: # day is not a number default to 1
                        sqlDate = dateOfCapture[2] + "-" + month_number + "-" + defaultDay
                        addCaptureDate(mydb, cursor, key, sqlDate, row)
                # no month default to January
                else:
                    # vaild day
                    if (dateOfCapture[0].isdigit()):
                        sqlDate = dateOfCapture[2] + "-" + defaultMonth + "-" + dateOfCapture[0]
                        addCaptureDate(mydb, cursor, key, sqlDate, row)
                    # not parsable date
                    else:
                        addCaptureDate(mydb, cursor, key, None, row)

            # just month and year
            elif (len(dateOfCapture) == 2):
                # month is long
                if(dateOfCapture[0] in dateArr): 
                    datetime_object = datetime.datetime.strptime(dateOfCapture[0], "%B")
                    month_number = str(datetime_object.month)
                    sqlDate = dateOfCapture[1] + "-" + month_number + "-" + defaultDay
                    addCaptureDate(mydb, cursor, key, sqlDate, row)
                # month is short
                elif(dateOfCapture[0] in abbrDates):
                    datetime_object = datetime.datetime.strptime(dateOfCapture[0], "%b")
                    month_number = str(datetime_object.month)
                    sqlDate = dateOfCapture[1] + "-" + month_number + "-" + defaultDay
                    addCaptureDate(mydb, cursor, key, sqlDate, row)
                # not parsable date
                else:
                    addCaptureDate(mydb, cursor, key, None, row)
            # just year
            elif (len(dateOfCapture) == 1):
                # year is a number
                if (dateOfCapture[0].isdigit()):
                    sqlDate = dateOfCapture[0] + "-" + defaultMonth + "-" + defaultDay
                    addCaptureDate(mydb, cursor, key, sqlDate, row)
            else: # not parsable date
                addCaptureDate(mydb, cursor, key, None, row)


    # # go through each date of adjudication
    #     if (len(dateOfAdju) == 3):
    #         if(dateOfAdju[0] in dateArr and dateOfAdju[1].isdigit()):
    #             newDate = dateOfAdju[1] + " " + dateOfAdju[0] + " " + dateOfAdju[2]
    #             #row["date of adjudication"] = newDate
    #             print(newDate)
    #     if (type(row["date of capture"]) == str):
    #         dateStr = row["date of capture"]
    #         #print(dateStr)
    #         dateOfCapture = re.split(" |, ", dateStr)
    #     if (len(dateOfCapture) == 3):
    #         if(dateOfCapture[0] in dateArr and dateOfCapture[1].isdigit()):
    #             newDate = dateOfCapture[1] + " " + dateOfCapture[0] + " " + dateOfCapture[2]
    #             #print(newDate)


        

if __name__ == '__main__':
    main()