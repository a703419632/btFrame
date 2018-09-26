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
        if indexs <= 2:
            continue

        blood.eventManager.SendEvent('OnHeartBeat_btcusdt_1m',data.loc[0:indexs])

oldorgan = {}
def heartBeatFromInter(blood):
    global oldorgan
    organ = blood.getOrgan()
    oldorgan = organ.copy()
    from binance.client import Client
    from binance.websockets import BinanceSocketManager
#    from binance.enums import *

    client = Client("","")
    bm = BinanceSocketManager(client)  

    def process_message(msg):
        proc_msg = msg['data']
        proc_msg["ts"] = int(time.time())
        _stream = msg['stream']
        symbol = proc_msg['k']['s'].upper()
        ti = proc_msg['k']['i']

        rawdata = DataFrame(client.get_historical_klines(symbol, ti,'7 days ago'),columns=['t','o','h','l','c','v','T','q','n','V','Q','B'])
#        print('rawdata:',rawdata)
        dealed = dealData(rawdata)
#        print('dealeddata',dealed)

        blood.eventManager.SendEvent('OnHeartBeat_%s_%s' % (symbol.lower(),ti),dealed)
        return

    stream_arr = []
    coin_arr = blood.getCoinArr()
    time_arr = blood.getTimeArr()

    for symbol in coin_arr:
        for ti in time_arr:
            _stream = "%s@kline_%s" % (symbol,ti)
            stream_arr.append(_stream)

    conn_key = bm.start_multiplex_socket(stream_arr, process_message)

    bm.start()

    def updateOrgan(blood,interval):
        global oldorgan
        while(1):
            organ = blood.getOrgan()
            if oldorgan != organ:
                bm.close()
                oldorgan = organ.copy()

                stream_arr = []
                coin_arr = blood.getCoinArr()
                time_arr = blood.getTimeArr()
                print(coin_arr,time_arr) 
                for symbol in coin_arr:
                    for ti in time_arr:
                        _stream = "%s@kline_%s" % (symbol,ti)
                        stream_arr.append(_stream)
            
                conn_key = bm.start_multiplex_socket(stream_arr, process_message)
                
                print('webstock connect start')
                bm.run()              
                print('restart net-connect************************************')            
            #test
            #process_message({'stream': 'btcusdt@kline_1m', 'data': {'e': 'kline', 'E': 1537497960109, 's': 'BTCUSDT', 'k': {'t': 1537497900000, 'T': 1537497959999, 's': 'BTCUSDT', 'i': '1m', 'f': 71119541, 'L': 71121042, 'o': '6518.25000000', 'c': '6555.01000000', 'h': '6560.00000000', 'l': '6511.48000000', 'v': '342.35654500', 'n': 1502, 'x': True, 'q': '2239903.81360292', 'V': '274.28551500', 'Q': '1794654.80281245', 'B': '0'}}})

            time.sleep(interval)
        return

    t = threading.Thread(target=updateOrgan, args=(blood,3))
    t.start()
    
def dealData(data):
    data['c'] = data['c'].astype('float64')
    data['h'] = data['h'].astype('float64')
    data['l'] = data['l'].astype('float64')
    data['v'] = data['v'].astype('float64')
    data['o'] = data['o'].astype('float64')

    data['OpenTime'] = data['t']
    data['Open'] = data['o']
    data['High'] = data['h']
    data['Low'] = data['l']
    data['Close'] = data['c']
    data['Volume'] = data['v']
    return data

if __name__ == '__main__':
    print("heart start")
    blood = Blood()

    if DEFAULT_LOCALDATA:
        heartBeatFromLocal(blood)
    else:
        heartBeatFromInter(blood)
