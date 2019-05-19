from xmlelement import XmlElement

class VehicleDefinitions(XmlElement):
    vehicleTypesCount = 0
    vehiclesCount = 0
    vehicleIds = []

    def __init__(self):
        self.vehicleTypesCount = 0
        self.vehiclesCount = 0
        self.vehicleIds = []
        XmlElement.__init__(self, 'vehicleDefinitions')
        self.xmlElement.set('xmlns','http://www.matsim.org/files/dtd')
        self.xmlElement.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
        self.xmlElement.set('xsi:schemaLocation','http://www.matsim.org/files/dtd http://www.matsim.org/files/dtd/vehicleDefinitions_v1.0.xsd')

    def addVehicleType(self, vehicleType):
        vehicleType.setId(self.vehicleTypesCount)
        self.vehicleTypesCount += 1
        self.addSubElement(vehicleType.xmlElement)
    
    def generateVehicles(self, vehicleTypeNum, numVehicles):
        for num in range(numVehicles):
            newVehicle = Vehicle(self.vehiclesCount, vehicleTypeNum)
            self.vehicleIds.append(newVehicle.id)
            self.vehiclesCount += 1
            self.addSubElement(newVehicle.xmlElement)

class VehicleType(XmlElement):
    def __init__(self, description, seatedCapacity, standingCapacity, length):
        XmlElement.__init__(self, 'vehicleType')
        descriptionElement = XmlElement('description')
        descriptionElement.text = description
        self.addSubElement(descriptionElement.xmlElement)
        capacityElement = XmlElement('capacity')
        seatsElement = XmlElement('seats')
        seatsElement.xmlElement.set('persons', str(seatedCapacity))
        capacityElement.addSubElement(seatsElement.xmlElement)
        standingRoomElement = XmlElement('standingRoom')
        standingRoomElement.xmlElement.set('persons', str(standingCapacity))
        capacityElement.addSubElement(standingRoomElement.xmlElement)
        self.addSubElement(capacityElement.xmlElement)
        lengthElement = XmlElement('length')
        lengthElement.xmlElement.set('meter', str(length))
        self.addSubElement(lengthElement.xmlElement)
    
    def setId(self, id):
        self.xmlElement.set('id', str(id))

class Vehicle(XmlElement):
    id = ''
    
    def __init__(self, inputId, typeId):
        self.id = ''
        XmlElement.__init__(self, 'vehicle')
        self.id = 'bus_' + str(inputId)
        self.xmlElement.set('id', self.id)
        self.xmlElement.set('type', str(typeId))
