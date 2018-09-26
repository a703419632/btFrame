#coding=utf-8
#author: pans
from xml.dom.minidom import parse
import xml.dom.minidom

from organ import *
from neuron import *

#base config and inited data

class Blood(object):
    def __init__(self):
        self.PATH_ORGANCONFIG = "./organConfig.xml"
        self.PATH_BASENEURON = "./baseneuron/baseneuron.xml"
        self.organDict = {}
        self.eventManager = EventManager()
        print("blood init")

    def getXMLDatabyPath(self,path):
        DOMTree = xml.dom.minidom.parse(path)
        collection = DOMTree.documentElement
        return collection

    def getOrgan(self):
        orgenXML = self.getXMLDatabyPath(self.PATH_ORGANCONFIG).getElementsByTagName("organ")
        neuronXMLDict = self.getNeuronXMLDict()

        organList = []
        for organData in orgenXML:
            if organData.getElementsByTagName("name")[0].childNodes[0].data not in self.organDict:
                organ = Organ(organData,neuronXMLDict)

                self.eventManager.AddEventListener(('OnHeartBeat_%s_%s' % (organ.cointype,organ.timetype)), organ.getHeartBeat)

                self.organDict[organData.getElementsByTagName("name")[0].childNodes[0].data] = organ
            organList.append(organData.getElementsByTagName("name")[0].childNodes[0].data)

        for key in list(self.organDict):
            if key not in organList:
                print('del organ:',key)
                delorgan = self.organDict.pop(key)
                self.eventManager.RemoveEventListener('OnHeartBeat_%s_%s' % (delorgan.cointype,delorgan.timetype), delorgan.getHeartBeat)
                del(delorgan)


        return self.organDict

    def getTimeArr(self):
        timearr = []
        for organ in self.organDict:
            if self.organDict[organ].timetype not in timearr:
                timearr.append(self.organDict[organ].timetype)
        return timearr

    def getCoinArr(self):
        coinarr = []
        for organ in self.organDict:
            if self.organDict[organ].cointype not in coinarr:
                coinarr.append(self.organDict[organ].cointype)
        return coinarr

    def getNeuron(self):
        neuronXML = self.getXMLDatabyPath(self.PATH_BASENEURON).getElementsByTagName("neuron")

        neuronDict = {}
        for neuronData in neuronXML:
            neuron = Neuron(neuronData)
            neuronDict[neuron.name] = neuron

        return neuronDict


    def getNeuronXMLDict(self):
        neuronXML = self.getXMLDatabyPath(self.PATH_BASENEURON).getElementsByTagName("neuron")

        neuronXMLDict = {}
        for neuronData in neuronXML:
            neuronXMLDict[neuronData.getElementsByTagName("name")[0].childNodes[0].data] = neuronData

        return neuronXMLDict
