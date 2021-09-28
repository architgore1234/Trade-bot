import yfinance
import pandas
import os

portfoliomax = 5
qualifyrank = 50
minindex = 50
p = (open('portfolio1').read()).split()
np = []
for x in p:
    data = (pandas.DataFrame(yfinance.Ticker(x).history(period="3mo")))
    if data['Close'].mean() > data['Close'][((len(data['Close'].index))-16):].mean():
        print('sell', x)
    else:
        np.append(x)

def getStockList():
    """this function returns list of stocks which has data for at least 50 days"""
    x = (open('stocklist').read()).split('\n')
    listOfStocks = []
    for s in x:
        if not s in listOfStocks:
            listOfStocks.append(s)
    listOfStockss = []
    for l in listOfStocks:
        if len((pandas.DataFrame(yfinance.Ticker(l).history(period="3mo")))['Close']) > minindex:
            listOfStockss.append(l)
    return listOfStockss

def sdratio(y):
    """return over standard deviation"""
    flist = {}
    for stock in y:
        data = (pandas.DataFrame(yfinance.Ticker(stock).history(period="3mo")))['Close']
        l = (((data[(len(data.index)) - 1]) - (data[0]) / (data[0])) / (((data.shift(-1) - data).std(ddof=1)) * 63))
        flist[stock] = l
    flist = ({k: v for k, v in sorted(flist.items(), key=lambda item: item[1])})
    flist = ((list(flist.items()))[((len(flist.items())) - qualifyrank):(len(flist.items()))])
    dlist = []
    for obj in flist:
        dlist.append(obj[0])
    return dlist

def maxdrawratio(z):
    maxlist = []
    ratiolist = {}
    n = 0
    for x in z:
        data = (pandas.DataFrame(yfinance.Ticker(x).history(period="3mo")))['Close']
        for point in data:
            for p in data[n:]:
                maxlist.append((point - p))
            n = n + 1
        ratiolist[x] = (min(maxlist) / (((data[(len(data.index)) - 1]) - (data[0])) / (data[0])))
    ratiolist = ({k: v for k, v in sorted(ratiolist.items(), key=lambda item: item[1])})
    return ((list(ratiolist))[0:qualifyrank])

def returnrank(lis):
    li = {}
    lit = []
    for x in lis:
        data = (pandas.DataFrame(yfinance.Ticker(x).history(period="3mo")))['Close']
        li[x] = (((data[(len(data.index)) - 1]) - (data[0])) / (data[0]))
    li = ({k: v for k, v in sorted(li.items(), key=lambda item: item[1])})
    li = ((list(li.items()))[((len(li.items())) - qualifyrank):(len(li.items()))])
    for y in li:
        lit.append(y[0])
    return lit

gd = getStockList()
mr = maxdrawratio(gd)
sdr = sdratio(gd)
rr = returnrank(gd)
n = 0

x = sdr
listOfStocks = []
for s in x:
    if not s in listOfStocks:
        listOfStocks.append(s)
sdr = listOfStocks

x = mr
listOfStocks = []
for s in x:
    if not s in listOfStocks:
        listOfStocks.append(s)
mr = listOfStocks

x = rr
listOfStocks = []
for s in x:
    if not s in listOfStocks:
        listOfStocks.append(s)
rr = listOfStocks

print(rr)

for x in rr:
    print('in loop 1')
    if x in mr and x in sdr:
        print('in loop 2')
        if not x in p:
            print('in loop 3')
            if not n >= ((portfoliomax) - len(np)):
                print('in loop 3')
                print('buy', x)
                np.append(x)
                n = n + 1
print('updating portfolio file')
os.remove('portfolio1')
print('portfolio file removed')
f = open('portfolio1', 'w+')
for d in np:
    f.write(' ' + d)
print('portfolio file updated')