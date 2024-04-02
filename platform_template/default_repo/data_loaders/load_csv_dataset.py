import pandas as pd

from pathlib import Path

from pandas import DataFrame

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_csv_dataset(*args, **kwargs) -> DataFrame:
    csv_path: str = kwargs.get("csv_path")
    return pd.read_csv(csv_path)


@test
def test_output(df: DataFrame, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
