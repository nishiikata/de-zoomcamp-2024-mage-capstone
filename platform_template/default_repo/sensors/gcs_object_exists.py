from os import getenv, path

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage

if 'sensor' not in globals():
    from mage_ai.data_preparation.decorators import sensor


@sensor
def gcs_object_exists(*args, **kwargs) -> bool:
    """
    Template code for checking if a file or folder exists in a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = "prod"

    bucket_name = getenv("GCS_BUCKET")
    object_key = kwargs.get("object_key")

    return GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).exists(
        bucket_name,
        object_key,
    )
