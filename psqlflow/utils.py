"""
AST Utils
"""

def get_schema_from_name(name):
    """
    Split a qualified table name and return schema.
    If unqualified, return None
    """
    parts = name.split('.')
    if len(parts) == 2:
        return parts[0]
    else:
        return None

def infer_qualified_name(old, new):
    """
    Given a qualified table (schema.table), apply the schema to a new table if unqualified.abs

    (schema.table, table2) -> schema.table2
    """
    schema = get_schema_from_name(old)
    new_parts = new.split('.')

    if len(new_parts) == 2:
        return new

    if schema is not None:
        return "{}.{}".format(schema, new)

    return new
