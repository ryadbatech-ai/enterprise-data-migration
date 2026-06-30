from functools import reduce
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from src.utils.config import MANDATORY_TARGET_FIELDS


def _missing_condition(column_name: str):
    return F.col(column_name).isNull() | (F.trim(F.col(column_name).cast("string")) == "")


def add_missing_fields_column(df: DataFrame, fields: list[str] | None = None) -> DataFrame:
    """Add a list of missing mandatory fields for each record."""
    fields = fields or MANDATORY_TARGET_FIELDS

    missing_array = F.array(*[
        F.when(_missing_condition(field), F.lit(field)).otherwise(F.lit(None))
        for field in fields
    ])

    return df.withColumn(
        "missing_mandatory_fields",
        F.expr("filter(missing_mandatory_fields_raw, x -> x is not null)")
    ) if False else df.withColumn("missing_mandatory_fields_raw", missing_array).withColumn(
        "missing_mandatory_fields",
        F.expr("filter(missing_mandatory_fields_raw, x -> x is not null)")
    ).drop("missing_mandatory_fields_raw")


def get_missing_mandatory_records(df: DataFrame, fields: list[str] | None = None) -> DataFrame:
    """Return records failing mandatory field validation with diagnostic details."""
    fields = fields or MANDATORY_TARGET_FIELDS
    conditions = [_missing_condition(field) for field in fields]

    if not conditions:
        return df.limit(0)

    return (
        add_missing_fields_column(df, fields)
        .filter(reduce(lambda a, b: a | b, conditions))
        .withColumn("error_code", F.lit("ERR_MANDATORY_FIELDS"))
        .withColumn(
            "error_message",
            F.concat(F.lit("Missing mandatory fields: "), F.concat_ws(", ", F.col("missing_mandatory_fields"))),
        )
    )
