#coding=utf-8
#author: pans
import pandas as pd
import numpy as np
import time

'''
@@这是一个简单的做空例子


用到所有所需的参数的命名必须统一
'OpenTime','Open','High','Low','Close','Volume'
交易模块必须返回以下条件之一
buy 买入
sell 卖出
shortbuy 做空借币
shortsell 做空还币
none 无需操作
'''

def simuTrade(priceFrm):
    if len(priceFrm)%7 == 0:
        return 'shortsell'
    elif len(priceFrm)%6 == 0:
        return 'shortbuy'
    else:
        return 'none'

