from pathlib import Path

_STATEMENTS_DIR = Path(__file__).parent / "statements"


def _load_sql(filename: str) -> str:
    return (_STATEMENTS_DIR / filename).read_text(encoding="utf-8").strip()


DROP_EXPLOSION_VIEW = _load_sql("drop_explosion_view.sql")
DROP_ANNUAL_VIEW = _load_sql("drop_annual_view.sql")
CREATE_SOURCE_TABLE = _load_sql("create_source_table.sql")
CREATE_REPORT_TABLE = _load_sql("create_report_table.sql")
CREATE_SOURCE_MATERIAL_INDEX = _load_sql("create_source_material_index.sql")
CREATE_SOURCE_FIN_INDEX = _load_sql("create_source_fin_index.sql")
CREATE_REPORT_INDEX = _load_sql("create_report_index.sql")
CREATE_ANNUAL_VIEW = _load_sql("create_annual_view.sql")
CREATE_EXPLOSION_VIEW = _load_sql("create_explosion_view.sql")

SCHEMA_QUERIES = (
    DROP_EXPLOSION_VIEW,
    DROP_ANNUAL_VIEW,
    CREATE_SOURCE_TABLE,
    CREATE_REPORT_TABLE,
    CREATE_SOURCE_MATERIAL_INDEX,
    CREATE_SOURCE_FIN_INDEX,
    CREATE_REPORT_INDEX,
    CREATE_ANNUAL_VIEW,
    CREATE_EXPLOSION_VIEW,
)
