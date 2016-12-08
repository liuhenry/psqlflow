import sys
from ast import AST
from printers import LogPrinter


query = open(sys.argv[1]).read()
graph = AST(query)

output = LogPrinter(graph, global_schema_exclusions=['workers'])
output.print_statement_flows()
output.print_io()
output.print_global_flows()
