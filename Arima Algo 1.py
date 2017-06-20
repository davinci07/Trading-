# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARIMAResults

    
#Set up of dictionaries and equity iteration
mktBIC = {}
hedgeBIC = {}
mktequity = 'C:/Users/Nikita/Documents/FDP/ADSK.csv'
hedgeequity  = 'C:/Users/Nikita/Documents/FDP/INTC.csv'

datemake = lambda dates: pd.datetime.strptime(dates, '%m/%d/%Y')
daten = pd.read_csv(mktequity, parse_dates=True, index_col='Date',date_parser=datemake)
p = daten['Adj Close'] 
p_log = np.log(p)
plt.plot(p_log)

def arimaTest(l_eq):
    for i in range(1,6):    
        ar = ARIMA(l_eq, order=(i,1,0))
        arfit = ar.fit(disp=-1)
        arresults = ARIMAResults.bic(arfit)
        mktBIC["AR(" + str(i) + ")"] = arresults
    for i in range(1,6):
        ma = ARIMA(l_eq, order=(0,1,i))
        mafit = ma.fit(disp=-1)
        maresults = ARIMAResults.bic(mafit)
        mktBIC["MA(" + str(i) + ")"] = maresults
        
#bestARIMA = min(mktBIC, key=mktBIC.get)
    

        
arimaTest(p_log)
#print bestARIMA
print mktBIC