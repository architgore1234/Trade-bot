import yfinance
import pandas
import numpy
import os
import datetime
import matplotlib.pyplot as plt

def strategy1 (timeStart, timeEnd):
    portfoliomax = 5
    qualifyrank = 100
    minindex = 50
    p = (open('portfolio1').read()).split()
    np = []
    for x in p:
        data = (pandas.DataFrame(yfinance.download(x, start=timeStart, end=timeEnd)))
        if data['Close'].mean() > data['Close'][((len(data['Close'].index)) - 16):].mean():
            print('sell', x)
        else:
            np.append(x)

    def getStockList():
        """this function returns list of stocks which has data for at least 50 days"""
        listOfStocks = []
        for l in (open('stocklist').read()).split('\n'):
            if len((pandas.DataFrame(yfinance.download(l, start=timeStart, end=timeEnd)))['Close']) > minindex:
                listOfStocks.append(l)
        return listOfStocks

    def sdratio(y):
        """return over standard deviation"""
        flist = {}
        for stock in y:
            data = (pandas.DataFrame(yfinance.download(stock, start=timeStart, end=timeEnd)))['Close']
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
            data = (pandas.DataFrame(yfinance.download(x, start=timeStart, end=timeEnd)))['Close']
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
            data = (pandas.DataFrame(yfinance.download(x, start=timeStart, end=timeEnd)))['Close']
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
    x = rr

    for x in rr:
        if x in mr and x in sdr:
            if not x in np:
                if not len(np)-1 <= portfoliomax:
                    print('buy', x)
                    np.append(x)
                    n = n + 1
    n = 0
    if not len(np) >= 5:
        for x in rr:
            if not x in sdr:
                if not x in np:
                    if not len(np)-1 <= portfoliomax:
                        print('buy', x)
                        np.append(x)
    n = 0
    if not len(np) >= 5:
        for x in rr:
            if not x in mr:
                if not x in np:
                    if not len(np)-1 <= portfoliomax:
                        print('buy', x)
                        np.append(x)
    n = 0
    if not len(np) >= 5:
        for x in rr:
            if not x in np:
                if not len(np)-1 <= portfoliomax:
                    print('buy', x)
                    np.append(x)

    os.remove('portfolio1')
    f = open('portfolio1', 'w+')
    for d in np:
        f.write(' ' + d)
    return [np, timeStart, timeEnd]

def strategy2 (timeStart1, timeEnd1):
    p = (open('portfolio2').read()).split()
    np = []

    def getStockList():
        x = (open('stocklist').read()).split('\n')
        listOfStocks = []
        for s in x:
            if not s in listOfStocks:
                listOfStocks.append(s)
        return listOfStocks

    for x in p:
        data = (pandas.DataFrame(yfinance.download(x, start=timeStart1, end=timeEnd1)))
        if data['Close'].mean() > data['Close'][((len(data['Close'].index)) - 16):].mean():
            print('sell', x)
        else:
            np.append(x)

    for x in getStockList():
        if len(np) < 5:
            data = (pandas.DataFrame(yfinance.download(x, start=timeStart1, end=timeEnd1)))
            if data['Close'].mean() < data['Close'][((len(data['Close'].index)) - 16):].mean():
                print('buy', x)
                np.append(x)

    os.remove('portfolio2')
    f = open('portfolio2', 'w+')
    for d in np:
        f.write(' ' + d)
    return [np, timeStart1, timeEnd1]

def strategy3 (timeStart2, timeEnd2):
    p = open('portfolio3').read().split()
    np = []

    for x in p:
        print('sell', x)

    def getStockList():
        """this function returns list of stocks which has data for at least 50 days"""
        x = (open('stocklist').read()).split('\n')
        listOfStocks = []
        print('in loop 1')
        for s in x:
            if not s in listOfStocks:
                listOfStocks.append(s)
        listOfStockss = []
        print('returning')
        return listOfStocks

    def returnrank(lis):
        li = {}
        lit = []
        for x in lis:
            data = (pandas.DataFrame(yfinance.download(x, start=timeStart2, end=timeEnd2)))['Close']
            li[x] = (((data[(len(data.index)) - 1]) - (data[0])) / (data[0]))
        li = ({k: v for k, v in sorted(li.items(), key=lambda item: item[1])})
        li = ((list(li.items()))[((len(li.items())) - 50):(len(li.items()))])
        for y in li:
            lit.append(y[0])
        return lit

    n = 0
    print('getting stocklist')
    stocklistbrrr = getStockList()
    print('getting return rank')
    for x in returnrank(stocklistbrrr):
        print('buying')
        if not n >= (10 - len(np)):
            print('buy', x)
            np.append(x)
            n = n + 1
    print('updating portfolio')
    os.remove('portfolio3')
    f = open('portfolio3', 'w+')
    for d in np:
        f.write(' ' + d)
    return [np, timeStart2, timeEnd2]

def theMightyThree (listofthree, prevvalue):
    port = listofthree[0]
    timeS = listofthree[1]
    timeE = listofthree[2]

    '''reads portfolio file and declares tables'''
    p = port
    np = []
    table1 = pandas.DataFrame()
    table2 = pandas.DataFrame()
    table3 = pandas.DataFrame()

    '''for table1'''
    '''retrieves close prices'''
    for x in p:
        y = (pandas.DataFrame((yfinance.download(x, start=timeS, end=timeE))['Close']))
        table1[x] = y
    '''removes rows with NaN values'''
    table1.dropna(axis='index', inplace=True)
    '''table2 will use the data from table;1, but without the last two rows that I will add. So this is a copy without the two rows for table2'''
    table1temp = table1
    '''appending the values fo the row I wan to add to the table in order to a list and then joinign the list to the table; for the second last ow in the first table'''
    z = []
    for x in table1.columns:
        y = ((((table1[x][(len(table1.index)) - 1]) / (table1[x][1])) - 1) * 100)
        z.append(y)
    data = {p[0]: [z[0]], p[1]: [z[1]], p[2]: [z[2]], p[3]: [z[3]], p[4]: [z[4]]}
    data = (pandas.DataFrame.from_dict(data))
    w = pandas.concat([table1, data])
    '''the same as above, but for the last row in the first table'''
    d = []
    for x in w.columns:
        h = 100 * (1 + ((table1[x][(len(table1[x])) - 1]) / 100))
        d.append(h)
    tata = {p[0]: [d[0]], p[1]: [d[1]], p[2]: [d[2]], p[3]: [d[3]], p[4]: [d[4]]}
    tata = pandas.DataFrame.from_dict(tata)
    table1 = pandas.concat([w, tata])

    '''for tabe2; this loops over a comand that ads return percent to a table column by column'''
    n = 0
    while n <= 4:
        table2[table1.columns[n]] = (
                    ((table1temp[table1temp.columns[n]] / table1temp[table1temp.columns[n]].shift(1)) - 1) * 100)
        n = n + 1

    '''tale3'''
    '''column 1; average of daily return percent'''
    table3['portfolio daily return'] = (table2[table2.columns[0]] + table2[table2.columns[1]] + table2[
        table2.columns[2]] + table2[table2.columns[3]] + table2[table2.columns[4]]) / 5
    '''column 2;; cdf of column 1, plus starting price (100)'''
    table3['portfolio growth'] = (numpy.cumsum(table3['portfolio daily return'])) + prevvalue
    prevvalue = table3['portfolio growth'][(len(table3['portfolio growth']) - 1)]
    table3temp = table3['portfolio growth']
    table3 = table3.reset_index()

    avgreturn = table3['portfolio daily return'].mean() * 252
    riskfreerate = 1.5
    volatlity = table3['portfolio daily return'].std() * numpy.sqrt(252)
    downside_deviation = (table3[table3['portfolio daily return'] < 0]['portfolio daily return']).std() * numpy.sqrt(
        252)
    sharpratio = (avgreturn - riskfreerate) / volatlity
    sortino_ratio = (avgreturn - riskfreerate) / downside_deviation
    print(sharpratio)
    print(sortino_ratio)
    data = table3[table3.columns[1]]
    mean = data.mean()
    std = data.std()
    daily_var = (mean - (std * 2))
    yearly_var = daily_var * numpy.sqrt(252)
    print(yearly_var)
    return [table3temp, prevvalue]



















x = 0
y = 2
n = 0
prevvalue = 100
while n < y:
    if x == 0:
        print('starting dataframe1')
        dataframe1 = theMightyThree((strategy1((datetime.date.today() - datetime.timedelta(30 * y)), (datetime.date.today() - datetime.timedelta(30 * (y - 1))))), prevvalue)
        prevvalue = dataframe1[1]
        dataframe1 = dataframe1[0]
        x = 1
        print('dataframe1 completed')
    else:
        print('starting dataframe2')
        dataframe2 = (theMightyThree((strategy1((datetime.date.today() - datetime.timedelta(30 * n)), (datetime.date.today() - datetime.timedelta(30 * (n - 1))))), prevvalue))
        prevvalue = dataframe2[1]
        dataframe2 = dataframe2[0]
        print('concating')
        dataframe1 = pandas.concat([dataframe1, dataframe2])
        print('done')
    n = n + 1
print('ploting')
plt.plot(dataframe1)

x = 0
y = 2
n = 0
prevvalue = 100
while n < y:
    if x == 0:
        print('starting dataframe1')
        dataframe1 = theMightyThree((strategy2((datetime.date.today() - datetime.timedelta(30 * y)), (datetime.date.today() - datetime.timedelta(30 * (y - 1))))), prevvalue)
        prevvalue = dataframe1[1]
        dataframe1 = dataframe1[0]
        x = 1
        print('dataframe1 completed')
    else:
        print('starting dataframe2')
        dataframe2 = (theMightyThree((strategy2((datetime.date.today() - datetime.timedelta(30 * n)), (datetime.date.today() - datetime.timedelta(30 * (n - 1))))), prevvalue))
        prevvalue = dataframe2[1]
        dataframe2 = dataframe2[0]
        print('concating')
        dataframe1 = pandas.concat([dataframe1, dataframe2])
        print('done')
    n = n + 1
print('ploting')
plt.plot(dataframe1)

x = 0
y = 2
n = 0
prevvalue = 100
while n < y:
    if x == 0:
        print('starting dataframe1')
        dataframe1 = theMightyThree((strategy3((datetime.date.today() - datetime.timedelta(30 * y)), (datetime.date.today() - datetime.timedelta(30 * (y - 1))))), prevvalue)
        prevvalue = dataframe1[1]
        dataframe1 = dataframe1[0]
        x = 1
        print('dataframe1 completed')
    else:
        print('starting dataframe2')
        dataframe2 = (theMightyThree((strategy3((datetime.date.today() - datetime.timedelta(30 * n)), (datetime.date.today() - datetime.timedelta(30 * (n - 1))))), prevvalue))
        prevvalue = dataframe2[1]
        dataframe2 = dataframe2[0]
        print('concating')
        dataframe1 = pandas.concat([dataframe1, dataframe2])
        print('done')
    n = n + 1
print('ploting')
plt.plot(dataframe1)

plt.legend(['strategy1', 'strategy2', 'strategy3'])
plt.show()