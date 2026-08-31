import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


SOURCE_COLUMNS = [
    "year", "month", "produced_material",
    "produced_material_production_type", "produced_material_release_type",
    "produced_material_quantity", "component_material",
    "component_material_production_type", "component_material_release_type",
    "component_material_quantity", "plant_id",
]
ID_COLUMNS = ["produced_material", "component_material", "plant_id"]
TYPE_COLUMNS = [
    "produced_material_production_type",
    "component_material_production_type",
]
QUANTITY_COLUMNS = [
    "produced_material_quantity",
    "component_material_quantity",
]


@dataclass(frozen=True)
class AppConfig:
    database_url: str

    @classmethod
    def from_environment(cls) -> "AppConfig":
        base_path = Path(__file__).parent
        load_dotenv(base_path / ".env")
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise RuntimeError("DATABASE_URL is not configured")
        return cls(database_url)
