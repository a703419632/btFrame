#coding=utf-8
import pandas as pd
import numpy as np
import time

#用到所有所需的参数的命名必须统一
#'OpenTime','Open','High','Low','Close','Volume'
#buy和sell必须有返回True或者False

def buy(dataFrm):
    priceFrm = dataFrm.copy()
    priceFrm['MA_5'] = priceFrm['Close'].rolling(5).mean()
    priceFrm['MA_10'] = priceFrm['Close'].rolling(10).mean()

    return priceFrm.loc[len(priceFrm)-1,'MA_5'] > priceFrm.loc[len(priceFrm)-1,'MA_10']



def sell(dataFrm):
    priceFrm = dataFrm.copy()
    priceFrm['MA_5'] = priceFrm['Close'].rolling(5).mean()
    priceFrm['MA_10'] = priceFrm['Close'].rolling(10).mean()

    return priceFrm.loc[len(priceFrm)-1,'MA_5'] < priceFrm.loc[len(priceFrm)-1,'MA_10']

