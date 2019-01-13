######################################################
#       MIEMBROS QUE HAN REALIZADO LA PRÁCTICA       #
#     Paula Carballo Pérez y Ester Cortés García     #
######################################################

#ESTE ES EL CÓDIGO DISEÑADO PARA HACER EL GRAFO RDF DEL XML COMPLETO CON TODAS LAS ESTACIONES
#POR FALTA DE RECURSOS, COMO BIEN NOS INDICA EL VALIDADOR RDF PROBADO, "The resources necessary to create this graph
# exceed size, cpu or memory restraints imposed for graphics generation on this server.", NO HA SIDO POSIBLE
#COMPROBAF SI EL FUNCIONAMIENTO DE ESTE CÓDIGO ES CORRECTO AL 100%

import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef, BNode, Literal

facilities_xml = ET.parse("TFLfacilities.xml")

g = Graph()

namespace = Namespace("http://tfl.gov.uk/tfl/")

#URIS CREADAS
station = URIRef("station")
line = URIRef("linea")
transport = URIRef("transporte")
contactDetails = URIRef('contactDetails')
zone = URIRef('zone')
facilities = URIRef('facilities')
entrances = URIRef('entrances')
bookingHallToPlatform = URIRef('bookingHallToPlatform')
platformToTrain = URIRef('platformToTrain')
path = URIRef('path')
placemark = URIRef('Placemark')
point = URIRef('point')
publicToilet = URIRef('PublicToilet')
lines = URIRef('Lines')
accessibility = URIRef('accessibility')
lifts = URIRef('lifts')
toilets = URIRef('toilets')
specificEntrance = URIRef('specificEntrance')
accessibleInterchanges = URIRef('accessibleInterchanges')
naptans = URIRef('naptans')
naptan = URIRef('naptan')
general_station = URIRef('general_station')

#PREDICADOS CREADOS
belongsTo = namespace.belongsTo
hasStations = namespace.hasStations
hasLines = namespace.hasLines
canBe = namespace.canBe
belongsToZone = namespace.belongsToZone
nameZone = namespace.nameZone
hasPublicToilet = namespace.hasPublicToilet
hasContactDetails = namespace.hasContactDetails
hasName = namespace.hasName
hasAddress = namespace.hasAddress
hasPhone = namespace.hasPhone
hasFacilities = namespace.hasFacilities
hasFacility = namespace.hasFacility
hasTicketHalls = namespace.hasTicketHalls
hasLifts = namespace.hasLifts
hasEscalators = namespace.hasEscalators
hasGates = namespace.hasGates
hasToilets = namespace.hasToilets
hasPhotoBooths = namespace.hasPhotoBooths
hasCashMachines = namespace.hasCashMachines
hasPayphones = namespace.hasPayphones
hasCarkPark = namespace.hasCarkPark
hasVendingMachines = namespace.hasVendingMachines
hasHelpPoints = namespace.hasHelpPoints
hasBridge = namespace.hasBridge
hasWaitingRoom = namespace.hasWaitingRoom
hasOtherFacilities = namespace.hasOtherFacilities
hasEntrances = namespace.hasEntrances
entranceElement = namespace.entranceElement
infoEntranceToBookingHall = namespace.infoEntranceToBookingHall
infoBookingHallToPlatform = namespace.infoBookingHallToPlatform
hasPointName = namespace.hasPointName
hasPathDescription = namespace.hasPathDescription
infoPlatformToTrain = namespace.infoPlatformToTrain
hasPlatformElem = namespace.hasPlatformElem
hasTrainName = namespace.hasTrainName
numSteps = namespace.numSteps
hasPath = namespace.hasPath
hasHeading = namespace.hasHeading
hasDescription = namespace.hasDescription
hasPoint = namespace.hasPoint
hasCoordinates = namespace.hasCoordinates
hasPlacemark = namespace.hasPlacemark
hasLocation = namespace.hasLocation
isPaymentRequired = namespace.isPaymentRequired
hasLineName = namespace.hasLineName
hasPlatform = namespace.hasPlatform
directionTo = namespace.directionTo
directionTowards = namespace.directionTowards
stepMinis = namespace.stepMinis
stepMaxis = namespace.stepMaxis
gapMinis = namespace.gapMinis
gapMaxis = namespace.gapMaxis
hasAccessbyramp = namespace.hasAccessbyramp
levelAccess = namespace.levelAccess
lineInformation = namespace.lineInformation
infoAccessibility = namespace.infoAccessibility
hasAdditionalInformation = namespace.hasAdditionalInformation
hasBlueBadgeCarParkSpaces = namespace.hasBlueBadgeCarParkSpaces
hasTaxiRanksOutsideStation = namespace.hasTaxiRanksOutsideStation
accessibilityType = namespace.accessibilityType
hasSpecificEntrance = namespace.hasSpecificEntrance
hasAccessViaLift = namespace.hasAccessViaLift
LimitedCapacityLift = namespace.LimitedCapacityLift
hasAccessibleToilet = namespace.hasAccessibleToilet
accessibleToiletNote = namespace.AccessibleToiletNote
specificEntranceRequired = namespace.specificEntranceRequired
specificEntranceInstructions = namespace.specificEntranceInstructions
hasAccessibleInterchanges = namespace.hasAccessibleInterchanges
hasAirportInterchange = namespace.hasAirportInterchange
hasPierInterchange = namespace.hasPierInterchange
hasMainBusInterchange = namespace.hasMainBusInterchange
hasEmiratesAirLineInterchange = namespace.hasEmiratesAirLineInterchange
hasTramlinkInterchange = namespace.hasTramlinkInterchange
hasNationalRailInterchange = namespace.hasNationalRailInterchange
hasLine = namespace.hasLine
hasNaptans = namespace.hasNaptans
naptanDescription = namespace.naptanDescription
naptanID = namespace.naptanID
naptanElement = namespace.naptanElement
hasStation = namespace.hasStation

#CREO EL DIAGRAMA BÁSICO, SIN PONER DETALLES EN LA ESTACIÓN
g.add((line,hasStations,general_station))
g.add((line,belongsTo,transport))
g.add((transport,hasStations,general_station))
g.add((general_station,belongsTo,line))
g.add((transport,hasLines,line))
g.add((general_station,belongsTo,transport))

g.add((transport,canBe,Literal("Tube")))
g.add((transport,canBe,Literal("Underground")))
g.add((transport,canBe,Literal("DLR")))

#OBTENGO EL NOMBRE DE LA ESTACIÓN SOBRE LA QUE SE VA A REALIZAR EL EJEMPLO
num_todas = 0
for my_station in facilities_xml.findall("stations/station"):
    g.add((general_station,hasStation,station))

    #NAME
    g.add((station, hasName, Literal(my_station.find('name').text)))

    #CONTACT DETAILS
    if my_station.find('contactDetails') != None:
        g.add((station, hasContactDetails, contactDetails))
        g.add((contactDetails,hasAddress,Literal(my_station.find('contactDetails/address').text)))
        g.add((contactDetails,hasPhone,Literal(my_station.find('contactDetails/phone').text)))
    else:
        g.add((station, hasContactDetails, BNode()))

    #ZONES
    if my_station.find('zones') != None:
        g.add((station, belongsToZone, zone))
        for zones in my_station.find('zones'):
            zone_value = zones.text
            g.add((zone,nameZone,Literal(zone_value)))
    else:
        g.add((station, belongsToZone, BNode()))

    #FACILITIES
    if my_station.find('facilities') != None:
        g.add((station, hasFacilities, facilities))
        g.add((facilities,hasTicketHalls, Literal(my_station.find('facilities/facility/[@name="Ticket Halls"]').text)))
        g.add((facilities,hasLifts, Literal(my_station.find('facilities/facility/[@name="Lifts"]').text)))
        g.add((facilities, hasOtherFacilities, Literal(my_station.find('facilities/facility/[@name="Escalators"]').text)))
        g.add((facilities,hasEscalators, Literal(my_station.find('facilities/facility/[@name="Gates"]').text)))
        g.add((facilities,hasGates, Literal(my_station.find('facilities/facility/[@name="Toilets"]').text)))
        g.add((facilities,hasToilets, Literal(my_station.find('facilities/facility/[@name="Photo Booths"]').text)))
        g.add((facilities,hasPhotoBooths, Literal(my_station.find('facilities/facility/[@name="Cash Machines"]').text)))
        g.add((facilities,hasCashMachines, Literal(my_station.find('facilities/facility/[@name="Payphones"]').text)))
        g.add((facilities,hasPayphones, Literal(my_station.find('facilities/facility/[@name="Car park"]').text)))
        g.add((facilities,hasCarkPark, Literal(my_station.find('facilities/facility/[@name="Vending Machines"]').text)))
        g.add((facilities,hasVendingMachines, Literal(my_station.find('facilities/facility/[@name="Help Points"]').text)))
        g.add((facilities,hasHelpPoints, Literal(my_station.find('facilities/facility/[@name="Bridge"]').text)))
        g.add((facilities,hasBridge, Literal(my_station.find('facilities/facility/[@name="Waiting Room"]').text)))
        g.add((facilities,hasWaitingRoom, Literal(my_station.find('facilities/facility/[@name="Other Facilities"]').text)))
    else:
        g.add((station, hasFacility, BNode()))

    #ENTRANCES
    if my_station.find('entrances')!= None:
        g.add((station,hasEntrances,entrances))
        num = 0
        for entranceElem in my_station.find('entrances'):
            num += 1
            name = 'entrance' + str(num)
            entrance = URIRef(name)
            g.add((entrances,entranceElement,entrance))
            g.add((entrance,hasName,Literal(entranceElem.find('name').text)))
            g.add((entrance,infoEntranceToBookingHall,Literal(entranceElem.find('entranceToBookingHall').text)))
            g.add((entrance,infoBookingHallToPlatform,bookingHallToPlatform))
            if entranceElem.find('bookingHallToPlatform/pointName') != None:
                g.add((bookingHallToPlatform, hasPointName, Literal(entranceElem.find('bookingHallToPlatform/pointName').text)))
            else:
                g.add((bookingHallToPlatform, hasPointName, BNode()))
            if entranceElem.find('bookingHallToPlatform/pathDescription') != None:
                g.add((bookingHallToPlatform, hasPathDescription,Literal(entranceElem.find('bookingHallToPlatform/pathDescription').text)))
            else:
                g.add((bookingHallToPlatform, hasPointName, BNode()))
            if entranceElem.find('bookingHallToPlatform/path') != None:
                g.add((bookingHallToPlatform, hasPath,path ))
                g.add((path,hasHeading,Literal(entranceElem.find('bookingHallToPlatform/path/heading').text)))
                g.add((path,hasPathDescription,Literal(entranceElem.find('bookingHallToPlatform/path/pathDescription').text)))
            else:
                g.add((bookingHallToPlatform, hasPath, BNode()))
            g.add((entrance,infoPlatformToTrain,platformToTrain))
            num2=0
            for platformElem in entranceElem.findall('platformToTrain'):
                num2 += 1
                name = 'platform' + str(num2)
                platformElemt = URIRef(name)
                g.add((platformToTrain,hasPlatformElem,platformElemt))
                g.add((platformElemt,hasTrainName,Literal(platformElem.find('trainName').text)))
                g.add((platformElemt,numSteps,Literal(platformElem.find('platformToTrainSteps').text)))
    else:
        g.add((station,hasEntrances,BNode()))

    #PLACE MARK
    if my_station.find('Placemark') != None:
        g.add((station, hasPlacemark, placemark))
        g.add((placemark,hasName,Literal(my_station.find('Placemark/name').text)))
        g.add((placemark,hasDescription,Literal(my_station.find('Placemark/description').text)))
        g.add((placemark,hasPoint,point))
        g.add((point,hasCoordinates,Literal(my_station.find('Placemark/Point/coordinates').text)))
    else:
        g.add((station, hasPlacemark, BNode()))

    #LINES
    if my_station.find('Lines') != None:
        g.add((station, hasLines, lines))
        num=0
        for lineElem in my_station.find('Lines'):
            num +=1
            name='line'
            lineElement = URIRef(name+str(num))
            g.add((lines,lineInformation,lineElement))
            g.add((lineElement, hasLineName, Literal(lineElem.find('LineName').text)))
            g.add((lineElement, hasPlatform, Literal(lineElem.find('Platform').text)))
            g.add((lineElement, directionTo, Literal(lineElem.find('Direction').text)))
            g.add((lineElement, directionTowards, Literal(lineElem.find('DirectionTowards').text)))
            g.add((lineElement, stepMinis, Literal(lineElem.find('StepMin').text)))
            g.add((lineElement, stepMaxis, Literal(lineElem.find('StepMax').text)))
            g.add((lineElement, gapMinis, Literal(lineElem.find('GapMin').text)))
            g.add((lineElement, gapMaxis, Literal(lineElem.find('GapMax').text)))
            g.add((lineElement, hasAccessbyramp, Literal(lineElem.find('LevelAccessByManualRamp').text)))
            g.add((lineElement, levelAccess, Literal(lineElem.find('LocationOfLevelAccess').text)))
    else:
        g.add((station,hasLine,BNode()))

    #PUBLIC TOILET
    if my_station.find('PublicToilet') != None and my_station.find('PublicToilet').attrib == {'Exists':'Yes'}:
        g.add((station, hasPublicToilet, publicToilet))
        g.add((publicToilet,hasLocation,Literal(my_station.find('PublicToilet/Location').text)))
        g.add((publicToilet,isPaymentRequired,Literal(my_station.find('PublicToilet/PaymentRequired').text)))
    else:
        g.add((station, hasPublicToilet, BNode()))

    #ACCESSIBILITY

    if my_station.find('Accessibility') != None:
        g.add((station,infoAccessibility,accessibility))
        g.add((accessibility,hasAdditionalInformation,Literal(my_station.find('Accessibility/AdditionalAccessibilityInformation').text)))
        g.add((accessibility,hasBlueBadgeCarParkSpaces,Literal(my_station.find('Accessibility/AdditionalAccessibilityInformation').text)))
        g.add((accessibility,hasTaxiRanksOutsideStation,Literal(my_station.find('Accessibility/TaxiRanksOutsideStation').text)))
        g.add((accessibility,hasLifts,lifts))
        g.add((lifts,hasAccessViaLift,Literal(my_station.find('Accessibility/Lifts/AccessViaLift').text)))
        g.add((lifts,LimitedCapacityLift,Literal(my_station.find('Accessibility/Lifts/LimitedCapacityLift').text)))
        g.add((accessibility,hasToilets,toilets))
        g.add((toilets,hasAccessibleToilet,Literal(my_station.find('Accessibility/Toilets/AccessibleToilet').text)))
        g.add((toilets,accessibleToiletNote,Literal(my_station.find('Accessibility/Toilets/AccessibleToiletNote').text)))
        g.add((accessibility,hasSpecificEntrance,specificEntrance))
        g.add((specificEntrance,specificEntranceRequired,Literal(my_station.find('Accessibility/SpecificEntrance/SpecificEntranceRequired').text)))
        g.add((specificEntrance,specificEntranceInstructions,Literal(my_station.find('Accessibility/SpecificEntrance/SpecificEntranceInstructions').text)))
        if my_station.find('Accessibility/AccessibilityType') != None:
            g.add((accessibility,accessibilityType,Literal(my_station.find('Accessibility/AccessibilityType').text)))
        else:
            g.add((accessibility,accessibility,BNode()))
    else:
        g.add((my_station,infoAccessibility,BNode()))

    #ACCESSIBLE INTERCHANGES
    if my_station.find('AccessibleInterchanges') != None:
        g.add((station, hasAccessibleInterchanges,accessibleInterchanges))
        g.add((accessibleInterchanges,hasAirportInterchange,Literal(my_station.find('AccessibleInterchanges/AirportInterchange').text)))
        g.add((accessibleInterchanges,hasPierInterchange,Literal(my_station.find('AccessibleInterchanges/PierInterchange').text)))
        g.add((accessibleInterchanges,hasMainBusInterchange,Literal(my_station.find('AccessibleInterchanges/MainBusInterchange').text)))
        g.add((accessibleInterchanges,hasEmiratesAirLineInterchange,Literal(my_station.find('AccessibleInterchanges/EmiratesAirLineInterchange').text)))
        g.add((accessibleInterchanges,hasTramlinkInterchange,Literal(my_station.find('AccessibleInterchanges/TramlinkInterchange').text)))
        g.add((accessibleInterchanges,hasNationalRailInterchange,Literal(my_station.find('AccessibleInterchanges/NationalRailInterchange').text)))
    else:
        g.add((station,hasAccessibleInterchanges,BNode()))

    #NAPTANS
    if my_station.find('Naptans') != None:
        g.add((station, hasNaptans,naptans))
        num_naptan = 0
        for naptane in my_station.find('Naptans'):
            num_naptan += 1
            name = 'naptan'+str(num_naptan)
            naptan = URIRef(name)
            g.add((naptans,naptanElement,naptan))
            g.add((naptan,naptanDescription,Literal(naptane.find('Description').text)))
            g.add((naptan,naptanID,Literal(naptane.find('NaptanID').text)))
    else:
        g.add((station,hasNaptans,BNode()))

g.serialize(destination="RDF_XML.xml",format="xml")
