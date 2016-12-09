import json
from collections import defaultdict
from .printer import Printer


class JsonPrinter(Printer):
    """
    Prints flows to stdout
    """
    def __init__(self, *args, **kwargs):
        super(JsonPrinter, self).__init__(*args, **kwargs)

    def new_obj(self):
        return defaultdict(set)

    @staticmethod
    def add_edge(obj, a, b):
        obj[a].add(b)
