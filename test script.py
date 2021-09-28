import pandas
import yfinance
from scipy.stats import norm
import matplotlib.pyplot as plt

p = (open('stocklist').read()).split('\n')
print(p)