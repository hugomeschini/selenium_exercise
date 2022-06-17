#import libraries
from selenium import webdriver
import urllib3
import re 
import time
import pandas as pd

#necessary to download the file according to the browser you choose
chrome_driver_path = 'chromedriver.exe'
options  = webdriver.ChromeOptions()

#create a drive
driver = webdriver.Chrome(executable_path = chrome_driver_path, options = options)

#URL we will acess
url = 'https://insolvencyinsider.ca/filing/'

#Driver to change the url status
driver.get(url)

#as from now is possible to click buttons "load more"
loadMore = driver.find_element_by_xpath(xpath="/html/body/div[2]/div/main/div/div/div/button")


#we need to understand how many pages we have in order to make the click (load more). Doing this with urllib3 y re
url = "https://insolvencyinsider.ca/filing/"
http = urllib3.PoolManager()
r = http.request("GET", url)
text = str(r.data)

#we need to extract total pages from our text. This is possible to print text using RE.
totalPagesObj = re.search(pattern='"total_pages":\d+', string=text)
totalPagesStr = totalPagesObj.group(0)
totalPages = int((re.search(pattern="\d+", string=totalPagesStr)).group(0))

#print(totalPagesObj)
#print(totalPagesStr)
#print(totalPages)

#click the button (load) - we need to establish a time.sleep, around 3 seconds
for i in range(10):
    loadMore.click()
    time.sleep(3)

#get/find data
filingNamesElements = driver.find_elements_by_class_name("filing-name")
filingDateElements = driver.find_elements_by_class_name("filing-date")
filingHrefElements = driver.find_elements_by_xpath("//*[@id='content']/div[2]/div/div[1]/h3/a")


#getting meta description
filingMetas = []
for i in range(len(filingNamesElements) + 1):
    filingMetai = driver.find_elements_by_xpath(("//*[@id='content']/div[2]/div[%d]/div[2]/div[1]" %(i)))
    for element in filingMetai:
        filingMetaTexti = element.text
        filingMetas.append(filingMetaTexti)


#extract some detail from each element
metaDict = {"Filing Type": [], "Industry": [], "Province": []}
for filing in filingMetas:
    filingSplit = filing.split("\n")
  
    for item in filingSplit:
        itemSplit = item.split(":")

        
        if itemSplit[0] == "Filing Type":
            metaDict["Filing Type"].append(itemSplit[1])
        elif itemSplit[0] == "Industry":
            metaDict["Industry"].append(itemSplit[1])
        elif itemSplit[0] == "Province":
            metaDict["Province"].append(itemSplit[1])
            
    if "Filing Type" not in filing:
        metaDict["Filing Type"].append("NA")
    if "Industry" not in filing:
        metaDict["Industry"].append("NA")
    if "Province" not in filing:
        metaDict["Province"].append("NA")

for key in metaDict:
    print(len(metaDict[key]))
