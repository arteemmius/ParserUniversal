from selenium import webdriver
from parsel import Selector
import pandas as pd
from bs4 import BeautifulSoup
import urllib3
import re
from time import sleep
from Include.Utils import *


def getPandasDF(finalList):
    for key in finalList:
        if len(finalList[key]) == 1:
            finalList[key] = finalList[key] * len(finalList["name"])

    df = pd.DataFrame(
        {'x': finalList["x"], 'y': finalList["y"],'id': [str(x) for x in range(1, len(finalList["name"]) + 1)],
         'name': finalList["name"], 'city': finalList["city"], 'address': finalList["address"],
         'cash_desk': finalList["cash_desk"], 'gba': finalList["gba"], 'gla': finalList["gla"],
         'sales_area': finalList["sales_area"], 'brand_name': finalList["brand_name"],
         'opening_date': finalList["opening_date"],
         'region': finalList["region"], 'holding_name': finalList["holding_name"],
         'parking_places': finalList["parking_places"],
         'date_review': finalList["date_review"], 'country': finalList["country"],
         'opens_at': finalList["opens_at"],
         'closes_at': finalList["closes_at"]})

    df.x = pd.to_numeric(df.x, downcast='float')
    df.y = pd.to_numeric(df.y, downcast='float')
    df.id = pd.to_numeric(df.id, downcast='integer')
    df.sales_area = pd.to_numeric(df.sales_area, downcast='integer')
    df.date_review = pd.to_datetime(df.date_review).dt.strftime('%d.%m.%Y')
    df.opening_date = pd.to_datetime(df.opening_date).dt.strftime('%d.%m.%Y')

    return df


def parse_nogotOK():
    orgLists = getNogotOKData()
    # get html by url
    driver.get("http://www.nogotok-studio.ru/salons/")
    # get data
    sel = Selector(text=driver.find_element_by_xpath("//*").get_attribute("outerHTML"))
    orgLists["name"] = sel.xpath("//div[@class='swiper-wrapper']/div/@data-name").extract()
    orgLists["opens_at"] = standardizerTimeOpen(sel.xpath("//div[@class='swiper-wrapper']/div/@data-time").extract())
    orgLists["closes_at"] = standardizerTimeClose_v1(sel.xpath("//div[@class='swiper-wrapper']/div/@data-time").extract())
    orgLists["address"] = sel.xpath("//div[@class='swiper-wrapper']/div/@data-address").extract()
    orgLists["x"] = standardizerCoordinateX(sel.xpath("//div[@class='swiper-wrapper']/div/@data-coords").extract())
    orgLists["y"] = standardizerCoordinateY(sel.xpath("//div[@class='swiper-wrapper']/div/@data-coords").extract())
    driver.close()

    #CreateCsvData(orgLists)
    getPandasDF(orgLists)


def parse_lenaLeninaStudio():
    orgLists = getlenaLeninaStudioData()
    # get html by url
    URL_LenaStudio = "https://llmanikur.ru/studios/"
    driver.get(URL_LenaStudio)
    driver.find_element_by_xpath("//button[@class='header-main-menu-item header-main-menu-item_type_city js-city-link']").click()
    sleep(2)
    sel_one = Selector(text=driver.find_element_by_xpath("//*").get_attribute("outerHTML"))
    idList = sel_one.xpath("//ul[@class='header-main-menu-widget-city__list 1 js-country-cities']/li/text()").extract()
    for j in range(0, len(idList)):
        if j != 0:
            driver.get(URL_LenaStudio)
            driver.find_element_by_xpath("//button[@class='header-main-menu-item header-main-menu-item_type_city js-city-link']").click()
            sleep(2)
        driver.find_element_by_xpath("//ul[@class='header-main-menu-widget-city__list 1 js-country-cities']/li[.='" + str(idList[j]) + "']").click()
        driver.get(URL_LenaStudio)
        # scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        request = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        #print(driver.find_element_by_xpath("//*").get_attribute("outerHTML"))
        #exit(0)
        sel_two = Selector(text=request)
        orgLists["name"] = orgLists["name"] + sel_two.xpath("//div[@class='page-studio-list-item js-studio-list-item']//a[@class='page-studio-list-item__name']/text()").extract()
        dataList = sel_two.xpath("//div[@class='page-studio-list-item js-studio-list-item']//div[@class='page-studio-list-item__address']").extract()
        for i in range(0, len(dataList)):
            sel_three = Selector(text=dataList[i])
            orgLists["address"].append(sel_three.xpath("//div/text()").extract_first())
            orgLists["city"].append(sel_three.xpath("//div/text()").extract_first())
            try:
                orgLists["opens_at"].append(sel_three.xpath("//div/span/text()").extract_first())
                orgLists["closes_at"].append(sel_three.xpath("//div/span/text()").extract_first())
            except:
                orgLists["opens_at"].append("")
                orgLists["closes_at"].append("")

        elem = driver.find_elements_by_xpath("//a[@class='page-studio-list-item__gallery']")
        refList = []
        for k in range(0, len(elem)):
            refList.append(elem[k].get_attribute("href"))

        for i in range(0,len(refList)):
            #print(elem[i].get_attribute("outerHTML"))
            driver.get(refList[i])
            sel_four = Selector(text=driver.find_element_by_xpath("//*").get_attribute("outerHTML"))
            try:
                orgLists["x"].append(sel_four.xpath("//div[@class='studios-detail-contacts']/span[@itemprop='geo']/meta/@content").extract()[0])
            except:
                orgLists["x"].append("")
            try:
                orgLists["y"].append(sel_four.xpath("//div[@class='studios-detail-contacts']/span[@itemprop='geo']/meta/@content").extract()[1])
            except:
                orgLists["y"].append("")
            sleep(2)
    driver.close()
    orgLists["city"] = standardizerCityName(orgLists["city"])
    orgLists["opens_at"] = standardizerTimeOpen(orgLists["opens_at"])
    orgLists["closes_at"] = standardizerTimeClose_v2(orgLists["closes_at"])

    #CreateCsvData(orgLists)
    getPandasDF(orgLists)


def parse_palchiki():
    orgLists = getPalchikiData()
    URL_palchiki = "http://www.palchiki.com"
    driver.get(URL_palchiki)
    #print(driver.find_element_by_xpath("//*").get_attribute("outerHTML"))
    driver.find_element_by_xpath("//div[@class='mainmenu-wrapper collapsed']//span[@class='separator ']").click()
    sel_one = Selector(text=driver.find_element_by_xpath("//*").get_attribute("outerHTML"))
    idList = sel_one.xpath("//li[@class='item-225 divider deeper parent']/ul[@class='nav-child unstyled small sub-menu']/li/a/@href").extract()
    townList = sel_one.xpath("//li[@class='item-225 divider deeper parent']/ul[@class='nav-child unstyled small sub-menu']/li/a/text()").extract()
    #print(townList)
    for j in range(0, len(idList)):
        current_ref = URL_palchiki + idList[j]
        #print("get " + current_ref)
        driver.get(current_ref)
        sel_two = Selector(text=driver.find_element_by_xpath("//*").get_attribute("outerHTML"))
        if current_ref == 'http://www.palchiki.com/adresa/moskva.html':
            #refList = sel_two.xpath("//div[@class='row']/div/a/@href").extract()
            driver.find_element_by_link_text("Список салонов").click()
            sel_three = Selector(text=driver.find_element_by_xpath("//*").get_attribute("outerHTML"))
            first_dataList = sel_three.xpath("//div[@class='col-md-12']/p/text()").extract()
            for i in range(0, len(first_dataList)):
                orgLists["address"].append(first_dataList[i].split(" | ")[0])
                orgLists["name"].append(first_dataList[i].split(" | ")[0])
                orgLists["opens_at"].append(first_dataList[i].split(" | ")[2])
                orgLists["closes_at"].append(first_dataList[i].split(" | ")[2])
                orgLists["city"].append("Москва и Московская область")
                orgLists["x"].append("")
                orgLists["y"].append("")

            continue
        if current_ref == 'http://www.palchiki.com/adresa/reutov.html':
            dataList = sel_two.xpath("//div[@class='item-page']/p/text()").extract()
        else:
            dataList = sel_two.xpath("//div[@class='z-content-inner']/p/text()").extract()

        dataList = [a for a in dataList if a != u'\xa0' and a!='\n\n\n\n\n\t\t']

        if len(dataList) % 2 == 0:
            step = 2
        if len(dataList) % 3 == 0:
            step = 3
        for k in range(0, int(len(dataList)/step)):
            orgLists["address"].append(dataList[0 + step * k])
            orgLists["name"].append(dataList[0 + step * k])
            orgLists["city"].append(townList[j])
            if step == 2:
                orgLists["opens_at"].append("")
                orgLists["closes_at"].append("")
                continue
            orgLists["opens_at"].append(dataList[2 + step * k])
            orgLists["closes_at"].append(dataList[2 + step * k])
        if current_ref == 'http://www.palchiki.com/adresa/reutov.html':
            iframeList = sel_two.xpath("//div[@class='moduletable']/div[@class='custom']//iframe/@src").extract()
        else:
            iframeList = sel_two.xpath("//div[@class='z-content-inner']/div[@class='moduletable']//iframe/@src").extract()
        if not iframeList:
            orgLists["x"].append("")
            orgLists["y"].append("")
            continue
        http = urllib3.PoolManager()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        for i in range(0, len(iframeList)):
            request = http.request("GET", iframeList[i])
            try:
                orgLists["x"].append(
                re.search(r'\[\d+\.\d+,\d+\.\d+\]', request.data.decode("utf-8")).group().replace("[", "").replace("]", ""))
                orgLists["y"].append(
                re.search(r'\[\d+\.\d+,\d+\.\d+\]', request.data.decode("utf-8")).group().replace("[", "").replace("]", ""))
            except:
                orgLists["x"].append("")
                orgLists["y"].append("")

    driver.close()
    orgLists["opens_at"] = standardizerTimeOpen(orgLists["opens_at"])
    orgLists["closes_at"] = standardizerTimeClose_v2(orgLists["closes_at"])
    orgLists["x"] = standardizerCoordinateX(orgLists["x"])
    orgLists["y"] = standardizerCoordinateY(orgLists["y"])

    #CreateCsvData(orgLists)
    getPandasDF(orgLists)

def parse_leruamerlen():
    orgLists = getLeruaMerlenData()
    URL_lerua = "https://leroymerlin.ru/shop/"
    driver.get(URL_lerua)
    driver.find_element_by_xpath("//*[@class='shops-info-region__your-region']/button").click()
    sleep(5)
    driver.find_element_by_link_text("Вся Россия").click()
    data = driver.find_element_by_xpath("//*[@class='shops-list scroll mCustomScrollbar _mCS_2']")

    source_code = data.get_attribute("outerHTML")
    soup = BeautifulSoup(source_code, 'html.parser')

    contact_data = parseTable(source_code)

    orgLists["name"] = [i.text.strip() for i in (soup.find_all('span', class_='shop-list-item__name ng-binding'))]
    orgLists["address"] = [i.text.strip() for i in (soup.find_all('span', class_='shop-list-item__address ng-binding'))]
    orgLists["city"] = standardizerCityName(orgLists["address"])
    orgLists["opens_at"] = standardizerTimeOpen(contact_data)
    orgLists["closes_at"] = standardizerTimeClose_v1(contact_data)

    elem = driver.find_element_by_xpath("//div[@class='shop ng-scope']/script")
    tagList = elem.get_attribute("outerHTML").split("\n")
    for i in range(0, len(tagList)):
        if "startShops.push" in tagList[i]:
            index = orgLists["address"].index(tagList[i + 13].replace("                'address': '", "").replace(" ',", "").replace("',", ""))
            orgLists["x"].insert(index, tagList[i + 4].replace("            'latitude': '", "").replace("',", ""))
            orgLists["y"].insert(index, tagList[i + 5].replace("            'longitude': ' ", "").replace("',", ""))

    #CreateCsvData(orgLists)
    getPandasDF(orgLists)


driver = webdriver.Chrome()
driver.set_window_size(1500, driver.get_window_size()['height'])
#parse_nogotOK()
parse_lenaLeninaStudio()
#parse_palchiki()
#parse_leruamerlen()


