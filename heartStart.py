#coding=utf-8
#author: pans
import sys
import pandas as pd

sys.path.append("./baseneuron")
sys.path.append("./EventCallBack")

from EventNotifier import *
from blood import *

DEFAULT_LOCALDATA = True

def heartBeatFromLocal(orgen):
    import baseInput as base
    data = base.getDatabyType(base.CoinType.bi_xrp,base.TimeType.h4)
    print(data)
    for indexs in data.index:
        OnHeartBeat(data.loc[0:indexs,:])

def heartBeatFromInter(organ):
    pass

if __name__ == '__main__':
    print("heart start")
    blood = Blood()
    organ = blood.getOrgan()

    if DEFAULT_LOCALDATA:
        heartBeatFromLocal(organ)
    else:
        heartBeatFromInter(organ)
