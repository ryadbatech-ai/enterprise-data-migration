def split_address(text: str, limits: list[int] | None = None) -> tuple[str, str, str]:
    """Split a long address into three target-safe address lines.

    The function is pure Python so it can be unit-tested without a Spark session.
    Spark-specific imports are kept inside apply_address_formatting.
    """
    limits = limits or [60, 40, 40]
    if not text or not text.strip():
        return "", "", ""

    output = ["", "", ""]
    words = text.strip().split()
    index = 0
    buffer = ""

    for word in words:
        candidate = word if not buffer else f"{buffer} {word}"
        if len(candidate) <= limits[index]:
            buffer = candidate
        else:
            output[index] = buffer
            index += 1
            if index >= len(output):
                break
            buffer = word

    if index < len(output) and buffer:
        output[index] = buffer

    return tuple(output)


def apply_address_formatting(df, source_column: str = "BillingStreet"):
    from pyspark.sql import functions as F, types as T

    address_schema = T.StructType([
        T.StructField("Street_1", T.StringType(), True),
        T.StructField("Street_2", T.StringType(), True),
        T.StructField("Street_3", T.StringType(), True),
    ])
    split_address_udf = F.udf(lambda value: split_address(value), address_schema)

    return (
        df.withColumn("Address", split_address_udf(F.col(source_column)))
        .withColumn("Street_1", F.col("Address.Street_1"))
        .withColumn("Street_2", F.col("Address.Street_2"))
        .withColumn("Street_3", F.col("Address.Street_3"))
        .drop("Address")
    )
