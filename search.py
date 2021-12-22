from scipy.sparse import data
from image_info import ImageInfo
from sklearn.neighbors import NearestNeighbors
#from skmultiflow.lazy import KNNClassifier
import numpy as np
from gensim.models import Word2Vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def search(text: str, database: dict) -> None:
    """Returns the most common to text image id"""
    sentences = [list(text.lower().split())]
    for elem in database.values():
        sentences.append(list(elem.text.split()))
    model = Word2Vec(sentences, min_count=1, vector_size=300)
    text_vectors = [model.wv[word] for word in text.split()]
    text_vector = np.mean(text_vectors, axis=0)
    X = list()
    keys = [elem for elem in database]
    for elem in database:
        data_vectors = [model.wv[word] for word in database[elem].text.split()]
        data_vector = list(np.mean(data_vectors, axis=0))
        X.append(data_vector)
    k = min(3, len(database))
    neigh = NearestNeighbors(n_neighbors=k)
    neigh.fit(X)
    dist, ind = neigh.kneighbors([text_vector], n_neighbors=k, return_distance=True)
    return [keys[ind[0][i]] for i in range(k)]

if __name__ == '__main__':
    database = dict()
    database[6] = ImageInfo(hash ="h12", text="Supervised learning wow")
    database[4] = ImageInfo(hash ="h22", text="food is tasty! Go to the restaurant")
    print(search("pizza", database))