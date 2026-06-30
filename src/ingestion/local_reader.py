from pathlib import Path
import pandas as pd


def read_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str).fillna("")
