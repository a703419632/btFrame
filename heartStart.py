#coding=utf-8
#author: pans
import sys
import pandas as pd
import threading
import time

sys.path.append("./baseneuron")
sys.path.append("./EventCallBack")

from blood import *

DEFAULT_LOCALDATA = True

def heartBeatFromLocal(blood):
    organ = blood.getOrgan()

#    这边可以导入自己本地的数据，注意统一列名'OpenTime','Open','High','Low','Close','Volume'
#    import baseInput as base
#    data = base.getDatabyType(base.CoinType.bi_xrp,base.TimeType.h4)
    data = pd.read_hdf('bi_xrp_h4.h5','priceInfo')
    print(data)

    for indexs in data.index:
        if indexs <= 1:
            continue

        blood.eventManager.SendEvent('OnHeartBeat',data.loc[0:indexs])

def heartBeatFromInter(blood):
    t = threading.Thread(target=updateOrgan, args=(blood,3))
    t.start()

    while(1):
        time.sleep(3)
        blood.eventManager.SendEvent('OnHeartBeat')
    pass

def updateOrgan(blood,interval):
    while(1):
        organ = blood.getOrgan()
        time.sleep(interval)
    

if __name__ == '__main__':
    print("heart start")
    blood = Blood()

    if DEFAULT_LOCALDATA:
        heartBeatFromLocal(blood)
    else:
        heartBeatFromInter(blood)
