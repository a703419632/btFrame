#coding=utf-8
#author: pans
from xml.dom.minidom import parse
import xml.dom.minidom
import pandas as pd
from pandas import DataFrame
import time

from neuron import *
from EventManager import *

class Organ(object):
    def __init__(self,data,neuronXMLDict):
        super(Organ, self).__init__()

        self.name = data.getElementsByTagName("name")[0].childNodes[0].data
        self.neuronList = data.getElementsByTagName("neuron")[0].childNodes[0].data.split(',')
        self.cointype = data.getElementsByTagName("cointype")[0].childNodes[0].data
        self.timetype = data.getElementsByTagName("timetype")[0].childNodes[0].data
        self.buytype = data.getElementsByTagName("buytype")[0].childNodes[0].data
        self.selltype = data.getElementsByTagName("selltype")[0].childNodes[0].data
        self.shortbuytype = data.getElementsByTagName("shortbuytype")[0].childNodes[0].data
        self.shortselltype = data.getElementsByTagName("shortselltype")[0].childNodes[0].data
        self.feeRatio = float(data.getElementsByTagName("feeRatio")[0].childNodes[0].data)
        self.capital = float(data.getElementsByTagName("capital")[0].childNodes[0].data)
        self.pos = float(data.getElementsByTagName("pos")[0].childNodes[0].data)
        self.buyonce = float(data.getElementsByTagName("buyonce")[0].childNodes[0].data)
        self.sellonce = float(data.getElementsByTagName("sellonce")[0].childNodes[0].data)
        self.shortsellonce = float(data.getElementsByTagName("shortsellonce")[0].childNodes[0].data)
        self.shortbuyonce = float(data.getElementsByTagName("shortbuyonce")[0].childNodes[0].data)
        self.shortmax = float(data.getElementsByTagName("shortmax")[0].childNodes[0].data)
        self.auth = data.getElementsByTagName("auth")[0].childNodes[0].data
        self.date = data.getElementsByTagName("date")[0].childNodes[0].data
        self.description = data.getElementsByTagName("description")[0].childNodes[0].data
        self.neuronDict = {}
        for neu in self.neuronList:
            if neu in neuronXMLDict:
                self.neuronDict[neu] = Neuron(neuronXMLDict[neu])

        self.shortpos = 0
        self.valRows = []
        print('a new organ is created,name:%s,auth:%s,date:%s,description:%s,time:%s' % (self.name,self.auth,self.date,self.description,time.time()))

    def getHeartBeat(self,priceFrm):
       
        print('getHeartBeat',self.cointype,self.timetype)
        result = self.tradeResult(priceFrm.loc[0:len(priceFrm)-2,:])

        openTime = priceFrm.loc[len(priceFrm)-1,'OpenTime']
        curPrice = float(priceFrm.loc[len(priceFrm)-1,'Open'])

        if result == 'buy':
            newPos = min(self.capital/(curPrice*(1+self.feeRatio)),self.buyonce) if self.buyonce>0 else self.capital/(curPrice*(1+self.feeRatio))
            self.pos += newPos
            curFee = curPrice*newPos*self.feeRatio
            self.capital -= (curPrice*newPos+curFee)
            self.valRows.append([openTime,curPrice,self.pos,self.shortpos,self.capital,curFee,'buy %s' % newPos])
        elif result == 'sell':
            sellPos = min(self.pos,self.sellonce) if self.sellonce>0 else self.pos
            curFee = curPrice*sellPos*self.feeRatio
            self.capital += (curPrice*sellPos-curFee)
            self.pos -= sellPos
            self.valRows.append([openTime,curPrice,self.pos,self.shortpos,self.capital,curFee,'sell %s' % sellPos])
        elif result == 'shortbuy':
            sellPos = min(self.shortbuyonce,self.shortmax-self.shortpos) if self.shortbuyonce>0 else (self.shortmax-self.shortpos)
            curFee = curPrice*sellPos*self.feeRatio
            self.shortpos += sellPos
            self.capital += (curPrice*sellPos-curFee)
            self.valRows.append([openTime,curPrice,self.pos,self.shortpos,self.capital,curFee,'shortbuy %s' % sellPos])
        elif result == 'shortsell':
            newPos = min(self.shortpos,self.shortsellonce) if self.shortsellonce>0 else self.shortpos
            self.shortpos -= newPos
            curFee = curPrice*newPos*self.feeRatio
            self.capital -= (curPrice*newPos+curFee)
            self.valRows.append([openTime,curPrice,self.pos,self.shortpos,self.capital,curFee,'shortsell %s' % newPos])


        DataFrame(self.valRows,columns=['time','Price','Pos','shortPos','Capital','Fee','des']).to_pickle('./result/val_%s.pkl' % self.name)

    def tradeResult(self,priceFrm):
        if len(self.neuronDict) <= 1:
            return self.neuronDict[self.neuronList[0]].trade(priceFrm)
        else:
            newstr = self.buytype
            for string in self.neuronList:
                newstr = newstr.replace(string,eval('self.neuronDict[\'%s\'].trade(priceFrm)' % string))
            
            if eval(newstr.replace('shortbuy','False').replace('shortsell','False').replace('buy','True').replace('sell','False').replace('none','False')):
                return 'buy'
            elif eval(newstr.replace('shortbuy','False').replace('shortsell','False').replace('buy','False').replace('sell','True').replace('none','False')):
                return 'sell'
            elif eval(newstr.replace('shortbuy','True').replace('shortsell','False').replace('buy','False').replace('sell','False').replace('none','False')):
                return 'shortbuy'
            elif eval(newstr.replace('shortbuy','False').replace('shortsell','True').replace('buy','False').replace('sell','False').replace('none','False')):
                return 'shortsell'
            else:
                return ''

    def buy(self,priceFrm):
        if len(self.neuronDict) <= 1:
            return self.neuronDict[self.neuronList[0]].buy(priceFrm)
        else:
            newstr = self.buytype
            for string in self.neuronList:
                newstr = newstr.replace(string,'self.neuronDict[\'%s\'].buy(priceFrm)' % string)
            return eval(newstr)

    def sell(self,priceFrm):
        if len(self.neuronDict) <= 1:
            return self.neuronDict[self.neuronList[0]].sell(priceFrm)
        else:
            newstr = self.selltype
            for string in self.neuronList:
                newstr = newstr.replace(string,'self.neuronDict[\'%s\'].sell(priceFrm)' % string)
            return eval(newstr)

    def __del__(self):
        class_name = self.__class__.__name__
        print(self.name, '销毁')
