#coding=utf-8
#author: pans
import pandas as pd
import numpy as np
import time

#this is an example
#用到所有所需的参数的命名必须统一
#'OpenTime','Open','High','Low','Close','Volume'
#buy和sell必须有返回True或者False

def buy(priceFrm):
    return len(priceFrm)%4 == 0

def sell(priceFrm):
    return len(priceFrm)%3 == 0

