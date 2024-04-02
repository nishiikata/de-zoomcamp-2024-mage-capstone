from pathlib import Path

if 'sensor' not in globals():
    from mage_ai.data_preparation.decorators import sensor


@sensor
def local_file_exists(*args, **kwargs) -> bool:
    local_file_dir = kwargs.get("local_file_dir", "/home/src/data/")
    local_file = kwargs.get("object_key")
    file_path: Path = Path(local_file_dir) / local_file

    return file_path.is_file()
