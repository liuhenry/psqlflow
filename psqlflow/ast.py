from parser import parse
from utils import infer_qualified_name


def _get_node_type(node):
    if isinstance(node, dict):
        keys = node.keys()
        if len(keys) == 1:
            return keys[0]


class AST(object):
    """
    Stolen from the Python AST module :)
    https://hg.python.org/cpython/file/2.7/Lib/ast.py

    A node visitor base class that walks the abstract syntax tree and calls a
    visitor function for every node found.  This function may return a value
    which is forwarded by the `visit` method.

    This class is meant to be subclassed, with the subclass adding visitor
    methods.

    Per default the visitor functions for the nodes are ``'visit_'`` +
    class name of the node.  So a `TryFinally` node visit function would
    be `visit_TryFinally`.  This behavior can be changed by overriding
    the `visit` method.  If no visitor function exists for a node
    (return value `None`) the `generic_visit` visitor is used instead.
    """

    def __init__(self, query):
        self.query = query
        self.ast = parse(self.query)
        self.flows = []
        self.inputs = set()
        self.outputs = set()
        self.traverse(self.ast)

    def trace_input_table(self, name):
        """Recursively returns all descendent tables using this input table in the graph"""
        child_tables = set()
        descendent_tables = set()
        for flow in self.flows:
            if name in flow['input']:
                if name in self.outputs:
                    descendent_tables.add(flow['output'])
                else:
                    child_tables.add(flow['output'])
        for name in child_tables:
            for table in self.trace_input_table(name):
                descendent_tables.add(table)
        return child_tables.union(descendent_tables)

    def traverse(self, root):
        """Starts tree traversal"""
        if isinstance(root, list):
            for node in root:
                self.visit(node)
        else:
            self.visit(root)

    def visit(self, node):
        """Visit a node."""
        node_type = _get_node_type(node)
        node_actual = node[node_type]
        method = 'visit_' + node_type
        visitor = getattr(self, method, None)
        if visitor is None:
            return self.generic_visit(node_type, node[node_type])
        else:
            return visitor(node[node_type])

    def _add_statement_flow(self, input_tables, output_table):
        if not isinstance(input_tables, list):
            input_tables = [input_tables]

        self.flows.append({
            'input': set(input_tables),
            'output': output_table,
        })

    def _add_query_inputs(self, tables):
        if not isinstance(tables, list):
            tables = [tables]

        for table in tables:
            if not table in self.outputs:
                self.inputs.add(table)

    def _add_query_output(self, table):
        self.outputs.add(table)

    def _remove_query_output(self, table):
        self.outputs.discard(table)

    def generic_visit(self, node_type, node):
        """Called if no explicit visitor function exists for a node."""
        print "Generic visit:", node_type
        # print node

    def visit_String(self, node_actual):
        """Leaf Node"""
        return node_actual['str']

    def visit_RangeVar(self, node_actual):
        """Leaf Node"""
        if node_actual.get('schemaname'):
            table_name = "{}.{}".format(
                node_actual['schemaname'],
                node_actual['relname'])
        else:
            table_name =  node_actual['relname']

        return table_name

    def visit_JoinExpr(self, node_actual):
        tables = []
        larg = self.visit(node_actual['larg'])
        rarg = self.visit(node_actual['rarg'])

        for child in [larg, rarg]:
            if isinstance(child, list):
                tables.extend(child)
            else:
                tables.append(child)
        return tables

    def visit_RangeSubselect(self, node_actual):
        return self.visit(node_actual['subquery'])

    def visit_IntoClause(self, node_actual):
        return self.visit(node_actual['rel'])

    def visit_BoolExpr(self, node_actual):
        tables = []
        for arg in node_actual['args']:
            arg_tables = self.visit(arg)
            if arg_tables:
                for table in arg_tables:
                    tables.append(table)
        return tables

    def visit_SubLink(self, node_actual):
        return self.visit(node_actual['subselect'])

    def visit_DropStmt(self, node_actual):
        for obj in node_actual['objects']:
            references = [self.visit(child) for child in obj]
            self._remove_query_output('.'.join(references))

    def visit_RenameStmt(self, node_actual):
        old_table = self.visit(node_actual['relation'])
        new_table = infer_qualified_name(old_table, node_actual['newname'])
        self._add_statement_flow(
            old_table,
            new_table)
        self._add_query_inputs(old_table)
        self._add_query_output(new_table)
        self._remove_query_output(old_table)

    def visit_CreateTableAsStmt(self, node_actual):
        input_tables = self.visit(node_actual['query'])
        output_table = self.visit(node_actual['into'])
        self._add_statement_flow(input_tables, output_table)

        self._add_query_inputs(input_tables)
        self._add_query_output(output_table)

    def visit_InsertStmt(self, node_actual):
        input_tables = self.visit(node_actual['selectStmt'])
        output_table = self.visit(node_actual['relation'])

        self._add_statement_flow(input_tables, output_table)

        self._add_query_inputs(input_tables)
        self._add_query_output(output_table)

    def visit_SelectStmt(self, node_actual):
        def add_val(val):
            if val:
                if isinstance(val, list):
                    tables.extend(val)
                else:
                    tables.append(val)

        tables = []
        if node_actual.get('fromClause'):
            for child in node_actual['fromClause']:
                add_val(self.visit(child))


        if node_actual.get('larg'):
            add_val(self.visit(node_actual['larg']))

        if node_actual.get('rarg'):
            add_val(self.visit(node_actual['rarg']))

        if node_actual.get('whereClause'):
            add_val(self.visit(node_actual['whereClause']))

        self._add_query_inputs(tables)
        return tables
