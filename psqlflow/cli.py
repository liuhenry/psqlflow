import argparse
from sys import stdout
from .ast import AST
from .printers import JsonPrinter, GraphPrinter


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description='Parses PostgreSQL query into dependency and output graph.')
    parser.add_argument("sql",
                        help="Input file for SQL query",
                        type=file)
    parser.add_argument("-o", "--output",
                        help="Output file",
                        type=argparse.FileType('w'),
                        default=stdout)
    parser.add_argument("-t", "--trace",
                        help=("By default, we only output the flows that cross the query interface."
                              "Pass trace to show intermediate flows as well."),
                        action="store_true",
                        default=False)
    args = parser.parse_args()
    query = args.sql.read()
    graph = AST(query)

    output = GraphPrinter(graph, global_schema_exclusions=['workers'])
    g = output.statement_flows() if args.trace else output.global_flows()
    g.draw(args.output, format='png', prog='dot')

if __name__ == '__main__':
    main()
