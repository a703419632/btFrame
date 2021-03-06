#coding=utf-8
#author: pans
from xml.dom.minidom import parse
import xml.dom.minidom
import glob
import os
import sys
import time

class Neuron(object):
    def __init__(self,data):
        self.name = data.getElementsByTagName("name")[0].childNodes[0].data
        self.source = data.getElementsByTagName("source")[0].childNodes[0].data
        self.trademodule = data.getElementsByTagName("trademodule")[0].childNodes[0].data       
        self.auth = data.getElementsByTagName("auth")[0].childNodes[0].data
        self.date = data.getElementsByTagName("date")[0].childNodes[0].data
        self.description = data.getElementsByTagName("description")[0].childNodes[0].data
        self.module = __import__(self.source)
        print('a new neuron is created,name:%s,auth:%s,date:%s,description:%s,time:%s' % (self.name,self.auth,self.date,self.description,time.time()))


    def trade(self,priceFrm):
        return getattr(self.module,self.trademodule)(priceFrm)
