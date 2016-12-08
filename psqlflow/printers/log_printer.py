from printer import Printer


class LogPrinter(Printer):

    def print_statement_flows(self):
        """Print the input/output tables for each statement"""
        print "\n===== Start Statement Flow Trace =====\n"
        for flow in self.ast.flows:
            self._print_flow_out(flow['input'], [flow['output']])
        print "\n===== End Statement Flow Trace =====\n"

    def print_global_flows(self):
        """Print the input/output tables for each statement"""
        print "\n===== Start Global Flow Trace =====\n"
        for table in sorted(self.without_schema_exclusions(self.ast.inputs)):
            global_outputs = self.ast.trace_input_table(table).intersection(self.ast.outputs)
            self._print_flow_out([table], self.without_schema_exclusions(global_outputs))
            print ""
        print "\n===== End Global Flow Trace =====\n"

    def print_io(self):
        """Shows the overall inputs and outputs of this query"""
        print "\n===== Global Inputs =====\n"
        for table in sorted(self.without_schema_exclusions(self.ast.inputs)):
            print table
        print "\n===== Global Outputs =====\n"
        for table in sorted(self.without_schema_exclusions(self.ast.outputs)):
            print table

    def _print_flow_in(self, input_tables, output_table):
        for t in sorted(input_tables):
            print t
        print "\t > {}\n".format(output_table)

    def _print_flow_out(self, input_tables, output_tables):
        for t in sorted(input_tables):
            print t
        for t in sorted(output_tables):
            print "\t > {}".format(t)
        print ''
