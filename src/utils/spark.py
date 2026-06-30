from pyspark.sql import SparkSession


def get_spark(app_name: str = "enterprise-data-migration") -> SparkSession:
    return (
        SparkSession.builder
        .appName(app_name)
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic")
        .getOrCreate()
    )
