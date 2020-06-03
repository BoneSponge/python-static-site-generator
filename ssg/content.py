import re

from collections.abc import Mapping
from yaml import load, FullLoader


class Content(Mapping):
    __delimeter = r"^(?:-|+){3}\s*$"  # Remember to prefix string with r to denote raw string
    __regex = re.compile(__delimiter, re.MULTILINE)

    @classmethod
    def load(cls, string):  # self parameter is not included because it is outside the instance method i.e. __init__
        # but still within the class definition
        _, fm, content = cls.__regex.split(string, 2)
        metadata = load(fm, Loader=FullLoader)
        return cls(metadata, content)

    def __init__(self, metadata, content):
        self.data = metadata
        self.data["content"] = content  # Use this syntax for assigning key-value pairs

    @property
    def body(self):
        return self.data['content']

    @property
    def type(self):
        return self.data['type'] if "type" in self.data else None  # ternary if refers to an inline if

    @type.setter
    def type(self, type):
        self.data['type'] = type

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        self.data.__iter__()  # Literally calls iterator method upon self.data

    def __len__(self):
        return len(self.data)

    @property
    def __repr__(self):
        data = {}
        for key, value in self.data.items():
            if key != "content":
                data[key] = value
        return str(data)
