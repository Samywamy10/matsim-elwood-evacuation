from xmlelement import XmlElement
from networkChangeEvents import NetworkChangeEvents

class TransitSchedule(XmlElement):
    stopFacilityCount = 0

    def __init__(self):
        XmlElement.__init__(self,'transitSchedule')
        transitStopsElement = XmlElement('transitStops')
        self.addSubElement(transitStopsElement.xmlElement)

    def addStopFacility(self, stopFacility):
        for item in self.xmlElement.findall("transitStops"):
            stopFacility.setId(str(self.stopFacilityCount))
            self.stopFacilityCount += 1
            item.append(stopFacility.xmlElement)
            break
    
    def addTransitLine(self, transitLine):
        self.addSubElement(transitLine.xmlElement)

class StopFacility(XmlElement):
    def __init__(self, x, y, linkRefId, name):
        XmlElement.__init__(self,'stopFacility')
        self.xmlElement.set('x',str(x))
        self.xmlElement.set('y',str(y))
        self.xmlElement.set('linkRefId',str(linkRefId))
        self.xmlElement.set('name',name)

    def setId(self, id):
        self.xmlElement.set('id', str(id))

class TransitLine(XmlElement):
    def __init__(self, id):
        XmlElement.__init__(self,'transitLine')
        self.xmlElement.set('id', str(id))
    
    def addTransitRoute(self, transitRoute):
        self.addSubElement(transitRoute.xmlElement)

class TransitRoute(XmlElement):
    departuresCount = 0
    currentTime = "00:00:00"

    def __init__(self,id, transportMode):
        XmlElement.__init__(self,'transitRoute')
        self.xmlElement.set('id',str(id))
        transportModeElement = XmlElement('transportMode')
        transportModeElement.xmlElement.text = transportMode
        self.addSubElement(transportModeElement.xmlElement)
        routeProfileElement = XmlElement('routeProfile')
        self.addSubElement(routeProfileElement.xmlElement)
        routeElement = XmlElement('route')
        self.addSubElement(routeElement.xmlElement)
        departuresElement = XmlElement('departures')
        self.addSubElement(departuresElement.xmlElement)

    def addStop(self,stop):
        for item in self.xmlElement.findall("routeProfile"):
            item.append(stop.xmlElement)
            break

    def addRouteLink(self, link):
        for item in self.xmlElement.findall("route"):
            item.append(link.xmlElement)
            break
    
    def addRouteLinksFromFile(self, inputFile):
        with open(inputFile, 'r') as linksFile:
            for linkRefId in linksFile:
                link = Link(linkRefId.strip())
                self.addRouteLink(link)

    def addDeparture(self, departure):
        for item in self.xmlElement.findall("departures"):
            departure.setId(str(self.departuresCount))
            self.departuresCount += 1
            item.append(departure.xmlElement)
            break
    
    def generateDepartures(self, vehicleIds, spacingSeconds):
        for vehicleId in vehicleIds:
            departure = Departure(self.currentTime, vehicleId)
            self.addDeparture(departure)
            self.currentTime = NetworkChangeEvents.addToTime(self.currentTime, spacingSeconds)


class Stop(XmlElement):
    def __init__(self,refId):
        XmlElement.__init__(self,'stop')
        self.xmlElement.set('refId', str(refId))
    
    def setDepartureOffset(self, departureOffset):
        self.xmlElement.set('departureOffset',departureOffset)
    
    def setArrivalOffset(self, arrivalOffset):
        self.xmlElement.set('arrivalOffset', arrivalOffset)


class Link(XmlElement):
    def __init__(self,refId):
        XmlElement.__init__(self,'link')
        self.xmlElement.set('refId', refId)

class Departure(XmlElement):
    def __init__(self,departureTime,vehicleRefId):
        XmlElement.__init__(self,'departure')
        self.xmlElement.set('departureTime', departureTime)
        self.xmlElement.set('vehicleRefId', vehicleRefId)
    
    def setId(self, id):
        self.xmlElement.set('id',id)