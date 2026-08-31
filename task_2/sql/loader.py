from pathlib import Path
from typing import Protocol

import pandas as pd

from .config import ID_COLUMNS, QUANTITY_COLUMNS, SOURCE_COLUMNS, TYPE_COLUMNS


class FileReader(Protocol):
    suffixes: tuple[str, ...]

    def read(self, path: Path, dtype: dict) -> pd.DataFrame: ...


class CsvReader:
    suffixes = (".csv",)

    def read(self, path: Path, dtype: dict) -> pd.DataFrame:
        return pd.read_csv(path, dtype=dtype)


class ExcelReader:
    suffixes = (".xlsx", ".xls")

    def read(self, path: Path, dtype: dict) -> pd.DataFrame:
        return pd.read_excel(path, dtype=dtype)


class ReaderFactory:
    def __init__(self, readers: tuple[FileReader, ...]):
        self._readers = readers

    def create(self, suffix: str) -> FileReader:
        for reader in self._readers:
            if suffix.lower() in reader.suffixes:
                return reader
        raise ValueError(f"Unsupported input format: {suffix}")


class BomLoader:
    def __init__(self, reader_factory: ReaderFactory):
        self._reader_factory = reader_factory

    def load_and_clean_bom(self, source: str | Path) -> pd.DataFrame:
        path = Path(source)
        dtype = {column: "string" for column in ID_COLUMNS}
        reader = self._reader_factory.create(path.suffix)
        frame = reader.read(path, dtype)
        self._validate(frame)
        self._clean(frame)
        return frame[SOURCE_COLUMNS]

    def _validate(self, frame: pd.DataFrame) -> None:
        missing = set(SOURCE_COLUMNS).difference(frame.columns)
        if missing:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")

    def _clean(self, frame: pd.DataFrame) -> None:
        for column in QUANTITY_COLUMNS:
            values = frame[column].astype("string").str.replace(",", "", regex=False)
            frame[column] = pd.to_numeric(values, errors="raise")
        frame[TYPE_COLUMNS] = frame[TYPE_COLUMNS].apply(pd.to_numeric).astype("Int64")
        frame[["year", "month"]] = frame[["year", "month"]].astype("Int64")
