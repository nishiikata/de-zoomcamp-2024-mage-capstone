import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from pathlib import Path

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def users_score_to_pq_local(*args, **kwargs):
    csv_path = Path("/home/src/data/users-score-2023.csv")
    parquet_name = kwargs.get("object_key", "users-score-2023.parquet") 
    parquet_path: Path = csv_path.parent / parquet_name

    # Open CSV file using pandas chunksize parameter
    chunksize = 131_072  # Adjust the chunk size according to your system's memory constraints
    csv_reader = pd.read_csv(
        csv_path,
        header=0,
        names=[
            "user_id",
            "username",
            "anime_id",
            "anime_title",
            "rating",
        ],
        chunksize=chunksize,
    )

    # Create an Arrow schema from the CSV file's first chunk
    first_chunk = next(csv_reader)
    arrow_schema = pa.Schema.from_pandas(first_chunk)

    # Write Parquet file in chunks
    with pq.ParquetWriter(
        parquet_path,
        arrow_schema,
        compression="zstd",
    ) as writer:
        table = pa.Table.from_pandas(first_chunk, schema=arrow_schema) 
        writer.write_table(table)

        # Iterate over the remaining chunks and append to the Parquet file
        for chunk in csv_reader:
            table = pa.Table.from_pandas(chunk, schema=arrow_schema)
            writer.write_table(table)
