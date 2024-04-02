import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(*args, **kwargs) -> None:
    # Define GCS URI
    bucket_name = os.getenv("GCS_BUCKET")
    object_key = kwargs.get("object_key")
    gcs_uri = f"gs://{bucket_name}/{object_key}"

    # Define BigQuery fully qualified table name (table path)
    your_project = os.getenv("GCLOUD_PROJECT")
    your_dataset = kwargs.get("dataset")
    your_table_name = kwargs.get("table_name")
    table_id = f"{your_project}.{your_dataset}.{your_table_name}"

    # Define spark variable and other necessary arguments
    spark = kwargs.get("spark")
    file_suffix = os.path.splitext(object_key)[1][1:]
    numPartitions: int | None = kwargs.get("numPartitions", 10)

    # Load data from GCS to Pyspark
    # And write the data to BigQuery
    (spark.read
     .format(file_suffix)
     .load(gcs_uri)
     .repartition(numPartitions=numPartitions)
     .write
     .format("bigquery")
     .option("table", table_id)
     .option("writeMethod", "direct")
     .mode("overwrite")
     .save())
