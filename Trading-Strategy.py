# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#'docker run --rm -p 8888:8888 \
 #      rpy2/rpy2:2.8.x

import csv
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from statsmodels.tsa.arima_model import ARIMA 
from statsmodels.tsa.arima_model import ARIMAResults
from statsmodels.tsa.stattools import adfuller

#If R starts working here, then do apply these
#import rpy2 as rp 
#import rpy2.objects as robj
#from robj.packages import importr as impr
#base = impr('base')
#utils = impr('utils')

#Set up of dictionaries and equities
inteq = 'GLD'
hedge = 'INTC'
mktBIC = {}
hedgeBIC = {}
equitypath = 'C:/Users/Nikita/Documents/Trading-Strategy/' 
toteq = equitypath + inteq +'.csv'

    
def csvset(file):
    global p_log
    datemake = lambda dates: pd.datetime.strptime(dates, '%m/%d/%Y')
    daten = pd.read_csv(file, parse_dates=True, index_col='Date',date_parser=datemake)
    # ADD BRACKETS AFTER ADJ CLOSE FOR CHOOSING YOUR SAMPLE 
    p = daten['Adj Close'][1:60]
    p_log = np.log(p)
    

#Dickey-Fuller to test for stationarity
def acfpacfdf(data):
    global dftest
    global d
    dftest = float(adfuller(data)[1])
    if dftest > float(0.05):
        d = 1
    else:
        d = 0
    
#Multi-Use automatically choosing the best BIC
def bestBIC(bic):
    global min_BIC
    min_BIC = min(bic, key=bic.get)

#Allocating the Best ARIMA    
def bestarima(model):
    global bestmodel
    if str(model[0:1]) == "AR":
        a = int(model[4])
        m = 0
    else:
        a = 0
        m = int(model[4]) 
    model = ARIMA(p_log, order=(a,d,m))
    bestmodel = model.fit(disp=-1)

#ARIMA Function    
def arimaTest(l_eq):
    for i in range(1,6):    
        ar = ARIMA(l_eq, order=(i,d,0))
        arfit = ar.fit(disp=-1)
        arresults = ARIMAResults.bic(arfit)
        mktBIC["AR (" + str(i) + ")"] = arresults
    for i in range(1,6):
        ma = ARIMA(l_eq, order=(0,d,i))
        mafit = ma.fit(disp=-1)
        maresults = ARIMAResults.bic(mafit)
        mktBIC["MA (" + str(i) + ")"] = maresults
        
def predict(model):
    global fore
    fore = model.predict(1,100)
    

def archTest(l_eq):
    pass
    


 #for i in range(1,len(['Date'])):     
csvset(toteq)
acfpacfdf(p_log)
arimaTest(p_log)
bestBIC(mktBIC)
bestarima(min_BIC)
print (min_BIC)
plt.plot(p_log - p_log.shift())
plt.plot(bestmodel.fittedvalues, color='red')
predict(bestmodel)
print (fore[100])


#eqpredict = pd.Series(bestmodel.fittedvalues, copy=True)
#print (eqpredict.head())