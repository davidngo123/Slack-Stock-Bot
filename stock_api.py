import yfinance as yf




try:
  msft = yf.Ticker("MSFTTTTT")
  todayData = msft.history(period='1d')
  print(todayData['Close'][0])
except:
  print("An exception occurred")