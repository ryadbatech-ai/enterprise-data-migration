from pathlib import Path


def write_delta(df, path: str, partition_by: str | None = None, mode: str = "overwrite"):
    writer = df.write.format("delta").mode(mode)
    if partition_by:
        writer = writer.partitionBy(partition_by)
    writer.save(path)


def write_json_logs(logs: dict, base_path: str):
    for log_name, df_log in logs.items():
        df_log.write.format("json").mode("overwrite").save(f"{base_path}/{log_name}")


def write_local_csv(df, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.toPandas().to_csv(path, index=False)
    
def write_delta_table(df, output_path: str, partition_by: str = "Region_Code") -> None:
    """
    Write a Spark DataFrame to Delta Lake.
    Intended for Databricks / Spark environments.
    """
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .partitionBy(partition_by)
        .save(output_path)
    )