from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv

url = "http://www.values.com/inspirational-quotes"

cService = webdriver.ChromeService(executable_path='C:\\Users\\HP\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe') # '/Users/bpfalz/Downloads/chromedriver' for my macbook
driver = webdriver.Chrome(service=cService)

driver.get(url)

qouestList=[]
qoutesDiv = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-6 col-lg-3 text-center margin-30px-bottom sm-margin-30px-top')]")
for p in range(len(qoutesDiv)):
    quote = {}
    quote['theme'] = qoutesDiv[p].text
    innerImg = qoutesDiv[p].find_element(By.TAG_NAME, "img")
    innera = qoutesDiv[p].find_element(By.TAG_NAME, "a")
    quote["img"] =innerImg.get_attribute('src') 
    quote["lines"] =innerImg.get_attribute('alt') 
    quote['url'] = innera.get_attribute('href')
    qouestList.append(quote)

filename = 'Week4/inspirational_quotes.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['theme','url','img','lines','author'])
    w.writeheader()
    for quote in qouestList:
        w.writerow(quote)

driver.close()