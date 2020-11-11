import pandas as pd
from bs4 import BeautifulSoup
import re

COUNTRY_NAME = "Russian Federation"
DATE_REVIEW = "12.03.2019"


# инициализация входных данных для функции parse_nogotOK()
def getNogotOKData():
    # [""] - список останется пустым
    # [] - список будет заполняться значениями
    # [SOME_NAME] - список будет заполнен константами со значением SOME_NAME
    orgAtrs = dict()
    orgAtrs["x"] = []
    orgAtrs["y"] = []
    orgAtrs["name"] = []
    orgAtrs["address"] = []
    orgAtrs["opens_at"] = []
    orgAtrs["closes_at"] = []
    orgAtrs["city"] = ["Москва и Московская область"]
    orgAtrs["cash_desk"] = [""]
    orgAtrs["gba"] = [""]
    orgAtrs["gla"] = [""]
    orgAtrs["sales_area"] = [""]
    orgAtrs["brand_name"] = ["ноготОК"]
    orgAtrs["opening_date"] = [""]
    orgAtrs["region"] = [""]
    orgAtrs["holding_name"] = [""]
    orgAtrs["parking_places"] = [""]
    orgAtrs["date_review"] = [DATE_REVIEW]
    orgAtrs["country"] = [COUNTRY_NAME]
    return orgAtrs


# инициализация входных данных для функции parse_lenaLeninaStudio()
def getlenaLeninaStudioData():
    # [""] - список останется пустым
    # [] - список будет заполняться значениями
    # [SOME_NAME] - список будет заполнен константами со значением SOME_NAME
    orgAtrs = dict()
    orgAtrs["x"] = []
    orgAtrs["y"] = []
    orgAtrs["name"] = []
    orgAtrs["address"] = []
    orgAtrs["opens_at"] = []
    orgAtrs["closes_at"] = []
    orgAtrs["city"] = []
    orgAtrs["cash_desk"] = [""]
    orgAtrs["gba"] = [""]
    orgAtrs["gla"] = [""]
    orgAtrs["sales_area"] = [""]
    orgAtrs["brand_name"] = ["студия маникюра Лены Лениной 'Новая счастливая ты'"]
    orgAtrs["opening_date"] = [""]
    orgAtrs["region"] = [""]
    orgAtrs["holding_name"] = [""]
    orgAtrs["parking_places"] = [""]
    orgAtrs["date_review"] = [DATE_REVIEW]
    orgAtrs["country"] = [COUNTRY_NAME]
    return orgAtrs


# инициализация входных данных для функции parse_lenaLeninaStudio()
def getPalchikiData():
    # [""] - список останется пустым
    # [] - список будет заполняться значениями
    # [SOME_NAME] - список будет заполнен константами со значением SOME_NAME
    orgAtrs = dict()
    orgAtrs["x"] = []
    orgAtrs["y"] = []
    orgAtrs["name"] = []
    orgAtrs["address"] = []
    orgAtrs["opens_at"] = []
    orgAtrs["closes_at"] = []
    orgAtrs["city"] = []
    orgAtrs["cash_desk"] = [""]
    orgAtrs["gba"] = [""]
    orgAtrs["gla"] = [""]
    orgAtrs["sales_area"] = [""]
    orgAtrs["brand_name"] = ["САЛОН МАНИКЮРА И ПЕДИКЮРА 'ПАЛЬЧИКИ'"]
    orgAtrs["opening_date"] = [""]
    orgAtrs["region"] = [""]
    orgAtrs["holding_name"] = [""]
    orgAtrs["parking_places"] = [""]
    orgAtrs["date_review"] = [DATE_REVIEW]
    orgAtrs["country"] = [COUNTRY_NAME]
    return orgAtrs


# инициализация входных данных для функции parse_leruamerlen()
def getLeruaMerlenData():
    # [""] - список останется пустым
    # [] - список будет заполняться значениями
    # [SOME_NAME] - список будет заполнен константами со значением SOME_NAME
    orgAtrs = dict()
    orgAtrs["x"] = []
    orgAtrs["y"] = []
    orgAtrs["name"] = []
    orgAtrs["address"] = []
    orgAtrs["opens_at"] = []
    orgAtrs["closes_at"] = []
    orgAtrs["city"] = []
    orgAtrs["cash_desk"] = [""]
    orgAtrs["gba"] = [""]
    orgAtrs["gla"] = [""]
    orgAtrs["sales_area"] = [""]
    orgAtrs["brand_name"] = ["Леруа Мерлен"]
    orgAtrs["opening_date"] = [""]
    orgAtrs["region"] = [""]
    orgAtrs["holding_name"] = [""]
    orgAtrs["parking_places"] = [""]
    orgAtrs["date_review"] = [DATE_REVIEW]
    orgAtrs["country"] = [COUNTRY_NAME]
    return orgAtrs


def standardizerCoordinateX(inputList):
    outputList = list()
    for i in range(0, len(inputList)):
        try:
            outputList.append(re.search(r'\S+,', inputList[i]).group().replace(",", ""))
        except:
            outputList.append("")
    return outputList


def standardizerCoordinateY(inputList):
    outputList = list()
    for i in range(0, len(inputList)):
        try:
            outputList.append(re.search(r',\S+', inputList[i]).group().replace(",", ""))
        except:
            outputList.append("")
    return outputList


def standardizerCityName(inputList):
    outputList = list()
    for i in range(0, len(inputList)):
        #print(inputList[i])
        try:
            if not any(map(str.isdigit, re.search(r"([сгпдх]|нп|город)\.\s*\b[\w-]+", inputList[i]).group())):
                outputList.append(re.search(r"([сгпдх]|нп|город)\.\s*\b[\w-]+", inputList[i]).group())
            else:
                outputList.append("")
        except:
            outputList.append("")
    return outputList


def standardizerTimeOpen(inputList):
    outputList = list()
    for i in range(0, len(inputList)):
        try:
            outputList.append(re.search(r'[Сс]*\d\d[:\.\-]\d\d', inputList[i].replace(" ", "")).group().replace("с", "").replace("С", ""))
        except:
            outputList.append("")
    return outputList


def standardizerTimeClose_v1(inputList):
    outputList = list()
    for i in range(0, len(inputList)):
        try:
            outputList.append(re.search(r'(до|-|—)\d\d[:\.\-]\d\d', inputList[i].replace(" ", "")).group().replace("до", "").replace("-", "").replace("—", ""))
        except:
            outputList.append("")
    return outputList


def standardizerTimeClose_v2(inputList):
    outputList = list()
    for i in range(0, len(inputList)):
        try:
            outputList.append(re.search(r'(до|-|—)\d\d[:\.\-]\d\d', inputList[i].replace(" ", "")).group().replace("до","").replace("—", ""))
        except:
            outputList.append("")
    return outputList


def parseTable(source_code):
    table = []
    data = []
    soup = BeautifulSoup(source_code, 'html.parser')
    table = soup.find_all("table")
    for i in range(0, len(table)):
        table_body = table[i].find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(str([ele for ele in cols if ele])[35:]) # in lerua parser we cut telephone
    return data


def CreateCsvData(finalList):
    for key in finalList:
        if len(finalList[key]) == 1:
            finalList[key] = finalList[key] * len(finalList["name"])

    df = pd.DataFrame(
        {'x': finalList["x"], 'y': finalList["y"], 'id': [str(x) for x in range(1, len(finalList["name"]) + 1)],
         'name': finalList["name"], 'city': finalList["city"], 'address': finalList["address"],
         'cash_desk': finalList["cash_desk"], 'gba': finalList["gba"], 'gla': finalList["gla"],
         'sales_area': finalList["sales_area"], 'brand_name': finalList["brand_name"],
         'opening_date': finalList["opening_date"],
         'region': finalList["region"], 'holding_name': finalList["holding_name"],
         'parking_places': finalList["parking_places"],
         'date_review': finalList["date_review"], 'country': finalList["country"],
         'opens_at': finalList["opens_at"],
         'closes_at': finalList["closes_at"]})

    df.to_csv('parse_' + finalList["brand_name"][0] + '_res.csv', sep=';', encoding='utf-8', index=False)
