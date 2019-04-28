from xmlelement import XmlElement
from network import Shape, Coordinate
import random

class Population(XmlElement):
    def __init__(self):
        XmlElement.__init__(self,'population')
    
    def generatePopulation(self, populationSize, startPolygon, endPolygons):
        for personNumber in range(populationSize):
            person = Person(personNumber, self.xmlElement)
            plan = Plan()
            startCoordinate = startPolygon.getRandomPosition()
            #startCoordinate = Coordinate(1.6141652226832656E7,-4564170.219945342)
            startActivity = Activity('h', startCoordinate, '00:00:00')
            plan.addActivity(startActivity)
            plan.addActivity(Leg('car'))
            #endCoordinate = Shape.getClosestShapeFromCoordinate(startCoordinate, endPolygons).getRandomPosition()
            endCoordinate = Coordinate(1.6143126101003256E7, -4567282.359673435)
            endActivity = Activity('w', endCoordinate, '01:00:00')
            plan.addActivity(endActivity)
            person.addPlan(plan)
            self.addPerson(person)

    def addPerson(self, person):
        self.addSubElement(person.xmlElement)

class Person(XmlElement):
    def __init__(self, internalId, populationXml):
        XmlElement.__init__(self, 'person')
        self.__generateId()
        self.xmlElement.set('id',self.id)
        self.internalId = internalId
    
    def __generateId(self):
        self.id = str(random.randint(1000000000,9999999999))

    def addPlan(self, plan):
        self.addSubElement(plan.xmlElement)

class Plan(XmlElement):
    def __init__(self, selected = True):
        XmlElement.__init__(self, 'plan')
        if selected:
            self.xmlElement.set('selected','yes')
        else:
            self.xmlElement.set('selected','no')

    def addActivity(self, activity):
        self.addSubElement(activity.xmlElement)
    
    def addLeg(self, leg):
        self.addSubElement(leg.xmlElement)

class Activity(XmlElement):
    def __init__(self, typeName, coordinate, endTime):
        XmlElement.__init__(self, 'activity')
        self.xmlElement.set('type', typeName)
        self.xmlElement.set('x', str(coordinate.x))
        self.xmlElement.set('y', str(coordinate.y))
        self.xmlElement.set('end_time', endTime)

class Leg(XmlElement):
    def __init__(self, modeName):
        XmlElement.__init__(self, 'leg')
        self.xmlElement.set('mode',modeName)