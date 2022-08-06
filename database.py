"""
DatabaseModel
version 1.0.0
date 2022
auther Mohammad Sadegh Masoumi
"""

import re
import json
from pathlib import Path


class DatabaseModel:
    """database class"""

    def __init__(self, name='default') -> None:
        """initial object"""
        self.name = name
        self.db = {}

    def set_data(self, key: str, value) -> None:
        """set key:value in database"""
        if isinstance(key, str):
            self.db.update({key: value})
        else:
            raise KeyError('key value most be string')

    def exist(self, key: str) -> bool:
        """This function checks that the key is in the database"""
        if key not in self.db.keys():
            raise KeyError('This key does not exist in the database')
        return True

    def get_data(self, key) -> None:
        """get value of key from database"""
        self.exist(key)
        return self.db.get(key)

    def delete(self, key) -> None:
        """delete key from database"""
        self.exist(key)
        del self.db[key]

    def get_keys_by_regex(self, regex):
        """get keys by regex"""
        regex = re.compile(regex)
        return list(filter(lambda key: regex.search(key), self.db.keys()))

    def dump(self, filepath=None) -> None:
        """export database to file"""
        if filepath is None:
            filepath = Path(__file__).parent
        else:
            Path(filepath).mkdir(parents=True, exist_ok=True)
            filepath = Path(filepath)
        filepath = filepath / (str(self.name) + '.json')

        with open(filepath, 'w') as file:
            file.write(json.dumps(self.db, indent=4))

    def __repr__(self):
        """representation of obj"""
        return str(self.name)

    def __str__(self) -> str:
        """convert obj to string"""
        return str(self.name)
