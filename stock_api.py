from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

from bs4 import BeautifulSoup
def scrape(symbol):  
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://finance.yahoo.com/quote/'+symbol+'?p='+symbol+'&.tsrc=fin-srch%27')
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')


def checkStock(stock_name):
    symbol = yf.Ticker(stock_name)
    try:
        test = symbol.info
        return True
    except:
        return False


def getStock(stock_name):
    if(checkStock(stock_name)):
        symbol = yf.Ticker(stock_name)
        todayData = symbol.history(period='1d')
        return todayData['Close'][0]
    else:
        return "Does not exist"
    
