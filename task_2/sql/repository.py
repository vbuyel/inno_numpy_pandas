from abc import ABC, abstractmethod

import pandas as pd
import psycopg

from .config import SOURCE_COLUMNS
from .queries import SCHEMA_QUERIES


class AbstractBomRepository(ABC):
    @abstractmethod
    def initialize_database(self) -> None:
        pass

    @abstractmethod
    def replace_source(self, frame: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def build_bom_index(self) -> None:
        pass

    @abstractmethod
    def aggregate_bom_to_year(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def explode_fin_material(self, plant: str, year: int, material: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def explode_all(self) -> pd.DataFrame:
        pass


class PostgresBomRepository(AbstractBomRepository):
    def __init__(self, connection: psycopg.Connection):
        self._connection = connection

    def initialize_database(self) -> None:
        for query in SCHEMA_QUERIES:
            self._connection.execute(query)

    def replace_source(self, frame: pd.DataFrame) -> None:
        columns = ", ".join(SOURCE_COLUMNS)
        self._connection.execute("TRUNCATE TABLE bom_source")
        statement = f"COPY bom_source ({columns}) FROM STDIN"
        with self._connection.cursor().copy(statement) as copy:
            for row in frame.itertuples(index=False, name=None):
                copy.write_row(tuple(self._db_value(value) for value in row))

    def build_bom_index(self) -> None:
        self._connection.execute(
            "CREATE INDEX IF NOT EXISTS bom_source_lookup_idx "
            "ON bom_source (plant_id, year, produced_material)"
        )
        self._connection.execute("ANALYZE bom_source")

    def aggregate_bom_to_year(self) -> pd.DataFrame:
        return self._query_frame("SELECT * FROM bom_annual")

    def explode_fin_material(
        self, plant: str, year: int, fin_material: str
    ) -> pd.DataFrame:
        query = """
            SELECT * FROM bom_explosion
            WHERE plant = %s AND year = %s AND fin_material_id = %s
        """
        return self._query_frame(query, (plant, year, fin_material))

    def explode_all(self) -> pd.DataFrame:
        self._connection.execute("TRUNCATE TABLE bom_report")
        self._connection.execute("INSERT INTO bom_report SELECT * FROM bom_explosion")
        query = (
            "SELECT * FROM bom_report "
            "ORDER BY plant, year, fin_material_id, prod_material_id, component_id"
        )
        return self._query_frame(query)

    def _query_frame(self, query: str, params=()) -> pd.DataFrame:
        cursor = self._connection.execute(query, params)
        columns = [column.name for column in cursor.description]
        return pd.DataFrame(cursor.fetchall(), columns=columns)

    @staticmethod
    def _db_value(value):
        if pd.isna(value):
            return None
        return value.item() if hasattr(value, "item") else value
