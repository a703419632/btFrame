#coding=utf-8
from xml.dom.minidom import parse
import xml.dom.minidom

from EventNotifier import *
from EventBase import EventBase
from organ import *
from neuron import *

#base config and inited data

class Blood(object):
    def __init__(self):
        self.PATH_ORGANCONFIG = "./organConfig.xml"
        self.PATH_BASENEURON = "./baseneuron/baseneuron.xml"
        print("blood init")

    def getXMLDatabyPath(self,path):
        print("start get xmlData from",path)
        DOMTree = xml.dom.minidom.parse(path)
        collection = DOMTree.documentElement
        return collection

    def getOrgan(self):
        orgenXML = self.getXMLDatabyPath(self.PATH_ORGANCONFIG).getElementsByTagName("organ")
        neuronDict = self.getNeuron()

        organList = []
        for organData in orgenXML:
            organ = Organ(organData,neuronDict)
            organList.append(organ)

        return organList

    def getNeuron(self):
        neuronXML = self.getXMLDatabyPath(self.PATH_BASENEURON).getElementsByTagName("neuron")

        neuronDict = {}
        for neuronData in neuronXML:
            neuron = Neuron(neuronData)
            neuronDict[neuron.name] = neuron

        return neuronDict
