
import cv2
import numpy as np
import pytesseract as pt
import pymongo

def extract_bs_card_details(path):
    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(np.array(img_gray), 125, 255, cv2.THRESH_BINARY)
    scaned_text = pt.image_to_string(img)
    lines = scaned_text.split('\n')
    return lines

def save_information(data):
    user = {
            "Company":f"{data[13]}",
            "Name":f"{data[0]}",
            "Position":f"{data[2]}",
            "Email":f"{data[5][3:]}",
            "Phone":f"{data[4][1:]}",
            "Adress":f"{data[8]} {data[9]}"
            }
    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = my_client['OCR_Python']
    collection = my_db['BsCard']
    collection.insert_one(user)
    print("Details successfully captured and stored in the DataBase")

if __name__ == '__main__':
    img_path = "../resources/bs_card.jpg"
    data = extract_bs_card_details(img_path)
    save_information(data)


