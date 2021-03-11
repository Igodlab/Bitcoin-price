# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

### 
###

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

## Data merger for iPython

## 1.1) Bitcoin data kaggle (from 2016 to 2021)
data0 = pd.read_csv("BTC-USD (1).csv")


## 1.2) load bitstamp data (from 2012 to 2020)
data = pd.read_csv("bitstampUSD_1-min_data_2012-01-01_to_2020-12-31.csv")
data["Date"] = [datetime.utcfromtimestamp(int(ttt)) for ttt in data["Timestamp"]]

## 1.3) subsample daily data
def _daily_(x, cc="Date"):
    idx = []
    n, m = np.shape(x)  ## data dimensions
    for iidd, xi in enumerate(x[cc]):
        if (xi. hour == 0) and (xi.minute == 0) and (xi.second == 0):
            idx.append(iidd)
            
    df = x.iloc[idx]
    return df.reset_index().drop("index", axis=1)
    
    
## daily data
Xday0 = _daily_(data)


## 1.4) merge daily datasets (bitstamp and kaggle)
for ni, i in enumerate(data0["Date"]): 
    if (str(data0["Date"][ni]) == str(Xday0["Date"].iloc[[-1]].values[0])[:10]):
        idx_merge = ni
        
## change column name
Xday0.rename(columns={"Volume_(Currency)":"Volume"}, inplace = True)
a1 = Xday0[["Date", "Open", "High", "Low", "Close", "Volume"]]
a2 = data0.iloc[range(idx_merge+1, data0.index[-1]+1)][["Date", "Open", "High", "Low", "Close", "Volume"]]

Xday = pd.concat([a1, a2])
Xday = Xday.reset_index().drop("index", axis=1)

## convert all dates to datetime.datetime
DT = []
for dt in Xday["Date"]:
    if (len(str(dt)) < 19):
        dti = datetime.strptime(str(dt)+ " 00:00:00", '%Y-%m-%d %H:%M:%S')
        DT.append(dti)
    else:
        dti = datetime.strptime(str(dt), '%Y-%m-%d %H:%M:%S')
        DT.append(dti)
        
Xday["Date"] = DT  ## all date values are datetime.datetime


## 1.5) load s&p500
SP = pd.read_csv("SP500.csv")

## convert time to same format of Bitcoin data
SP["Date"] = [datetime.strptime(dte+" 00:00:00", '%Y-%m-%d %H:%M:%S') for dte in SP["Date"]]
SP.tail()


## nan padder
def pad_nan(x, cc="Close", t0=Xday["Date"][Xday.iloc[[0]].index[0]], tf=Xday["Date"][Xday.iloc[[-1]].index[0]]):
    xd = x["Date"]
    BTC = Xday["Date"]

    #df = pd.DataFrame(np.nan, index=list(range(t0, tf)), columns=cc)
    idx = []
    
    for i in range(len(BTC)):
        try:
            iid = x[cc][xd == BTC[i]].index[0]
            val = x[cc].iloc[[iid]]
            idx.append(float(val))
        except:
            idx.append(np.nan)
            
    #price = x["Close"].iloc[[idx]]
    return idx#pd.DataFrame(price, columns=cc)
    
    
Xday["SP500"] = pad_nan(SP)


## 1.6) compute S2F to our Dataset
## truncate S2F time range so that it matches BTC price
def time_truncate(x, t0=Xday["Date"][Xday.iloc[[0]].index[0]], tf=Xday["Date"][Xday.iloc[[-1]].index[0]]):
    cdate = "Date"
    ii0, ii0_found = 0, False
    iif, iif_found = 0, False
    for ni, i in enumerate(x[cdate]):
        if (ii0_found == False) and (i == t0):
            ii0_found = True
            ii0 = ni
        elif (iif_found == False) and (i == tf):
            iif_found = True
            iif = ni+1
        
        if (ii0 == True) and (iif == True):
            break
    
    df = x.iloc[list(range(ii0,iif))]
    return df.reset_index().drop("index", axis=1)
    
    
## dates of genesis and last block
base0 = datetime.strptime("2009-1-3 00:00:00", '%Y-%m-%d %H:%M:%S')
baseF = datetime.strptime("2140-1-3 00:00:00", '%Y-%m-%d %H:%M:%S')

## halving dates 
halv0 = datetime.strptime("2012-11-28 00:00:00", '%Y-%m-%d %H:%M:%S')
halv1 = datetime.strptime("2016-7-9 00:00:00", '%Y-%m-%d %H:%M:%S')
halv2 = datetime.strptime("2020-5-15 00:00:00", '%Y-%m-%d %H:%M:%S')

mhalv = [(halv0 - base0).days, (halv1 - halv0).days, (halv2 - halv1).days]
mhalv = int(round(np.mean(mhalv), 0))  ## mean halving time in days


## create date variable from genesis block to last bitcon creation
s2f_time = [base0]

i = 0
ddd = False
next0 = base0

while ddd == False:
    if (next0 != baseF):
        i += 1
        next0 = base0 + timedelta(days=i)
        s2f_time.append(next0)
    else:
        ddd = True


## compute Bitcoins per block
Bpb = 51.93494777042 ## Bitcoins-per-block mined pre-halving era
BTCp = [] ## Bitcoins produced
BTCf = []  ## yearly flow
min_in_day = 6*24 ## number of 10-minutes in a day
ref_day = base0 ## reference day
hlv = halv0

for b in range(len(s2f_time)):
    ref_day = base0 + timedelta(days=b)
    if (ref_day == hlv):
        Bpb = Bpb/2  ## decrease by one-half
        hlv = hlv + timedelta(days=mhalv)
    BTCp.append(min_in_day*Bpb)
    BTCf.append(min_in_day*365*Bpb)
    

## Bitcoins in stock
BTCstock = np.cumsum(BTCp)
BTCflow = BTCf
BTC_S2F = BTCstock/BTCflow

## convert to dataframe
BTCs = pd.DataFrame({"Date": s2f_time, "BTC_mined": BTCp, "BTC_stock": BTCstock, "BTC_flow": BTCflow, "S2F": BTC_S2F})    

## 1.7) add S2F to master dataset
BTCs_chopped = time_truncate(BTCs)
Xday[["S2F", "BTC_stock"]] = BTCs_chopped[["S2F", "BTC_stock"]]


## 2. Save Xday (Master dataset) and save BTCs (Bticoins mined, Bitcoin S2F)
Xday.to_csv("BTC.csv")
BTCs.to_csv("BTCs2f.csv")