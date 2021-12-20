
from difflib import SequenceMatcher

def search(text: str, database: dict) -> None:
    """Returns the most common to text image id"""
    return max([
        (SequenceMatcher(None, database[element][0], text).ratio(), database[element][0]) 
        for element in database
    ])[1]


if __name__ == '__main__':
    database = dict()
    database[0] = ("string1", "h1")
    database[1] = ("string2", "h2")
    print(search("string31", database))