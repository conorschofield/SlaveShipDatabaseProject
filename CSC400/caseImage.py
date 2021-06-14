import os
import mysql.connector
import re

def add_case_images(cnx, cursor, caseImgIdPairArr):
    statement = "INSERT INTO CaseImage (UniqCase, UniqImage) VALUES (%s, %s)"
    try:
        cursor.executemany(statement, caseImgIdPairArr)
        cnx.commit()
    except mysql.connector.Error as err:
        print("err: ", err)
        #exit(1)

def iterateData():
    image_arr = []
    caseImgIdPairArr = []

    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="SeniorProject2021",
      database="SeniorProject"
    )

    cursor = mydb.cursor()
    images = cursor.execute("SELECT * FROM ImageConcordance JOIN Images ON ImageConcordance.UniqID = Images.UniqID;")
    for image in cursor:
        #print(image)
        imgId = image[0]
        imgVol = image[1]
        imgPage = image[2]
        imgURL = image[4]
        image_arr.append((imgId, imgVol, imgPage, imgURL))

    cases = cursor.execute("SELECT * FROM Cases;")
    for case in cursor:
        caseId = case[0]
        vol = case[2]
        startPage = case[3]
        endPage = case[4]
        numberofPages = endPage - startPage
        # for now just do the first Volume
        if (vol == 1):
            #print(numberofPages)
            for i in range(numberofPages + 1):
                pageNumber = startPage + i
                #print(pageNumber)
                imgIds = find_imageId(pageNumber, image_arr)
                for imgId in imgIds:
                    print((caseId, imgId))
                    caseImgIdPairArr.append((caseId, imgId))
    caseImgIdPairArr = list(set(caseImgIdPairArr))
    add_case_images(mydb, cursor, caseImgIdPairArr)
    mydb.close()

# returns an array of image ids that matches given page number
def find_imageId(pageNumber, images):
    imgIds = []
    for image in images:
        # find image with matching page could be more than 1
        if (image[2] == pageNumber):
            imgIds.append(image[0])
    return imgIds

def main():
    iterateData()
    
if __name__ == "__main__":
    main()
