import yfinance
import pandas
import os

p = (open('portfolio2').read()).split()
np = []

def getStockList():
    x = (open('stocklist').read()).split('\n')
    listOfStocks = []
    for s in x:
        if not s in listOfStocks:
            listOfStocks.append(s)
    listOfStockss = []
    for l in listOfStocks:
        if len((pandas.DataFrame(yfinance.Ticker(l).history(period="2y")))['Close'].index()) > 50:
            listOfStockss.append(l)
    return listOfStockss

for x in p:
    data = (pandas.DataFrame(yfinance.Ticker(x).history(period="2y")))
    if data['Close'].mean() > data['Close'][((len(data['Close'].index))-16):].mean():
        print('sell', x)
    else:
        np.append(x)

for x in getStockList():
    if len(np) < 5:
        data = (pandas.DataFrame(yfinance.Ticker(x).history(period="2y")))
        if data['Close'].mean() < data['Close'][((len(data['Close'].index))-16):].mean():
            print('buy', x)
            np.append(x)

os.remove('portfolio2')
f = open('portfolio2', 'w+')
for d in np:
    f.write(' ' + d)