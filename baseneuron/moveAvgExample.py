#coding=utf-8
#author: pans
import pandas as pd
import numpy as np
import time

#用到所有所需的参数的命名必须统一
#'OpenTime','Open','High','Low','Close','Volume'
#交易模块必须返回以下条件之一
#buy 买入
#sell 卖出
#shortbuy 做空买入
#shortsell 做空卖出
#none 无需操作

def simuTrade(dataFrm):
    priceFrm = dataFrm.copy()
    priceFrm['MA_5'] = priceFrm['Close'].rolling(5).mean()
    priceFrm['MA_10'] = priceFrm['Close'].rolling(10).mean()
    if priceFrm.loc[len(priceFrm)-1,'MA_5'] > priceFrm.loc[len(priceFrm)-1,'MA_10']:
        return 'buy'
    elif priceFrm.loc[len(priceFrm)-1,'MA_5'] < priceFrm.loc[len(priceFrm)-1,'MA_10']:
        return 'sell'
    else:
        return 'none'

