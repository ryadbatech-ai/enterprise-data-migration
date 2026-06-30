from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def get_duplicate_external_ids(df: DataFrame, key: str = "Target_External_ID") -> DataFrame:
    """Return all records involved in a duplicate target identifier.

    Unlike a simple groupBy count, this keeps the original rows and enriches them
    with diagnostic columns that are directly usable in rejection logs.
    """
    duplicate_keys = (
        df.groupBy(key)
        .agg(
            F.count("*").alias("duplicate_count"),
            F.collect_set("External_ID").alias("source_external_ids"),
        )
        .filter(F.col("duplicate_count") > 1)
    )

    return (
        df.join(duplicate_keys, key, "inner")
        .withColumn("error_code", F.lit("ERR_DUPLICATE_EXTERNAL_ID"))
        .withColumn(
            "error_message",
            F.concat(F.lit("Duplicate target external ID: "), F.col(key)),
        )
    )


def add_duplicate_flag(df: DataFrame, key: str = "Target_External_ID") -> DataFrame:
    """Flag duplicates while preserving all records."""
    w = Window.partitionBy(key)
    return df.withColumn("is_duplicate_external_id", F.count("*").over(w) > 1)
