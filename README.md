# psqlflow

A static analysis tool for ETL jobs written in PostgreSQL.

psqflow can analyze a file containing one or more statements to produce:
* A "global graph" of table dependencies + exports at the boundaries of the ETL job
* A "trace graph" of tables flowing through the ETL job


Under the hood, psqflow uses [libpg_query](https://github.com/lfittl/libpg_query) to access the internal PostgresSQL parse tree and Python glue code from [psqlparse](https://github.com/alculquicondor/psqlparse).

## Installation
[parser.c](psqlflow/parser/parser.c) is included in the distribution, so Cython should not be needed.
However, this will still need to download and compile libpg_query for inclusion.
```
python setup.py install
```

## Usage
```
psqlflow exec_dash.sql -o global_graph.png
```