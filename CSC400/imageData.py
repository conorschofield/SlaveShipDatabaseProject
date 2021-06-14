import os
import mysql.connector
import re

def fn():
    file_list = os.listdir(r"../assets/HCA-35-01")
    return (file_list)

def import_images(file_list):
    id = 1
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="SeniorProject2021",
      database="SeniorProject"
    )


    mycursor = mydb.cursor()

    imgSql = "INSERT INTO Images (UniqID, imageURL) VALUES (%s, %s)"
    imageVal = []

    for file in file_list:
        splitFileName = file.split("-")
        if (splitFileName[0] == "HCA35"):
            imageVal.append((id, file))
            id += 1

    print(imageVal)
    mycursor.executemany(imgSql, imageVal)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")

def import_image_concordance(file_list):
    id = 1

    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="SeniorProject2021",
      database="SeniorProject"
    )


    mycursor = mydb.cursor()

    imgConSql = "INSERT INTO ImageConcordance (UniqID, Volume, Page) VALUES (%s, %s, %s)"
    imageConVal = []

    for file in file_list:
        splitFileName = re.split('[- .]', file)
        if (splitFileName[0] == "HCA35"):
            volume = int(splitFileName[1])
            # checks if there is a page number
            if (splitFileName[2].isdigit()):
                imageConVal.append((id, volume, int(splitFileName[2])))
            # check if there is a second page number
            if (len(splitFileName) > 3 and splitFileName[3].isdigit()):
                imageConVal.append((id, volume, int(splitFileName[3])))
            id += 1

    print(imageConVal)
    mycursor.executemany(imgConSql, imageConVal)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")

def showDatabase():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="SeniorProject2021",
      database="SeniorProject"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM Images")

    for x in mycursor:
      print(x)

def main():
    showDatabase()
    #import_image_concordance(fn())
    #import_images(fn())
    #import_image_concordance(fn())

if __name__ == "__main__":
    main()
