import pygraphviz as pgv
from .printer import Printer


class GraphPrinter(Printer):
    """
    Exports flows to graphviz
    """
    def __init__(self, *args, **kwargs):
        super(GraphPrinter, self).__init__(*args, **kwargs)

    def new_obj(self):
        return pgv.AGraph(strict=False, directed=True, rankdir='LR')

    @staticmethod
    def add_edge(graph, a, b):
        graph.add_edge(a, b)

