import yfinance
import pandas
import os

p = open('portfolio3').read().split()
np = []

for x in p:
    print('sell', x)

"""
for ticker in p:
    data = (pandas.DataFrame(yfinance.Ticker(ticker).history(period="2y")))['Close']
    if (data[len(data.index)-91:].max()/10)*8 > data[((len(list(data.index)))-1)]:
        print('sell:', ticker)
    else:
        np.append(ticker)
"""

def getStockList():
    """this function returns list of stocks which has data for at least 50 days"""
    x = (open('stocklist').read()).split('\n')
    listOfStocks = []
    for s in x:
        if not s in listOfStocks:
            listOfStocks.append(s)
    listOfStockss = []
    for l in listOfStocks:
        if len((pandas.DataFrame(yfinance.Ticker(l).history(period="3mo")))['Close'].index()) > 50:
            listOfStockss.append(l)
    return listOfStockss

def returnrank(lis):
    li = {}
    lit = []
    for x in lis:
        data = (pandas.DataFrame(yfinance.Ticker(x).history(period="3mo")))['Close']
        li[x] = (((data[(len(data.index)) - 1]) - (data[0])) / (data[0]))
    li = ({k: v for k, v in sorted(li.items(), key=lambda item: item[1])})
    li = ((list(li.items()))[((len(li.items())) - 50):(len(li.items()))])
    for y in li:
        lit.append(y[0])
    return lit
n = 0
for x in returnrank(getStockList()):
    if not n >= (10 - len(np)):
        print('buy', x)
        np.append(x)
        n = n + 1
os.remove('portfolio3')
f = open('portfolio3', 'w+')
for d in np:
    f.write(' ' + d)