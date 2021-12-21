from collections import defaultdict
from image_info  import ImageInfo
import numpy as np
from gensim.models import Word2Vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def search(text: str, database: dict) -> None:
    """Returns the most common to text image id"""
    sentences = [list(text.split())]
    for elem in database.values():
        sentences.append(list(elem.text.split()))
    model = Word2Vec(sentences, min_count=1)
    text_vectors = [model.wv[word] for word in text.split()]
    text_vector = np.mean(text_vectors, axis=0)
    nearest_text = list()
    for elem in database:
        data_vectors = [model.wv[word] for word in database[elem].text.split()]
        data_vector = np.mean(data_vectors, axis=0)
        nearest_text.append((sum([(text_vector[i]-data_vector[i])**2 for i in range(len(text_vector))]), elem))
    return min(nearest_text)[1]

if __name__ == '__main__':
    database = dict()
    database[6] = ImageInfo(hash ="h12", text="Supervised learning wow")
    database[4] = ImageInfo(hash ="h22", text="food is tasty! Go to the restaurant")
    print(search("I am eating pizza", database))