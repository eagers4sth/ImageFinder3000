from scipy.sparse import data
from image_info import ImageInfo
from sklearn.neighbors import NearestNeighbors
import numpy as np
from gensim.models import Word2Vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def search(text: str, database: dict) -> None:
    """Returns the most common to text image id"""
    sentences = [list(text.lower().split())]
    for elem in database.values():
        sentences.append(list(elem.text.split()))
    model = Word2Vec(sentences, min_count=1, vector_size=2)
    text_vectors = [model.wv[word] for word in text.split()]
    text_vector = np.mean(text_vectors, axis=0)
    X = list()
    keys = [elem for elem in database]
    for elem in database:
        print(database[elem].text)
        data_vectors = [model.wv[word] for word in database[elem].text.split()]
        data_vector = list(np.mean(data_vectors, axis=0))
        X.append(data_vector)
    
    neigh = NearestNeighbors(n_neighbors=2)
    neigh.fit(X)
    dist, ind = neigh.kneighbors([text_vector], n_neighbors=1, return_distance=True)
    #print(dist, id, type(id), id[0])
    return keys[ind[0][0]]

if __name__ == '__main__':
    database = dict()
    database[6] = ImageInfo(hash ="h12", text="Supervised learning wow")
    database[4] = ImageInfo(hash ="h22", text="food is tasty! Go to the restaurant")
    print(search("pizza", database))