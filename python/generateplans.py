import sys

import xml.etree.ElementTree as ET
import lxml.etree
import subprocess
import os
import math
from network import Network
from shape import Polygon, Coordinate
from population import Population
from networkChangeEvents import NetworkChangeEvents
from vehicles import VehicleDefinitions, VehicleType
from transitschedule import TransitSchedule, StopFacility, TransitLine, TransitRoute, Stop, Departure
from multiprocessing.dummy import Pool as ThreadPool 
from glob import glob
import re

def modifyConfig(reRoute,changeTripMode):
    config = lxml.etree.parse('../config.xml')
    #ReRoute
    totalValue = 1.00
    if reRoute:
        reRoute = config.xpath("module[@name='strategy']/parameterset[param/@value='ReRoute']/param[@name='weight']")[0]
        weight = 0.05
        reRoute.attrib["value"] = str(weight)
        totalValue -= weight
    if changeTripMode:
        changeTripMode = config.xpath("module[@name='strategy']/parameterset[param/@value='ChangeTripMode']/param[@name='weight']")[0]
        weight = 0.05
        changeTripMode.attrib["value"] = str(weight)
        totalValue -= weight
    bestScore = config.xpath("module[@name='strategy']/parameterset[param/@value='BestScore']/param[@name='weight']")[0]
    bestScore.attrib["value"] = str(totalValue)
    with open('../config.xml', 'wb') as f:
        f.write(lxml.etree.tostring(config))

def generatePlans(numberOfBuses,busSpacing,reRoute,changeLegMode,floodSpacing):
    populationSize = 500
    #safe zone above creek
    aboveCreek = Polygon(Coordinate(1.614234761040829E7,-4560734.749976564), Coordinate(1.6143367207888365E7,-4560898.8048608275), Coordinate(1.6142285026590563E7, -4561169.767607265), Coordinate(1.614330436803581E7,-4561331.897382162))

    #safe zone below creek
    belowCreek = Polygon(Coordinate(1.6143313774532782E7,-4566525.3373900475), Coordinate(1.6144027621899443E7,-4566781.843705078), Coordinate(1.6143215668665543E7,-4567264.97602887),Coordinate(1.6143947816956492E7,-4567382.626620158))

    startPolygon = Polygon(Coordinate(1.614028846699539E7,-4564142.798143045), Coordinate(1.6141367319840414E7,-4564304.043329135), Coordinate(1.6140162052581646E7,-4564994.586420819),Coordinate(1.6141633184180276E7,-4565200.056965046))

    network = Network(ET.parse('../net.xml'))
    population = Population()
    population.generatePopulation(populationSize, startPolygon, [belowCreek])
    header2 = '<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v6.dtd">'
    #population.writeTreeToFile("../generatedplans.xml", header2)

    #network change events
    networkChangeEvents = NetworkChangeEvents()
    networkChangeEvents.generateNetworkChangeEvents("../flooding.txt", int(floodSpacing))
    networkChangeEvents.writeTreeToFile("../networkChangeEvents.xml")

    #vehicles
    vehicleDefinitions = VehicleDefinitions()
    bus = VehicleType("Bus",80,0,50.0)
    vehicleDefinitions.addVehicleType(bus)
    vehicleDefinitions.generateVehicles(0,int(numberOfBuses))
    vehicleIds = vehicleDefinitions.vehicleIds
    vehicleDefinitions.writeTreeToFile("../vehicles.xml")

    #transit schedule
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
    transitRoute.generateDepartures(vehicleIds, int(busSpacing))
    transitLine.addTransitRoute(transitRoute)
    transitSchedule.addTransitLine(transitLine)

    header2 = '<!DOCTYPE transitSchedule SYSTEM "http://www.matsim.org/files/dtd/transitSchedule_v1.dtd">'
    transitSchedule.writeTreeToFile("../transitSchedule.xml", header2)

    #config
    modifyConfig(reRoute, changeLegMode)

    os.chdir('../')
    subprocess.call(['java', '-cp', 'matsim-0.10.1.jar', 'org.matsim.run.Controler', './config.xml', '-Xmx16024m', '-d64'])

    #summarise trip durations and total evacuation times into one file
    tripDurations = []
    totalEvacuationTimes = []
    tripDistances = []
    modeSplit = []
    for iterationNumber in range(0,101):
        with open(f'output/ITERS/it.{iterationNumber}/{iterationNumber}.tripdurations.txt', 'r') as f:
            lineCount = 0
            totalLineCount = 0
            for line in f:
                totalLineCount += 1
        with open(f'output/ITERS/it.{iterationNumber}/{iterationNumber}.tripdurations.txt', 'r') as f:
            for line in f:
                if lineCount == totalLineCount - 1:
                    averageTripDuration = re.search(r'\d+\.\d', line).group()
                    tripDurations.append(averageTripDuration)
                lineCount += 1

        with open(f'output/ITERS/it.{iterationNumber}/{iterationNumber}.legHistogram.txt', 'r') as f:
            evacuationEndSeconds = math.inf
            firstLine = True
            for line in f:
                if firstLine:
                    firstLine = False
                    continue
                splitLine = line.split('\t')
                allZero = True
                for columnIdx in range(2,len(splitLine)):
                    column = splitLine[columnIdx].strip()
                    if int(column) != 0:
                        allZero = False
                        break
                if allZero:
                    evacuationEndSeconds = splitLine[1]
                    break
            totalEvacuationTimes.append(evacuationEndSeconds)
    with open('output/modestats.txt', 'r') as f:
        firstLine = True
        for line in f:
            if firstLine:
                firstLine = False
                continue
            splitLine = line.split('\t')
            carRatio = splitLine[1]
            modeSplit.append(carRatio)

    with open('output/traveldistancestats.txt', 'r') as f:
        firstLine = True
        for line in f:
            if firstLine:
                firstLine = False
                continue
            splitLine = line.split('\t')
            tripdistance = splitLine[1]
            tripDistances.append(tripdistance)

    with open('output/iterationSummary.txt', 'w') as f:
        f.write('ITERATION\tAVG. Trip Duration\tevacuation end seconds\tcar ratio\ttrip distances\n')
        for idx, tripDuration in enumerate(tripDurations):
            f.write(f'{idx}\t{tripDuration}\t{totalEvacuationTimes[idx]}\t{modeSplit[idx]}\t{tripDistances[idx]}\n')
    os.rename('output',f'nobus{numberOfBuses}-busspace{busSpacing}-rrw{reRoute}-clmw{changeLegMode}-flood{floodSpacing}')
    os.chdir('python')
    return (tripDurations[-1],tripDistances[-1],modeSplit[-1],totalEvacuationTimes[-1])

results = []
with open('../inputs.csv','r') as f:
    firstLine = True
    for line in f:
        if firstLine:
            header = line
            firstLine = False
            continue
        splitLine = line.split(',')
        splitLine[5], splitLine[6], splitLine[7], splitLine[8] = generatePlans(splitLine[0],splitLine[1],splitLine[2],splitLine[3],splitLine[4])
        results.append(splitLine)

with open('../results.csv','a') as f:
    #f.write(header)
    for result in results:
        f.write(','.join(result) + '\n')


