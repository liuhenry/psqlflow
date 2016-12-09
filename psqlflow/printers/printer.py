from ..utils import get_schema_from_name


class Printer(object):
    """
    Generic AST Printer Class
    """
    def __init__(self, ast, global_schema_exclusions=None):
        self.ast = ast
        self.global_schema_exclusions = global_schema_exclusions or []

    def global_flows(self):
        obj = self.new_obj()
        for in_table in sorted(self.without_schema_exclusions(self.ast.inputs)):
            for out_table in self.without_schema_exclusions(self.ast.trace_input_table(table).intersection(self.ast.outputs)):
                self.add_edge(obj, in_table, out_table)
        return obj

    def statement_flows(self):
        obj = self.new_obj()
        for flow in self.ast.flows:
            for in_table in flow['input']:
                self.add_edge(obj, in_table, flow['output'])
        return obj

    def new_obj(self):
        raise NotImplementedError

    @staticmethod
    def add_edge(obj, a, b):
        raise NotImplementedError

    def without_schema_exclusions(self, table_set):
        condition = lambda t: get_schema_from_name(t) in self.global_schema_exclusions
        return (table for table in table_set if not condition(table))

    # def print_io(self):
    #     """Shows the overall inputs and outputs of this query"""
    #     for table in sorted(self.without_schema_exclusions(self.ast.inputs)):
    #         print table
    #     for table in sorted(self.without_schema_exclusions(self.ast.outputs)):
    #         print table
