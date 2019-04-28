import sys

populationSize = int(sys.argv[1])

import xml.etree.ElementTree as ET
from network import Network
from shape import Polygon, Coordinate
from population import Population
from networkChangeEvents import NetworkChangeEvents
from vehicles import VehicleDefinitions, VehicleType
from transitschedule import TransitSchedule, StopFacility, TransitLine, TransitRoute, Stop, Departure

#safe zone above creek
aboveCreek = Polygon(Coordinate(1.614234761040829E7,-4560734.749976564), Coordinate(1.6143367207888365E7,-4560898.8048608275), Coordinate(1.6142285026590563E7, -4561169.767607265), Coordinate(1.614330436803581E7,-4561331.897382162))

#safe zone below creek
belowCreek = Polygon(Coordinate(1.6143313774532782E7,-4566525.3373900475), Coordinate(1.6144027621899443E7,-4566781.843705078), Coordinate(1.6143215668665543E7,-4567264.97602887),Coordinate(1.6143947816956492E7,-4567382.626620158))

startPolygon = Polygon(Coordinate(1.614028846699539E7,-4564142.798143045), Coordinate(1.6141367319840414E7,-4564304.043329135), Coordinate(1.6140162052581646E7,-4564994.586420819),Coordinate(1.6141633184180276E7,-4565200.056965046))

network = Network(ET.parse('../net.xml'))
population = Population()
population.generatePopulation(populationSize, startPolygon, [belowCreek,aboveCreek])
header2 = '<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v6.dtd">'
population.writeTreeToFile("../generatedplans.xml", header2)

networkChangeEvents = NetworkChangeEvents()
networkChangeEvents.generateNetworkChangeEvents("../flooding.txt")
networkChangeEvents.writeTreeToFile("../networkChangeEvents.xml")

vehicleDefinitions = VehicleDefinitions()
bus = VehicleType("Bus",60,30,50.0)
vehicleDefinitions.addVehicleType(bus)
vehicleDefinitions.generateVehicles(0,200)
vehicleIds = vehicleDefinitions.vehicleIds
vehicleDefinitions.writeTreeToFile("../vehicles.xml")

transitSchedule = TransitSchedule()
stop1 = StopFacility("1.6141632226832656E7","-4564170.219945342","389629943_4","stop1")
stop2 = StopFacility("1.6143126101003256E7","-4567282.359673435","198451748_9","stop2")
transitSchedule.addStopFacility(stop1)
transitSchedule.addStopFacility(stop2)

transitLine = TransitLine("Bus trip")
transitRoute = TransitRoute("Bus route","bus")
stop1 = Stop(0)
stop1.setDepartureOffset("00:00:00")
transitRoute.addStop(stop1)
stop2 = Stop(1)
stop2.setArrivalOffset("00:00:30")
transitRoute.addStop(stop2)
transitRoute.addRouteLinksFromFile("../route1links.txt")
transitRoute.generateDepartures(vehicleIds, 1)
transitLine.addTransitRoute(transitRoute)
transitSchedule.addTransitLine(transitLine)

header2 = '<!DOCTYPE transitSchedule SYSTEM "http://www.matsim.org/files/dtd/transitSchedule_v1.dtd">'
transitSchedule.writeTreeToFile("../transitSchedule.xml", header2)