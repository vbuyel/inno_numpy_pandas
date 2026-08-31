from pathlib import Path
from typing import Protocol

import pandas as pd

from .repository import BomRepository


class SourceLoader(Protocol):
    def load_and_clean_bom(self, source: str | Path) -> pd.DataFrame:
        pass


class BomAggregationService:
    def __init__(self, repository: BomRepository):
        self._repository = repository

    def aggregate_bom_to_year(self) -> pd.DataFrame:
        return self._repository.aggregate_bom_to_year()


class BomExplosionService:
    def __init__(self, repository: BomRepository):
        self._repository = repository

    def explode_fin_material(
        self, plant: str, year: int, fin_material: str
    ) -> pd.DataFrame:
        return self._repository.explode_fin_material(plant, year, fin_material)

    def explode_all(self) -> pd.DataFrame:
        return self._repository.explode_all()


class BomPipeline:
    def __init__(
        self, loader: SourceLoader, repository: BomRepository,
        aggregator: BomAggregationService, exploder: BomExplosionService,
    ):
        self._loader = loader
        self._repository = repository
        self._aggregator = aggregator
        self._exploder = exploder

    def run(self, source: str | Path) -> pd.DataFrame:
        frame = self._loader.load_and_clean_bom(source)
        self._repository.initialize_database()
        self._repository.replace_source(frame)
        self._repository.build_bom_index()
        self._aggregator.aggregate_bom_to_year()
        return self._exploder.explode_all()
