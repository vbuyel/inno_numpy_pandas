# PostgreSQL BoM explosion

The Python entry point loads and cleans CSV/Excel data. PostgreSQL performs
the annual aggregation and recursive BoM explosion. The final `year` always
comes from the FIN root and represents the year when that product is saleable.

## Setup

```bash
python3 -m pip install -r task_2/sql/requirements.txt
python3 -m task_2.sql.main
```

Configuration is loaded automatically from `task_2/sql/.env`.

Pass another input file or save the report as CSV:

```bash
python3 -m task_2.sql.main path/to/bom.xlsx --output report.csv
```

Each run replaces the contents of `bom_source`. PostgreSQL exposes:

- `bom_annual`: monthly source rows aggregated to annual BoM edges.
- `bom_explosion`: complete hierarchy for every plant, FIN material, and year.
- `bom_report`: persisted result refreshed on every pipeline run.

The recursive view excludes the FIN-to-PROD wrapper edge, stops at ADD/RM
components, and tracks visited materials to prevent cycles.

## Structure

- `config.py`: immutable application configuration and source schema.
- `loader.py`: extensible CSV/Excel readers and source cleaning.
- `repository.py`: PostgreSQL persistence and report queries.
- `queries.py`: individual PostgreSQL DDL and view statements.
- `services.py`: aggregation, explosion, and pipeline use cases.
- `main.py`: dependency composition and command-line interface.
