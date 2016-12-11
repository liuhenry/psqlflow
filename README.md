# psqlflow

A static analysis tool for ETL jobs written in PostgreSQL.

psqflow can analyze a file containing one or more statements to produce:
* A "global graph" of table dependencies + exports at the boundaries of the ETL job
* A "trace graph" of tables flowing through the ETL job


Under the hood, psqflow uses [libpg_query](https://github.com/lfittl/libpg_query) to access the internal PostgreSQL parser outside of a PostgreSQL server and the Cython interface code from [psqlparse](https://github.com/alculquicondor/psqlparse) to talk to the parser from Python.

## Installation
[parser.c](psqlflow/parser/parser.c) is included in the distribution, so Cython should not be needed.
The build process will still need to download and compile libpg_query for inclusion.
```
python setup.py install
```

## Usage
Given a sample job:
```SQL
CREATE TABLE IF NOT EXISTS analytics.users_computed AS (
    SELECT *
    FROM application.users
    LEFT JOIN application.friends USING (user_id)
);

CREATE TABLE IF NOT EXISTS workers.activities_computed AS (
    SELECT *
    FROM application.activities
    JOIN application.activity_logs USING (activity_id)
);

INSERT INTO analytics.dashboard (
    SELECT *
    FROM analytics.users_computed
    JOIN workers.activities_computed USING (user_id)
);
```
### Global Graph
Shows how the input tables flow to the output tables
```
psqlflow exec_dash.sql -o global_graph.png
```
![Global Graph](../gh-pages/assets/images/global_graph.png?raw=true "Global Graph")

### Trace Graph
Shows a complete flow of all tables, including temporary and intermediate tables dropped at the end of the query
```
psqlflow exec_dash.sql -t -o trace_graph.png
```
![Trace Graph](../gh-pages/assets/images/trace_graph.png?raw=true "Trace Graph")
