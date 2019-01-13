import pymongo
import json

from pymongo import MongoClient

#se realiza una conexión con mongo
conex = pymongo.MongoClient()

#se crean la base de datos y la colección necesarias
db = conex.practica #base de datos: practica
col = db.dblp #colección: dblp

#se carga el documento json
with open("output.json",'r') as f:
    my_json= json.load(f)

documents = my_json["dblp"]

#se van guardando los documentos de uno en uno en la colección indicada
for doc in documents:
    col.insert(doc)
