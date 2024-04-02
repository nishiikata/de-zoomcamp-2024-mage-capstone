import hashlib
import zipfile

from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def download_dataset(*args, **kwargs):
    api = KaggleApi()
    api.authenticate()

    download_dir = Path("/home/src/data/")
    download_dir.mkdir(parents=True, exist_ok=True)
    dataset_path: str = "dbdmobile/myanimelist-dataset"
    filenames_to_hash: dict[str, str] = {
        "anime-dataset-2023.csv": "60fbcd6772f0bdad1bad1824486a6a87d0df1e69a6323f8d9eca6c8bc7218115",
        "users-details-2023.csv": "a7ea0f4922c153bbe86093ec01921b4dfa2fe7a0d58278cefb65306e71feafca",
        "users-score-2023.csv": "68d635154c0d9b8b601c2b3514933e3433c9ef2db0188b6c63155853cf85cea0",
    }

    for filename in filenames_to_hash.keys():
        file_path: Path = download_dir / filename
        if file_path.is_file() and verify_checksum(file_path, filenames_to_hash[filename]):
            print("A copy of {} already exists.".format(filename))
            continue

        api.dataset_download_file(dataset_path, filename, download_dir)

        zipped_file: Path = file_path.with_suffix(file_path.suffix + ".zip")
        try:
            with zipfile.ZipFile(zipped_file) as z:
                z.extractall(download_dir)
        except zipfile.BadZipFile as e:
            raise ValueError(
                'Bad zip file, please report on '
                'www.github.com/kaggle/kaggle-api', e)

        try:
            zipped_file.unlink()
        except FileNotFoundError:
            print(f"File {zipped_file} not found!")

        print(f"{filename} downloaded successfully!")


def verify_checksum(file_path, checksum_string, algorithm='sha256'):
    """Verify if the checksum of a file matches a given checksum string."""
    # Calculate the checksum of the file
    file_checksum = calculate_checksum(file_path, algorithm)

    # Compare the calculated checksum with the provided checksum string
    return file_checksum == checksum_string


def calculate_checksum(file_path, algorithm='sha256'):
    """Calculate the checksum of a file."""
    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        # Initialize the hashlib object with the specified algorithm
        hasher = hashlib.new(algorithm)

        # Read the file in chunks to avoid loading the entire file into memory
        while chunk := f.read(4096):
            hasher.update(chunk)

    # Return the hexadecimal digest of the checksum
    return hasher.hexdigest()
