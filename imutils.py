import numpy as np
from PIL import Image
import imagehash
import numpy

def get_hash(img: Image):
    hash_image = imagehash.average_hash(img)
    return hash_image

def read_image(name: str):
    img = Image.open(name)
    my_hash = get_hash(img)
    img = np.asarray(img)
    return img, my_hash

if __name__ == "__main__":
    one, two = read_image("jelly1.png")
    print(two)
    print(one)