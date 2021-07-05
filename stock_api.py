from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup

"""
Initlalizes the current requested stock URL if it exists 
"""
def scrape(symbol):
    print('hello')  
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    stock_url = 'https://finance.yahoo.com/quote/'+symbol+'?p='+symbol+'&.tsrc=fin-srch%27'
    driver.get(stock_url)
    if(driver.current_url != stock_url):
        return "Does not exist"
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    return soup

def scrape_hist(symbol):  
    driver = webdriver.Chrome('chromedriver.exe')
    stock_url = 'https://finance.yahoo.com/quote/' + symbol + '/history?ltr=1'
    driver.get(stock_url)
    if(driver.current_url != stock_url):
        return "Does not exist"
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    return soup

def getPrice(stock_name):
    print('hgelp')
    soup = scrape(stock_name)
    if(soup == "Does not exist"):
        return "I don't think this stock exists"
    price = soup.find('span', 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)').get_text()
    return 'The price of ' + stock_name + ' is $' + price + ' at this current moment.'
    

def getInfo(stock_name):
    soup = scrape(stock_name)
    if(soup == "Does not exist"):
        return "I don't think this stock exists"
    volume = soup.find('td', attrs={'data-test': 'TD_VOLUME-value'}).get_text()
    open  = soup.find('td', attrs={'data-test': 'OPEN-value'}).get_text()
    prev_close = soup.find('td', attrs={'data-test': 'PREV_CLOSE-value'}).get_text()
    range  = soup.find('td', attrs={'data-test': 'DAYS_RANGE-value'}).get_text()
    sentence = 'The current volume of ' + stock_name + ' is ' +  volume + '\n'
    sentence += 'The open value today of ' + stock_name + ' is ' +  open + '\n'
    sentence += 'The previous close value of ' + stock_name + ' is ' +  prev_close + '\n'
    sentence += 'The range of ' + stock_name + ' is ' + range
    return sentence

def getGraph(stock_name):
    soup = scrape_hist(stock_name)
    if(soup == "Does not exist"):
        return "I don't think this stock exists"
    dates = []
    prices = []

