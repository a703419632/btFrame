#coding=utf-8
#author: pans
import pandas as pd
import numpy as np
import time

#this is an example
#用到所有所需的参数的命名必须统一
#'OpenTime','Open','High','Low','Close','Volume'
#交易模块必须返回以下条件之一
#buy 买入
#sell 卖出
#shortbuy 做空买入
#shortsell 做空卖出
#none 无需操作


def simuTrade(priceFrm):
    if len(priceFrm)%4 == 0:
        return 'buy'
    elif len(priceFrm)%3 == 0:
        return 'sell'
    else:
        return 'none'

