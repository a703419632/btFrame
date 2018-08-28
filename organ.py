#coding=utf-8
#author: pans
from xml.dom.minidom import parse
import xml.dom.minidom
import pandas as pd
from pandas import DataFrame

from neuron import *
from EventNotifier import *
from EventBase import EventBase

OnHeartBeat = DataEvent('OnHeartBeat')

class Organ(EventBase):
    def __init__(self,data,neuronDict):
        super(Organ, self).__init__()

        self.name = data.getElementsByTagName("name")[0].childNodes[0].data
        self.neuronList = data.getElementsByTagName("neuron")[0].childNodes[0].data.split(',')
        self.buytype = data.getElementsByTagName("buytype")[0].childNodes[0].data
        self.selltype = data.getElementsByTagName("selltype")[0].childNodes[0].data
        self.feeRatio = float(data.getElementsByTagName("feeRatio")[0].childNodes[0].data)
        self.capital = float(data.getElementsByTagName("capital")[0].childNodes[0].data)
        self.pos = float(data.getElementsByTagName("pos")[0].childNodes[0].data)
        self.buyonce = float(data.getElementsByTagName("buyonce")[0].childNodes[0].data)
        self.sellonce = float(data.getElementsByTagName("sellonce")[0].childNodes[0].data)
        self.auth = data.getElementsByTagName("auth")[0].childNodes[0].data
        self.date = data.getElementsByTagName("date")[0].childNodes[0].data
        self.description = data.getElementsByTagName("description")[0].childNodes[0].data
        self.neuronDict = {}
        for neu in self.neuronList:
            if neu in neuronDict:
                self.neuronDict[neu] = neuronDict[neu]

        self.valRows = []
        print('a new organ is created,name:%s,auth:%s,date:%s,description:%s' % (self.name,self.auth,self.date,self.description))

    @data_listener(OnHeartBeat)
    def getHeartBeat(self,priceFrm):

        openTime = priceFrm.loc[len(priceFrm)-1,'OpenTime']
        curPrice = float(priceFrm.loc[len(priceFrm)-1,'Close'])

        if self.buy(priceFrm):
            newPos = (min(self.capital,self.buyonce) if self.buyonce>0 else self.capital) / (curPrice*(1+self.feeRatio))
            self.pos += newPos
            curFee = curPrice*newPos*self.feeRatio
            self.capital -= (curPrice*newPos+curFee)
            self.valRows.append([openTime,curPrice,self.pos,self.capital,curFee,'buy %s' % newPos])
        elif self.sell(priceFrm):
            sellPos = min(self.pos,self.sellonce) if self.sellonce>0 else self.pos
            curFee = curPrice*curPrice*sellPos
            self.capital += (curPrice*sellPos-curFee)
            self.pos -= sellPos
            self.valRows.append([openTime,curPrice,self.pos,self.capital,curFee,'sell %s' % sellPos])

        DataFrame(self.valRows,columns=['time','Price','Pos','Capital','Fee','des']).to_pickle('./result/val_%s.pkl' % self.name)

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


        
