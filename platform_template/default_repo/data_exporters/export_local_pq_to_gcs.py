from os import fspath, getenv, path
from pathlib import Path

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_local_pq_to_gcs(*args, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = "prod"

    bucket_name = getenv("GCS_BUCKET")
    object_key = kwargs.get("object_key")

    local_file_dir = kwargs.get("local_file_dir", "/home/src/data/")
    file_path: Path = Path(local_file_dir) / object_key
    file_fspath: str = fspath(file_path)
    print(f"{file_fspath=}")

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        file_fspath,
        bucket_name,
        object_key,
    )
