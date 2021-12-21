from difflib import SequenceMatcher
from image_info import ImageInfo

def search(text: str, database: dict) -> None:
    """Returns the most common to text image id"""
    return max([
        (SequenceMatcher(None, database[element].text, text).ratio(), element) 
        for element in database
    ])[1]


if __name__ == '__main__':
    database = dict()
    database[6] = ImageInfo(hash ="h12", text="string1")
    database[4] = ImageInfo(hash ="h22", text="string2")
    print(search("string31", database))