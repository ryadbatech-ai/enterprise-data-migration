def read_sql_reference(spark, jdbc_url: str, table_name: str, partition_column: str, properties: dict):
    return spark.read.jdbc(
        url=jdbc_url,
        table=table_name,
        column=partition_column,
        lowerBound=1,
        upperBound=1_000_000,
        numPartitions=8,
        properties=properties,
    )
