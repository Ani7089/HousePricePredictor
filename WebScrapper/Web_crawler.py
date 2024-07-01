import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import html5lib
import requests
from bs4 import BeautifulSoup
import re
import random
import pandas as pd



options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service = s)

#pages it is hitting 
driver.get("https://www.99acres.com/search/property/buy/mumbai?city=12&keyword=mumbai&preference=S&area_unit=1&res_com=R")
#Using random sleep time
time.sleep(round(20*random.random(),0))


# list of all the data which is been extracted
Name = []
Area = []
Price = []
BHK = []
Builder = []
desc = []
Nearby = []


#No of pages it is hitting
for k in range(100):

    #location of chrome bot in PC
    s = Service("C:/Users/lenovo/Desktop/chromedriver.exe")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service = s)

    #Link it is hitting page wise
    driver.get(f"https://www.99acres.com/property-in-mumbai-ffid-page-{k}")
    time.sleep(round(20*random.random(),0))

    webpage = driver.page_source

    soup=BeautifulSoup(webpage,'html.parser')

    data = soup

    #Scroll the webpage
    old_height = driver.execute_script('return document.body.scrollHeight')
    while True:

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(round(20*random.random(),0))

        new_height = driver.execute_script('return document.body.scrollHeight')

        if new_height == old_height:
            break

        old_height = new_height

    

    #No of blocks it is extracting in a page
    for i in range(len(data.find_all('div', class_='PseudoTupleRevamp__outerTupleWrap'))):
        
        #Type of building in a block 
        for j in range(len(data.find_all('div', class_='PseudoTupleRevamp__outerTupleWrap')[i].find_all('div', class_='configs__configCard'))):

            # Name
            try :
                Name.append(re.sub(r'\s+', ' ', data.find_all('div', class_='PseudoTupleRevamp__outerTupleWrap')[i].find_all('a', class_='ellipsis')[0].text).strip())
            except :
                Name.append('')

            # Description
            try :
                desc.append(re.sub(r'\s+', ' ', data.find_all('div', class_='PseudoTupleRevamp__outerTupleWrap')[i].find_all('p', class_ = "descPtag_undefined tupleNew__descText")[0].text).strip())
            except :
                desc.append('')
           
            # Carpet Area
            try :
                text = re.sub(r'\s+', ' ', data.find_all('div', class_='PseudoTupleRevamp__outerTupleWrap')[i].find_all('p', class_ = "descPtag_undefined tupleNew__descText")[0].text).strip()
                text = text.replace(',', '')
                text = text.replace('.','')
                text = text[::-1]
                text
                pattern = r"tfqs\s(\d+) - (\d+)"
                matches = re.findall(pattern, text)
                matches
                s = str(matches[0][1])[::-1] + ' - ' + str(matches[0][0])[::-1] + ' sq.ft'
                Area.append(s)
            except:
                Area.append('')

            #Builder
            try:
                Builder.append(re.sub(r'\s+', ' ', data.find_all('div', class_='PseudoTupleRevamp__outerTupleWrap')[i].find_all('div', class_ = "PseudoTupleRevamp__contactSubheading")[0].text).strip())
            except:
                Builder.append('')

            #BHK
            try:
                BHK.append(re.sub(r'\s+', ' ', data.find_all('div', class_='PseudoTupleRevamp__outerTupleWrap')[i].find_all('div', class_ = "configs__configCard")[j].find_all('div', class_ = "configs__ccl1")[0].text).strip())
            except:
                BHK.append('')

            #Price
            try:
                Price.append(re.sub(r'\s+', ' ', data.find_all('div', class_='PseudoTupleRevamp__outerTupleWrap')[i].find_all('div', class_ = "configs__configCard")[j].find_all('div', class_ = "configs__ccl2")[0].text).strip())
            except:
                Price.append('')

            #Nearby 
            Near = []
            try:
                for p in range(len(data.find_all('div', class_='tupleNew__onlyHighlight')[i].find_all('span', class_='tupleNew__unitHighlightTxt'))):
                    Near.append(data.find_all('div', class_='tupleNew__onlyHighlight')[i].find_all('span', class_='tupleNew__unitHighlightTxt')[p].text.replace('\n','').strip())
                Nearby.append(Near)
            except:
                Nearby.append(Near)
 

print(len(Name))
print(len(Builder))
print(len(BHK))
print(len(Price))
print(len(Area))
print(len(desc))
print(len(Nearby))

#adding column name and creating the dataframe
ind = ['Name', 'Builder', 'BHK', 'Price', 'Area', 'Description', 'Nearby']
data = pd.DataFrame({
    'Name' : Name,
    'Builder' : Builder,
    'BHK' : BHK,
    'Price' : Price,
    'Area' : Area,
    'Description' : desc,
    'Nearby' : Nearby
}, columns = ind)

data.reset_index(drop=True)


#Converting the dataframe to CSV file and exporting it
data.to_csv('99Acres.csv', mode='a', header=False, index=False)
    