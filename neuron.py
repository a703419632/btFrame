#coding=utf-8
#author: pans
from xml.dom.minidom import parse
import xml.dom.minidom
import glob
import os
import sys

class Neuron(object):
    def __init__(self,data):
        self.name = data.getElementsByTagName("name")[0].childNodes[0].data
        self.source = data.getElementsByTagName("source")[0].childNodes[0].data
        self.buymodule = data.getElementsByTagName("buymodule")[0].childNodes[0].data
        self.sellmodule = data.getElementsByTagName("sellmodule")[0].childNodes[0].data       
        self.auth = data.getElementsByTagName("auth")[0].childNodes[0].data
        self.date = data.getElementsByTagName("date")[0].childNodes[0].data
        self.description = data.getElementsByTagName("description")[0].childNodes[0].data
        self.module = __import__(self.source)
        print('a new neuron is created,name:%s,auth:%s,date:%s,description:%s' % (self.name,self.auth,self.date,self.description))


    def buy(self,priceFrm):
        return getattr(self.module,self.buymodule)(priceFrm)

    def sell(self,priceFrm):
        return getattr(self.module,self.sellmodule)(priceFrm)
