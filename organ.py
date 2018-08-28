#coding=utf-8
#author: pans
from xml.dom.minidom import parse
import xml.dom.minidom

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
        self.fee = data.getElementsByTagName("fee")[0].childNodes[0].data
        self.capital = data.getElementsByTagName("capital")[0].childNodes[0].data
        self.pos = data.getElementsByTagName("pos")[0].childNodes[0].data
        self.buyonce = data.getElementsByTagName("buyonce")[0].childNodes[0].data
        self.sellonce = data.getElementsByTagName("sellonce")[0].childNodes[0].data
        self.auth = data.getElementsByTagName("auth")[0].childNodes[0].data
        self.date = data.getElementsByTagName("date")[0].childNodes[0].data
        self.description = data.getElementsByTagName("description")[0].childNodes[0].data
        self.neuronDict = {}
        for neu in self.neuronList:
            if neu in neuronDict:
                self.neuronDict[neu] = neuronDict[neu]
        print('a new organ is created,name:%s,auth:%s,date:%s,description:%s' % (self.name,self.auth,self.date,self.description))

    @data_listener(OnHeartBeat)
    def getHeartBeat(self,priceFrm):
        if self.buy(priceFrm):
            print(self.name,'buy buy buy')
        elif self.sell(priceFrm):
            print(self.name,'sell sell sell')

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


        
