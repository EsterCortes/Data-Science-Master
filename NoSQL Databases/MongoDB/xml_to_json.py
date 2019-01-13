
import xml.etree.ElementTree as ET
import json
from collections import OrderedDict

#se crea un parseador para el documento xml debido a los caracteres inusuales
parser = ET.XMLParser(encoding='ISO-8859-1')

parser.entity["agrave"] = 'à'
parser.entity["uuml"] = 'ü'
parser.entity["Eacute"] = 'É'
parser.entity["eacute"] = 'é'
parser.entity["aacute"] = 'á'
parser.entity["iacute"] = 'í'
parser.entity["ouml"] = 'ö'
parser.entity["ccedil"] = 'ç'
parser.entity["egrave"] = 'è'
parser.entity["auml"] = 'ä'
parser.entity["uacute"] = 'ú'
parser.entity["aring"] = 'å'
parser.entity["oacute"] = 'ó'
parser.entity["szlig"] = 'ß'
parser.entity["oslash"] = 'ø'
parser.entity["yacute"] = 'ỳ'
parser.entity["iuml"] = 'ï'
parser.entity["igrave"] = 'í'
parser.entity["ocirc"] = 'ô'
parser.entity["icirc"] = 'î'
parser.entity["Uuml"] = 'Ü'
parser.entity["euml"] = 'ë'
parser.entity["acirc"] = 'â'
parser.entity["atilde"] = 'ã'
parser.entity["Uacute"] = 'Ù'
parser.entity["Aacute"] = 'À'
parser.entity["ntilde"] = 'ñ'
parser.entity["Auml"] = 'Ä'
parser.entity["Oslash"] = 'Ø'
parser.entity["Ccedil"] = 'Ç'
parser.entity["otilde"] = 'õ'
parser.entity["ecirc"] = 'ê'
parser.entity["times"] = '×'
parser.entity["Ouml"] = 'Ö'
parser.entity["reg"] = '®'
parser.entity["Aring"] = 'Å'
parser.entity["Oacute"] = 'Ò'
parser.entity["ograve"] = 'ó'
parser.entity["yuml"] = 'ÿ'
parser.entity["eth"] = 'ð'
parser.entity["aelig"] = 'æ'
parser.entity["AElig"] = 'Æ'
parser.entity["Agrave"] = 'Á'
parser.entity["Iuml"] = 'Ï'
parser.entity["micro"] = 'µ'
parser.entity["Acirc"] = 'Â'
parser.entity["Otilde"] = 'Õ'
parser.entity["Egrave"] = 'É'
parser.entity["ETH"] = 'Ð'
parser.entity["ugrave"] = 'ú'
parser.entity["ucirc"] = 'û'
parser.entity["thorn"] = 'þ'
parser.entity["THORN"] = 'Þ'
parser.entity["Iacute"] = 'Ì'
parser.entity["Icirc"] = 'Î'
parser.entity["Ntilde"] = 'Ñ'
parser.entity["Ecirc"] = 'Ê'
parser.entity["Ocirc"] = 'Ô'
parser.entity["Ograve"] = 'Ó'
parser.entity["Igrave"] = 'Í'
parser.entity["Atilde"] = 'Ã'
parser.entity["Yacute"] = 'Ỳ'
parser.entity["Ucirc"] = 'Û'
parser.entity["Euml"] = 'Ë'

#se parsea el documento xml
tree = ET.parse("dblp.xml",parser=parser)
root = tree.getroot()
#se crea el diccionario auxiliar y las listas con los valores que necesitamos
dblp = OrderedDict()
dblp["dblp"]=[]
document_types = ["article","inproceedings","incollection"]
attributes = ["title","author","year"]
#se recorre el xml y se guarda en el diccionario creado la información que necesitamos
for child in root:
    documento = {"author":[]}
    if child.tag in document_types: #el tipo de documento nos interesa
        documento["type"]=child.tag
        for elem in child:
            if elem.tag in attributes:
                if elem.tag == "year":
                    documento[elem.tag]=int(elem.text)
                elif elem.tag == "author":
                    autor = {"Author":elem.text}
                    documento[elem.tag].append(autor)
                else:
                    documento[elem.tag]=elem.text
        dblp["dblp"].append(documento)

#se guarda el diccionario en un documento json
with open("output.json",'w') as f:
    json.dump(dblp,f,indent=4)
