######################################################
#       MIEMBROS QUE HAN REALIZADO LA PRÁCTICA       #
#     Paula Carballo Pérez y Ester Cortés García     #
######################################################

#Imports

import requests
import xml.etree.ElementTree as ET

##########################EJERCICIO 1###################################

#Descarga de datos Station Facilities

app_id= ""
app_key = ""
parameters={"app_id":app_id,"app_key":app_key}
url_station = "https://api.tfl.gov.uk/tfl/syndication/feeds/stations-facilities.xml"
response_station = requests.get(url_station,params=parameters)
with open("StationFacilities.xml","wb") as file:
    file.write(response_station.content)
file.close()

#Descarga de datos Step Free Tube Guide Data

url_step = "https://api.tfl.gov.uk/tfl/syndication/feeds/step-free-tube-guide.xml"
response_step = requests.get(url_step)
with open("StepFreeTubeGuideData.xml","wb") as file:
    file.write(response_step.content)
file.close()

##########################EJERCICIO 2##################################

tree = ET.parse("StationFacilities.xml")
for child in tree.findall("stations/station"): #obtengo cada estación con su información
    child.remove(child.find("openingHours"))
tree.write("StationFacilitiesNOH.xml")

############################EJERCICIO 3##############################

ET.register_namespace("","ELRAD")
tree = ET.parse("StepFreeTubeGuideData.xml")
for child in tree.findall("{ELRAD}Station/{ELRAD}Accessibility"):
    if child.find("{ELRAD}AccessibilityType").text == "None":
        child.remove(child.find("{ELRAD}AccessibilityType"))
tree.write("StepFreeTubeNNone.xml")

############################EJERCICIO 5##############################

tree_station = ET.parse("StationFacilitiesNOH.xml")
station_root = tree_station.getroot()
tree_step = ET.parse("StepFreeTubeNNone.xml")
step_root = tree_step.getroot()

for child_station in tree_station.findall("stations/station"):
    found = False
    for child_step in tree_step.findall("{ELRAD}Station"):
        if child_station.find("name").text == child_step.find("{ELRAD}StationName").text:
            found = True
            #Se añade la información de las líneas contenida en Step Free Tube Guide porque es más completa
            lines = child_step.find("{ELRAD}Lines")
            child_station.remove(child_station.find("servingLines"))
            child_station.append(lines)
            #Se añade la información de baños públicos contenida en Step Free Tube Guide y que no figura en Station Facilities
            public_toilets = child_step.find("{ELRAD}PublicToilet")
            child_station.append(public_toilets)
            #Se añade la información de accesibilidad contenida en Step Free Tube Guide y que no figura en Station Facilities
            accessibility = child_step.find("{ELRAD}Accessibility")
            child_station.append(accessibility)
            #Se añade la información de intercambios accesibles contenida en Step Free Tube Guide y que no figura en Station Facilities
            accessible_interchanges = child_step.find("{ELRAD}AccessibleInterchanges")
            child_station.append(accessible_interchanges)
            #Se añade la información de naptans contenida en Step Free Tube Guide y que no figura en Station Facilities
            naptans = child_step.find("{ELRAD}Naptans")
            child_station.append(naptans)
            #Se borra la estación coincidente para ir dejando unicamente las que no aparecen en Station Facilities.
            step_root.remove(child_step)

tree_step.write("borrador_step.xml") #Se guarda un borrador con las estaciones que únicamente están en el xml Step Free

#Hay que pasar las estaciones que sólo están en Step Free a Station Facilities
list = tree_station.find('stations')
new_tree_step = ET.parse("borrador_step.xml")
for child in new_tree_step.findall("{ELRAD}Station"):
    list.append(child)
tree_station.write("TFLfacilities.xml")



#Se cambian los nombres de las etiquetas para que coincidan
station = ET.parse("TFLfacilities.xml")
root = station.getroot()
for element in root.iter('{ELRAD}Station'):
    element.tag = 'station'
for element in root.iter('{ELRAD}StationName'):
    element.tag = 'name'
for element in root.iter('{ELRAD}servingLines'):
    element.tag = 'Lines'
for element in root.iter('{ELRAD}servingLine'):
    element.tag = 'Line'
station.write("TFLfacilities.xml")

file = open('TFLfacilities.xml','r')
text = file.read()
file.close()
file = open('TFLfacilities.xml','w')
file.write(text.replace('xmlns="ELRAD"','xmlns:tfl="http://tfl.gov.uk/tfl#"'))
file.close()



