import xml.etree.ElementTree as ET
import pandas as pd
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

#se crean las listas con los valores que necesitamos
document_types = ["article","inproceedings","incollection"]

#Se crean los diccionarios que necesitamos para los nodos y las relaciones
#Nodos de los autores
authors_dict = OrderedDict()
authors_dict["authorId:ID(Authors)"] = []
authors_dict["name"] = []
authors_dict[":LABEL"] = []
#Nodos de los documentos
documents_dict = OrderedDict()
documents_dict["documentId:ID(Documents)"] = []
documents_dict["title"] = []
documents_dict["type"] = []
documents_dict["year"] = []
documents_dict[":LABEL"] = []
#Relaciones entre autores
relationshipsAA_dict = OrderedDict()
relationshipsAA_dict[":START_ID(Authors)"] = []
relationshipsAA_dict[":END_ID(Authors)"] = []
relationshipsAA_dict[":TYPE"] = []
relationshipsAA_dict["title"] = []
relationshipsAA_dict["type"] = []
relationshipsAA_dict["year"] = []
#Relaciones entre autores y documentos
relationshipsAP_dict = OrderedDict()
relationshipsAP_dict[":START_ID(Authors)"] = []
relationshipsAP_dict[":END_ID(Documents)"] = []
relationshipsAP_dict[":TYPE"] = []

#Inicializamos los ids para que empiecen en 1
authorId = 1
documentId = 1

#Se crea un diccionario auxiliar para los autores, para evitar repeticiones
aux_authors_dict = OrderedDict()

#Procedemos a la creación de los nodos, para ello será necesario recorrer el xml
for child in root:
    if child.tag in document_types: #el tipo de documento nos interesa
        AA_rel_list = [] #array auxiliar para poder crear las relaciones entre autores
        year_AA = None
        for elem in child:
            if elem.tag == "title":
                #creamos el nodo publicacion
                documents_dict["documentId:ID(Documents)"].append(documentId)
                myId = documentId
                documentId +=1
                documents_dict["title"].append(elem.text)
                documents_dict[":LABEL"].append("Document")
                title_AA = elem.text
                documents_dict["type"].append(child.tag)
                type_AA = child.tag
            elif elem.tag == "author":
                #creamos el nodo autor si no está creado ya
                if elem.text not in aux_authors_dict:
                    authors_dict["authorId:ID(Authors)"].append(authorId)
                    aux_authors_dict[elem.text] = authorId
                    authorId += 1
                    authors_dict["name"].append(elem.text)
                    authors_dict[":LABEL"].append("Author")
                AA_rel_list.append(aux_authors_dict[elem.text])
            elif elem.tag == "year":
                documents_dict["year"].append(int(elem.text))
                year_AA = elem.text
        #hay 6 documentos en los que no hay atributo fecha y, como no vamos a realizar consultas relacionadas, decidimos completar con 4 ceros
        if year_AA == None:
            documents_dict["year"].append(0000)
        # Una vez creados los nodos del documento y los autores, será necesario crear
        # las relaciones entre los autores si hay más de uno y entre el documento
        # y los autores que lo han creado
        for author in range(len(AA_rel_list)):
            relationshipsAP_dict[":START_ID(Authors)"].append(AA_rel_list[author])
            relationshipsAP_dict[":END_ID(Documents)"].append(myId)
            relationshipsAP_dict[":TYPE"].append("Authorship")
            for coauthor in range(author+1,len(AA_rel_list)):
                relationshipsAA_dict[":START_ID(Authors)"].append(AA_rel_list[author])
                relationshipsAA_dict[":END_ID(Authors)"].append(AA_rel_list[coauthor])
                relationshipsAA_dict[":TYPE"].append("Collaboration")
                relationshipsAA_dict["title"].append(title_AA)
                relationshipsAA_dict["type"].append(type_AA)
                relationshipsAA_dict["year"].append(year_AA)

#Una vez completados los diccionarios de nodos y relaciones, hay que pasarlos a DataFrame
authors = pd.DataFrame(authors_dict)
documents = pd.DataFrame(documents_dict)
AA_relationships = pd.DataFrame(relationshipsAA_dict)
AP_relationships = pd.DataFrame(relationshipsAP_dict)

#Se copian esos dataframe en ficheros CSV
authors.to_csv("authors.csv", index=False)
documents.to_csv("documents.csv", index=False)
AA_relationships.to_csv("AA_relationships.csv", index=False)
AP_relationships.to_csv("AP_relationships.csv", index=False)