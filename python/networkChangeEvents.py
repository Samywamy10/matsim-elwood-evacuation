from xmlelement import XmlElement
from dateutil import parser
from datetime import timedelta

class NetworkChangeEvents(XmlElement):
    def __init__(self):
        XmlElement.__init__(self, 'networkChangeEvents')
        self.xmlElement.set('xmlns','http://www.matsim.org/files/dtd')
        self.xmlElement.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
        self.xmlElement.set('xsi:schemaLocation','http://www.matsim.org/files/dtd http://www.matsim.org/files/dtd/networkChangeEvents.xsd')
    
    def addNetworkChangeEvent(self, networkChangeEvent):
        self.addSubElement(networkChangeEvent.xmlElement)

    @staticmethod
    def addToTime(currentTime, addSeconds):
        currentTime = parser.parse(currentTime) + timedelta(seconds=addSeconds)
        return currentTime.strftime("%H:%M:%S")
        
    def generateNetworkChangeEvents(self, inputfile):
        current = 0
        startTime = '01:00:01'
        with open(inputfile, 'r') as floodingFile:
            for line in floodingFile:
                if(line[0] == "#"):
                    if current != 0:
                        freespeed = Freespeed()
                        networkChangeEvent.addFreespeed(freespeed)
                    networkChangeEvent = NetworkChangeEvent(startTime)
                    startTime = self.addToTime(startTime,1)
                    self.addNetworkChangeEvent(networkChangeEvent)
                    current += 1
                else:
                    id = line.strip()
                    link = Link(id)
                    networkChangeEvent.addLink(link)
            freespeed = Freespeed()
            networkChangeEvent.addFreespeed(freespeed)
            
class NetworkChangeEvent(XmlElement):
    def __init__(self, startTime = '01:00:01'):
        XmlElement.__init__(self, 'networkChangeEvent')
        self.xmlElement.set('startTime', startTime)
    
    def addFreespeed(self, freespeed):
        self.addSubElement(freespeed.xmlElement)
    
    def addLink(self, link):
        self.addSubElement(link.xmlElement)

class Freespeed(XmlElement):
    def __init__(self, speed = 0.000001):
        XmlElement.__init__(self, 'freespeed')
        self.xmlElement.set('type','absolute')
        self.xmlElement.set('value',format(speed, 'f'))

class Link(XmlElement):
    def __init__(self, id):
        XmlElement.__init__(self, 'link')
        self.xmlElement.set('refId', id)