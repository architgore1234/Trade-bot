import yfinance
import pandas
import numpy

'''reads portfolio file and declares tables'''
p = (open('portfolio4').read()).split()
np = []
table1 = pandas.DataFrame()
table2 = pandas.DataFrame()
table3 = pandas.DataFrame()

'''for table1'''
'''retrieves close prices'''
for x in p:
    y = ((pandas.DataFrame(yfinance.Ticker(x).history(period="3mo")))['Close'])
    table1[x] = y
'''removes rows with NaN values'''
table1.dropna(axis='index', inplace=True)
'''table2 will use the data from table;1, but without the last two rows that I will add. So this is a copy without the two rows for table2'''
table1temp = table1
'''appending the values fo the row I wan to add to the table in order to a list and then joinign the list to the table; for the second last ow in the first table'''
z = []
for x in table1.columns:
    y = ((((table1[x][(len(table1[x]))-1])/(table1[x][0]))-1)*100)
    z.append(y)
data = {p[0]: [z[0]], p[1]: [z[1]], p[2]: [z[2]], p[3]: [z[3]], p[4]: [z[4]]}
data = (pandas.DataFrame.from_dict(data))
w = pandas.concat([table1, data])
'''the same as above, but for the last row in the first table'''
d = []
for x in w.columns:
    h = 100*(1 + ((table1[x][(len(table1[x]))-1])/100))
    d.append(h)
tata = {p[0]: [d[0]], p[1]: [d[1]], p[2]: [d[2]], p[3]: [d[3]], p[4]: [d[4]]}
tata = pandas.DataFrame.from_dict(tata)
table1 = pandas.concat([w, tata])

'''for tabe2; this loops over a comand that ads return percent to a table column by column'''
n = 0
while n <= 4:
    table2[table1.columns[n]] = (((table1temp[table1temp.columns[n]]/table1temp[table1temp.columns[n]].shift(1))-1)*100)
    n = n + 1

'''tale3'''
'''column 1; average of daily return percent'''
table3['portfolio daily return'] = (table2[table2.columns[0]] + table2[table2.columns[1]] + table2[table2.columns[2]] + table2[table2.columns[3]] + table2[table2.columns[4]])/5
'''column 2;; cdf of column 1, plus starting price (100)'''
table3['portfolio growth'] = (numpy.cumsum(table3['portfolio daily return'])) + 100

table3 = table3.reset_index()

avgreturn = table3['portfolio daily return'].mean() * 252
riskfreerate = 1.5
volatlity = table3['portfolio daily return'].std() * numpy.sqrt(252)
downside_deviation = (table3[table3['portfolio daily return'] < 0]['portfolio daily return']).std() * numpy.sqrt(252)
sharpratio = (avgreturn-riskfreerate)/volatlity
sortino_ratio = (avgreturn-riskfreerate)/downside_deviation
print(sharpratio)
print(sortino_ratio)
data = table3[table3.columns[1]]
mean = data.mean()
std = data.std()
daily_var = (mean-(std*2))
yearly_var = daily_var*numpy.sqrt(252)
print(yearly_var)