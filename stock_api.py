"""
Acesses Yahoo Finance for stock data and retrieves
the most important pieces of info. 

"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

"""
Initlalizes the current requested stock URL if it exists 
"""
def scrape(symbol): 
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

# Sets up the page that will be scraped for historical data 

def scrape_hist(symbol):  
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    stock_url = 'https://finance.yahoo.com/quote/' + symbol + '/history?ltr=1'
    driver.get(stock_url)
    if(driver.current_url != stock_url):
        return "Does not exist"
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    return soup

# Gets the current stocks name

def get_name(soup):
    return soup.find('h1', 'D(ib) Fz(18px)').get_text()

# Gets the current price of the requested stock

def getPrice(stock_name):
    soup = scrape(stock_name)
    name = get_name(soup)
    if(soup == "Does not exist"):
        return "I don't think this stock exists"
    price = soup.find('span', 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)').get_text()
    return 'The price of ' + name + ' is $' + price + ' at this current moment.'
    
# Gets basic info of volume, open, closing, and range of the
# price of a stock

def getInfo(stock_name):
    soup = scrape(stock_name)
    name = get_name(soup)
    if(soup == "Does not exist"):
        return "I don't think this stock exists"
    volume = soup.find('td', attrs={'data-test': 'TD_VOLUME-value'}).get_text()
    open  = soup.find('td', attrs={'data-test': 'OPEN-value'}).get_text()
    prev_close = soup.find('td', attrs={'data-test': 'PREV_CLOSE-value'}).get_text()
    range  = soup.find('td', attrs={'data-test': 'DAYS_RANGE-value'}).get_text()
    sentence = 'The current volume of ' + name + ' is ' +  volume + '\n'
    sentence += 'The open value today of ' + name + ' is ' +  open + '\n'
    sentence += 'The previous close value of ' + name + ' is ' +  prev_close + '\n'
    sentence += 'The range of ' + name + ' is ' + range
    return sentence

# Draws and downloads the graph of the requested stock
def getGraph(stock_name):
    soup = scrape_hist(stock_name)
    name = get_name(soup)
    if(soup == "Does not exist"):
        return "I don't think this stock exists"
    dates = []
    prices = []
    data = soup.findAll('td', 'Py(10px) Ta(start) Pend(10px)')
    for item in data:
        dates.append(item.get_text())
    dates.reverse()
    price = soup.findAll('td', 'Py(10px) Pstart(10px)')
    i = 3
    while i < price.__len__():
        prices.append(price[i].get_text())
        i += 6
    prices.reverse()
    plt.plot(dates,prices)
    plt.title('Stock Price Change of ' + name)
    plt.ylabel("Stock Price in USD ")
    plt.xlabel("Dates (from months to years)")
    ax = plt.gca()
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    plt.savefig('plot.png', dpi=100)
    return prices
