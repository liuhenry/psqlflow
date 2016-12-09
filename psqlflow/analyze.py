import argparse
from ast import AST
from printers import JsonPrinter, GraphPrinter


query = open(sys.argv[1]).read()
graph = AST(query)

output = GraphPrinter(graph, global_schema_exclusions=['workers'])
g = output.statement_flows()
g.layout(prog='dot')
g.draw('output.png')
