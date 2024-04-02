import os

import pyspark.sql.functions as F

from pyspark.sql import SparkSession, DataFrame

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def anime_avg_ratings_to_bq(*args, **kwargs):
    # Define BigQuery fully qualified table name (table path)
    your_project = os.getenv("GCLOUD_PROJECT")
    your_dataset = kwargs.get("dataset")
    your_table_name = kwargs.get("table_name", "users_score_2023")
    your_table_name2 = kwargs.get("table_name2", "anime_dataset_2023")
    table_formatter = f"{your_project}.{your_dataset}.{{}}"
    
    # Define spark variable
    spark: "SparkSession" = kwargs.get("spark")

    users_score: "DataFrame" = (spark.read
                                .format("bigquery")
                                .load(table_formatter.format(your_table_name)))
    anime_dataset: "DataFrame" = (spark.read
                                  .format("bigquery")
                                  .load(table_formatter.format(your_table_name2)))

    avg_anime_rating = (users_score
        .groupBy("anime_id")
        .agg(F.mean("rating").alias("average_rating"),
             F.count("rating").alias("rating_count"))
    )

    (avg_anime_rating
     .join(anime_dataset, on="anime_id", how="inner")
     .filter(F.col("premiered") != "UNKNOWN")
     .select("anime_id", "average_rating", "rating_count", "premiered")
     .withColumn("premiered_split", F.split(F.col("premiered"), " "))
     .withColumn("season", F.col("premiered_split").getItem(0))
     .withColumn("year", F.col("premiered_split").getItem(1))
     .withColumn('category_rating', 
                 F.when(F.col("average_rating") >= 8, '>=8')
                 .when(F.col("average_rating") >= 7, '>=7')
                 .otherwise('<7'))
     .drop(*["premiered", "premiered_split"])
     .write
     .format("bigquery")
     .option("table", table_formatter.format("anime_avg_ratings"))
     .option("writeMethod", "direct")
     .mode("overwrite")
     .save()
     )
