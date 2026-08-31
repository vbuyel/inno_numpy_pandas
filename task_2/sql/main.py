import argparse
import logging
from pathlib import Path

import pandas as pd
import psycopg

from .config import AppConfig
from .loader import BomLoader, CsvReader, ExcelReader, ReaderFactory
from .repository import PostgresBomRepository
from .services import BomAggregationService, BomExplosionService, BomPipeline


DEFAULT_SOURCE = Path(__file__).parents[2] / "data" / "task_2_data_ex.csv"
LOGGER = logging.getLogger(__name__)


class Application:
    def __init__(self, config: AppConfig):
        self._config = config

    def run(self, source: Path, output: Path | None) -> None:
        with psycopg.connect(self._config.database_url) as connection:
            report = self._build_pipeline(connection).run(source)
        self._present(report, output)

    def _build_pipeline(self, connection: psycopg.Connection) -> BomPipeline:
        factory = ReaderFactory((CsvReader(), ExcelReader()))
        loader = BomLoader(factory)
        repository = PostgresBomRepository(connection, self._config.schema_path)
        aggregator = BomAggregationService(repository)
        exploder = BomExplosionService(repository)
        return BomPipeline(loader, repository, aggregator, exploder)

    @staticmethod
    def _present(report: pd.DataFrame, output: Path | None) -> None:
        if output:
            report.to_csv(output, index=False)
            LOGGER.info("Report saved to %s", output)
        LOGGER.debug("Report preview:\n%s", report.head(10).to_string(index=False))
        LOGGER.info("Generated %d report rows", len(report))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the annual BoM hierarchy")
    parser.add_argument("source", nargs="?", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")
    Application(AppConfig.from_environment()).run(args.source, args.output)


if __name__ == "__main__":
    main()
