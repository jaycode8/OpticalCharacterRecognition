
import cv2
import numpy as np
import pytesseract as pt
import pymongo
import mysql.connector

# ------------------------ MySQL configuration ------------------------
myDb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '****',
        database = 'OCR_Python'
    )
mycursor = myDb.cursor()


def extract_bs_card_details(path):
    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(np.array(img_gray), 200, 255, cv2.THRESH_BINARY)
    scaned_text = pt.image_to_string(img)
    lines = scaned_text.split('\n')
    return lines

def save_information(data):
    card_infor ={
            "ACC No":f"{data[0]}",
            "card holder":f"{data[3]}",
            "Expires on":f"{data[2][4:]}"
            }
    fav_db = eval(input("Enter your preffered DB for data storange \n1: MongoDB \n2: MySQL \n>>>"))
    if fav_db ==1:
        mongoDataBase(card_infor)
    elif fav_db ==2:
        mysqlDataBase(card_infor)
    else:
        print('wrong DB')

def mongoDataBase(data):
    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = my_client['OCR_Python']
    collection = my_db['ATMCard']
    collection.insert_one(data)
    print("Card infor saved to MongoDB successfully")

def mysqlDataBase(data):
    sql = "INSERT INTO ATMCard (ACC_NO, HOLDER, Expires) VALUES (%s, %s, %s)"
    dt = (data['ACC No'], data['card holder'], data['Expires on'])
    mycursor.execute(sql, dt)
    myDb.commit()
    print("Card infor saved to MySQL successfully")

if __name__ == '__main__':
    img_path = "../resources/atm_card.jpeg"
    extracted_text = extract_bs_card_details(img_path)
    save_information(extracted_text)

