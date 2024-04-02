import os

import pyspark.sql.functions as F

from pyspark.sql import SparkSession, DataFrame

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def anime_categories_to_bq(*args, **kwargs):
    # Define BigQuery fully qualified table name (table path)
    your_project = os.getenv("GCLOUD_PROJECT")
    your_dataset = kwargs.get("dataset")
    your_table_name = kwargs.get("table_name")
    table_formatter = f"{your_project}.{your_dataset}.{{}}"
    table_id = table_formatter.format(your_table_name)

    # Define spark variable
    spark: "SparkSession" = kwargs.get("spark")

    df: "DataFrame" = (spark.read
                       .format("bigquery")
                       .load(table_id))

    # Explode category and groupby
    for category in ["genres", "licensors", "producers"]:
        category_singular = category[:-1]

        (df.select("anime_id", category)
        .withColumnRenamed(category, "n")
        .withColumn("n", F.split(F.col("n"), ","))
        .withColumn("n", F.explode_outer(F.col("n")))
        .withColumn("n", F.trim(F.col("n")))
        .withColumnRenamed("n", category_singular)
        .groupBy(category_singular)
        .count()
        .orderBy("count", ascending=False)
        .write
        .format("bigquery")
        .option("table", table_formatter.format(f"{category_singular}_count"))
        .option("writeMethod", "direct")
        .mode("overwrite")
        .save()
        )
