
# PAULA CARBALLO PÉREZ Y ESTER CORTÉS GARCÍA

import networkx as nx
import matplotlib.pyplot as plt
import requests
import xml.etree.ElementTree as ET
from collections import OrderedDict
import os
from networkx.readwrite import json_graph
import json


# Métodos que se emplean para obtener la información necesaria
# Método para obtener los xml con los datos de los usuarios y coger la información que nos interesa guardándola en un json
def get_data_user(user_item,id):
    # Se realiza la petición a la api y se guarda en un xml
    user_url = "https://www.goodreads.com/user/show/"+str(id)+".xml"
    parameters = {"key": api_key}
    response_url = requests.get(user_url, params=parameters)
    with open("User_User"+str(user_item)+".xml", "wb") as file:
        file.write(response_url.content)
    file.close()
    # Recorro el xml guardando los datos que nos interesan en un json
    user = OrderedDict()
    user_attributes = ["id","name","user_name","link","image_url","small_image_url","age","gender","location","joined","last_active","friends_count","user_shelves"]
    tree = ET.parse("User_User"+str(user_item)+".xml")
    root = tree.getroot()
    for child in root:
        if child.tag == "user":
            user["type"] = "user"
            for elem in child:
                if elem.tag in user_attributes:
                    if elem.tag == "id":
                        user["id"] = int(elem.text)
                    elif elem.tag == "name":
                        user["name"] = elem.text
                    elif elem.tag == "user_name":
                        user["user_name"] = elem.text
                    elif elem.tag == "link":
                        user["link"] = elem.text
                    elif elem.tag == "image_url":
                        user["image_url"] = elem.text
                    elif elem.tag == "small_image_url":
                        user["small_image_url"] = elem.text
                    elif elem.tag == "age":
                        user["age"] = elem.text
                    elif elem.tag == "gender":
                        user["gender"] = elem.text
                    elif elem.tag == "location":
                        user["location"] = elem.text
                    elif elem.tag == "joined":
                        user["joined"] = elem.text
                    elif elem.tag == "last_active":
                        user["last_active"] = elem.text
                    elif elem.tag == "friends_count":
                        user["friends_count"] = elem.text
                    elif elem.tag == "user_shelves":
                        count_shelves = 0
                        count_books = 0
                        shelves = []
                        for shelf in elem:
                            count_shelves += 1
                            aux = []
                            for element in shelf:
                                if element.tag == "name":
                                    aux.append(element.text)
                                if element.tag == "book_count":
                                    count_books += int(element.text)
                                    aux.append(element.text)
                            shelves.append(aux)
                        user["num_books"] = count_books
                        user["num_shelves"] = count_shelves
                        user["shelves_info"] = shelves
    return user

# Método para obtener los xml con los libros de los usuarios y coger la información que nos interesa guardándola en un json
def get_books_user(user_item,id,graph):
    # Se realiza la petición a la api y se guardan los datos en un xml
    book_list_url = "https://www.goodreads.com/review/list/"+str(id)+".xml"
    parameters={"key":api_key,"v":2}
    response_url = requests.get(book_list_url,params=parameters)
    with open("BookList_User"+str(user_item)+".xml", "wb") as file:
        file.write(response_url.content)
    file.close()
    # Se recorre el xml guardando cada uno de los libros en un json diferente
    # Además, como los libros contienen información de los autores que no podemos conseguir después, se crea una
    # una lista extra de diccionarios, donde cada diccionario es un autor de los libros que vamos analizando
    authors_info = []
    book_attributes = ["id", "isbn", "isbn13", "title", "title_without_series", "image_url", "small_image_url", "link", "num_pages", "publisher", "publication_day", "publication_year", "publication_month", "average_rating",
                       "description", "authors"]
    tree = ET.parse("BookList_User" + str(user_item) + ".xml")
    root = tree.getroot()
    for child in root:
        if child.tag == "reviews":
            count = 0
            for review in child:
                if review.tag == "review":
                    count += 1
                    book = OrderedDict()
                    for book_elem in review:
                        if book_elem.tag == "book":
                            book["type"] = "book"
                            for book_attribute in book_elem:
                                if book_attribute.tag in book_attributes:
                                    if book_attribute.tag == "id":
                                        book["id"] = book_attribute.text
                                    elif book_attribute.tag == "isbn":
                                        book["isbn/isbn13"] = book_attribute.text
                                    elif book_attribute.tag == "isbn13":
                                        book["isbn/isbn13"] = book["isbn/isbn13"]+"/"+book_attribute.text
                                    elif book_attribute.tag == "title":
                                        book["title"] = book_attribute.text
                                    elif book_attribute.tag == "title_without_series":
                                        book["title_without_series"] = book_attribute.text
                                    elif book_attribute.tag == "image_url":
                                        book["image_url"] = book_attribute.text
                                    elif book_attribute.tag == "small_image_url":
                                        book["small_image_url"] = book_attribute.text
                                    elif book_attribute.tag == "link":
                                        book["link"] = book_attribute.text
                                    elif book_attribute.tag == "num_pages":
                                        book["num_pages"] = book_attribute.text
                                    elif book_attribute.tag == "publisher":
                                        book["publisher"] = book_attribute.text
                                    elif book_attribute.tag == "publication_day":
                                        book["publication_day"] = book_attribute.text
                                    elif book_attribute.tag == "publication_month":
                                        book["publication_month"] = book_attribute.text
                                    elif book_attribute.tag == "publication_year":
                                        book["publication_year"] = book_attribute.text
                                    elif book_attribute.tag == "average_rating":
                                        book["average_rating"] = book_attribute.text
                                    elif book_attribute.tag == "description":
                                        book["description"] = book_attribute.text
                                    elif book_attribute.tag == "description":
                                        book["description"] = book_attribute.text
                                    elif book_attribute.tag == "authors":
                                        for author in book_attribute:
                                            author_attributes = OrderedDict()
                                            book["author"] = []
                                            author_attributes["type"] = "author"
                                            for attribute in author:
                                                if attribute.tag == "id":
                                                    author_attributes["id"] = attribute.text
                                                elif attribute.tag == "name":
                                                    book["author"].append(attribute.text)
                                                    author_attributes["name"] = attribute.text
                                                elif attribute.tag == "image_url":
                                                    author_attributes["image_url"] = attribute.text
                                                elif attribute.tag == "small_image_url":
                                                    author_attributes["small_image_url"] = attribute.text
                                                elif attribute.tag == "link":
                                                    author_attributes["link"] = attribute.text
                                                elif attribute.tag == "average_rating":
                                                    author_attributes["average_rating"] = attribute.text
                                            authors_info.append([book["title"],author_attributes])
                nodes = graph.nodes()
                if book["title"] not in nodes:
                    g.add_node(book["title"], information=book)
                if user_item == 1:
                    g.add_edge(book["title"],"Ester Cortes")
                else:
                    g.add_edge(book["title"],"Paula Carballo")
    return authors_info

# Método para obtener los xml con los datos que nos faltande los autores y coger la información que nos interesa
# guardándola en un json
def get_data_author(pair,user,graph):
    # Se realiza la petición a la api sacando el id del diccionario del autor
    info = pair[1]
    id = info["id"]
    author_book_list_url = "https://www.goodreads.com/author/list/"+str(id)
    parameters={"format":"xml","key":api_key}
    response_url = requests.get(author_book_list_url,params=parameters)
    with open("Author"+str(count)+"_Information.xml", "wb") as file:
        file.write(response_url.content)
    file.close()
    # Se coge la información relativa a los libros que ha escrito el autor y se guarda en el diccionario ya creado
    books = []
    book_attributes = ["id", "isbn", "isbn13", "title", "title_without_series", "image_url", "small_image_url",
                         "link", "num_pages", "publisher", "publication_day", "publication_year", "publication_month",
                         "average_rating", "description", "authors"]
    tree = ET.parse("Author"+str(count)+"_Information.xml")
    root = tree.getroot()
    for child in root:
        if child.tag == "author":
            for attr in child:
                if attr.tag == "books":
                    attributes = attr.attrib
                    info["total_books"] = attributes["total"]
                    for elem in attr:
                        if elem.tag == "book":
                            book = OrderedDict()
                            book["type"] = "book"
                            for attribute in elem:
                                if attribute.tag in book_attributes:
                                    if attribute.tag == "id":
                                        book["id"] = attribute.text
                                    elif attribute.tag == "isbn":
                                        if attribute.text != None:
                                            book["isbn/isbn13"] = attribute.text
                                        else:
                                            book["isbn/isbn13"] = "Does not exist"
                                    elif attribute.tag == "isbn13":
                                        if attribute.text != None:
                                            book["isbn/isbn13"] = book["isbn/isbn13"] + "/" + attribute.text
                                        else:
                                            book["isbn/isbn13"] = book["isbn/isbn13"] + "/Does not exist"
                                    elif attribute.tag == "title":
                                        book["title"] = attribute.text
                                    elif attribute.tag == "title_without_series":
                                        book["title_without_series"] = attribute.text
                                    elif attribute.tag == "image_url":
                                        book["image_url"] = attribute.text
                                    elif attribute.tag == "small_image_url":
                                        book["small_image_url"] = attribute.text
                                    elif attribute.tag == "link":
                                        book["link"] = attribute.text
                                    elif attribute.tag == "num_pages":
                                        book["num_pages"] = attribute.text
                                    elif attribute.tag == "publisher":
                                        book["publisher"] = attribute.text
                                    elif attribute.tag == "publication_day":
                                        book["publication_day"] = attribute.text
                                    elif attribute.tag == "publication_month":
                                        book["publication_month"] = attribute.text
                                    elif attribute.tag == "publication_year":
                                        book["publication_year"] = attribute.text
                                    elif attribute.tag == "average_rating":
                                        book["average_rating"] = attribute.text
                                    elif attribute.tag == "description":
                                        book["description"] = attribute.text
                                    elif attribute.tag == "description":
                                        book["description"] = attribute.text
                                    elif attribute.tag == "authors":
                                        for person in attribute:
                                            book["author"] = []
                                            for attribut in person:
                                                if attribut.tag == "name":
                                                    book["author"].append(attribut.text)
                            books.append(book)
    nodes = graph.nodes()
    if info["name"] not in nodes:
        g.add_node(info["name"], information=info)
        g.add_edge(pair[0],info["name"])
    else:
        g.add_edge(pair[0],info["name"])

    for element in books:
        if element["title"] not in nodes:
            g.add_node(element["title"], information=element)
            g.add_edge(info["name"], element["title"])

# Método para guardar la información del usuario en un nodo
def user_node (data,graph):
    nodes = graph.nodes()
    if nodes == []:
        g.add_node(data["name"],information=data)
    else:
        if data["name"] not in nodes:
            g.add_node(data["name"], information=data)
            g.add_edge(data["name"],"Ester Cortes")

#Método para pintar el grafo
def paint_graph(g):
    layout = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, layout, node_size=1000, node_color='blue', alpha=0.3)
    nx.draw_networkx_edges(g, layout)
    nx.draw_networkx_labels(g, layout, font_size=12, font_family='sans-serif')
    plt.show()

#Método para guardar el grafo
def save_graph(graph):
    g_json = json_graph.node_link_data(graph)
    with open("graph.json","w") as file:
        json.dump(g_json,file,indent=1)
    file.close()

def delete_xml():
    # Se borran los ficheros xml que se habían usado de manera provisional para obtener la información necesaria
    mydir = "."
    filelist = [f for f in os.listdir(mydir) if f.endswith(".xml")]
    for f in filelist:
        os.remove(os.path.join(mydir, f))

#Método para borrar los xml temporales
if __name__ == "__main__":
    # Variables
    g = nx.Graph()
    mydir = "."
    api_key = "" # valor de la api key de la persona que realiza la petición
    id_users = [80683105, 79635022]
    user = 0
    # Dados los id de los 2 usuarios que se quieren analizar en el grafo
    for id in id_users:
        user += 1
        # Obtener el xml del usuario donde se encuentran sus datos personales
        data_user = get_data_user(user, id)
        # Crear el nodo del autor
        user_node(data_user,g)
        # Obtener el xml con los datos de libros que tiene el usuario en sus estanterías
        authors_information = get_books_user(user, id,g)
        # Obtener la información que nos falta del autor y que no hemos obtenido en el anterior xml
        count = 0
        for author in authors_information:
            get_data_author(author,user,g)
    paint_graph(g)
    save_graph(g)
    delete_xml()



