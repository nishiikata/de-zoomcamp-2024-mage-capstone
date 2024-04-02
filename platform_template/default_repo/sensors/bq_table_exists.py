from os import getenv, path

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader

if 'sensor' not in globals():
    from mage_ai.data_preparation.decorators import sensor


@sensor
def bq_table_exists(*args, **kwargs) -> bool:
    """
    Template code for checking the results of a BigQuery query.
    Specify your configuration settings in 'io_config.yaml'.

    Return: True if the sensor should complete, False if it should
    keep waiting
    """

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = "prod"

    your_project = getenv("GCLOUD_PROJECT")
    your_dataset = kwargs.get("dataset")
    your_table = kwargs.get("table_name")

    query = f"""
    SELECT table_id
    FROM `{your_project}.{your_dataset}.__TABLES_SUMMARY__`
    WHERE table_id = '{your_table}'
    """

    loader = BigQuery.with_config(ConfigFileLoader(config_path, config_profile))
    df = loader.load(query)

    return not df.empty
