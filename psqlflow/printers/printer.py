from psqlflow.utils import get_schema_from_name


class Printer(object):
    """Generic AST Printer Class"""

    def __init__(self, ast, global_schema_exclusions=None):
        self.ast = ast
        self.global_schema_exclusions = global_schema_exclusions or []

    def without_schema_exclusions(self, table_set):
        return (table for table in table_set if not get_schema_from_name(table) in self.global_schema_exclusions)
