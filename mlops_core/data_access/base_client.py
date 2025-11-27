from abc import ABC, abstractmethod
import pandas as pd


class BaseDBClient(ABC):
    @abstractmethod
    def fetch_df(self, query: str) -> pd.DataFrame:
        ...

    @abstractmethod
    def write_df(self, df: pd.DataFrame, table_name: str, if_exists: str = "append") -> None:
        ...
