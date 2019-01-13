import numpy
import nltk
from bs4 import BeautifulSoup
from textblob import TextBlob
import os
import string
from nltk.corpus import stopwords
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.cluster import adjusted_rand_score


#MÉTODO QUE LEE LAS URL DEL DIRECTORIO
def read_file(file_url):
    try:
        with open(file_url,'r', encoding='utf-8') as f:
            pag = f.read()
        f.close()
    except UnicodeDecodeError:
        with open(file_url,'r', encoding='latin-1') as f:
            pag = f.read()
        f.close()
    bsObj = BeautifulSoup(pag,'html.parser')
    return(bsObj)

#MÉTODO QUE COGE EL CONTENIDO DE LAS NOTICIAS
def get_original_news(url_list):
    print('Se están procesando las 22 noticias')
    text_list = []
    for u in url_list:
        if u.endswith(".html"):
            url = folder + "/" + u
            text = read_file(url)
            original_text = []
            paragraphs = text.find_all('p')
            for paragraph in paragraphs:
                if len(paragraph.getText()) != 0 \
                        and paragraph.getText() != ' ' \
                        and paragraph.getText() != '\xa0':
                    original_text.append(paragraph.getText())
            text_list.append(original_text)
    print('Se han procesado las 22 noticias')
    return text_list

#MÉTODO QUE REALIZA LA TRADUCCIÓN DE LAS NOTICIAS EN ESPAÑOL AL INGLÉS
def translate_news(list_text):
    print('------------TRADUCCIÓN------------------')
    print('Comienza la traducción de los textos que están en español')
    translated_texts = []
    for text in list_text:
        trans_text = []
        for elem in text:
            t = TextBlob(elem)
            language = t.detect_language()
            if language == 'es':
                new_en = t.translate(to='en')
                trans_text.append(str(new_en))
            else:
                trans_text.append(elem)
        translated_texts.append(trans_text)
    print('Se ha completado la traducción de textos')
    return translated_texts

#MÉTODO QUE LOCALIZA LAS ENTIDADES NOMBRADAS
#HAY TRES ETIQUETAS: PERSON + ORGANIZATION + GPE
def extract_entity_names (sentence):
    entity_names = []
    #Se comprueba que el token tenga etiqueta
    if hasattr(sentence,'label') and sentence.label:
        #print(sentence.label)
        #Si es una entity, entonces lo agregamos con los que ya hemos identificado
        if sentence.label() =='GPE':
            entity_names.append(' '.join([child[0] for child in sentence]))
        # En caso contrario, obtenemos todos los hijos del token
        else:
            for child in sentence:
                entity_names.extend(extract_entity_names(child))
    return entity_names

#MÉTODO QUE ELIMINA LOS SIGNOS DE PUNTUACIÓN
def remove_punctuation(words):
    filter_sentence = []
    for word in words:
        if word not in string.punctuation:
            filter_sentence.append(word)
    return filter_sentence

#MÉTODO QUE ELIMINA LAS STOPWORDS INGLESAS
def remove_stopwords(sentence):
    non_stop_sentence = []
    for word in sentence:
        posible = word.lower()
        if posible not in stop:
            non_stop_sentence.append(word)
    return non_stop_sentence 

#OBTIENE EL VOCABULARIO
def cluster_texts(texts, clustersNumber, distance):
    #Load the list of texts into a TextCollection object.
    collection = nltk.TextCollection(texts)
    print("Created a collection of", len(collection), "terms.")

    #get a list of unique terms
    unique_terms = list(set(collection))
    print("Unique terms found: ", len(unique_terms))

    ### And here we actually call the function and create our array of vectors.
    vectors = [numpy.array(TF(f,unique_terms, collection)) for f in texts]
    print("Vectors created.")

    # initialize the clusterer
    clusterer = AgglomerativeClustering(n_clusters=clustersNumber,
                                      linkage="average", affinity=distanceFunction)
    clusters = clusterer.fit_predict(vectors)

    return clusters

# Function to create a TF vector for one document. For each of
# our unique words, we have a feature which is the tf for that word
# in the current document
def TF(document, unique_terms, collection):
    word_tf = []
    for word in unique_terms:
        word_tf.append(collection.tf(word, document))
    return word_tf

#CLASE PRINCIPAL
if __name__ == "__main__":
    stop = set(stopwords.words('english'))
    texts = []
    folder = './Corpus'
    listing = os.listdir(folder)
    original_news = get_original_news(listing)
    translated_texts = translate_news(original_news)

    for element in translated_texts: #se coge cada noticia
        entity_names = []
        for elem in element: #se coge cada párrafo de la noticia
            sentences = nltk.sent_tokenize(elem)
            for s in sentences:
                tokens = nltk.word_tokenize(s)
                #tokens = remove_punctuation(tokens)
                #tokens = remove_stopwords(tokens)
                tagged_sentence = nltk.pos_tag(tokens)
                chunked_sentence = nltk.ne_chunk(tagged_sentence)
                entity_names.extend(extract_entity_names(chunked_sentence))
        texts.append(entity_names)

    print("Prepared ", len(texts), " documents...")
    print("They can be accessed using texts[0] - texts[" + str(len(texts)-1) + "]")

    #distanceFunction ="cosine"
    distanceFunction = "euclidean"
    test = cluster_texts(texts,5,distanceFunction)
    print("test: ", test)
    # Gold Standard
    reference =[0, 5, 0, 0, 0, 2, 2, 2, 3, 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 0, 2, 5]
    print("reference: ", reference)

    # Evaluation
    print("rand_score: ", adjusted_rand_score(reference,test))

