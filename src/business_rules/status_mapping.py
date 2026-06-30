from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from src.utils.config import STATUS_MAPPING


def map_status(df: DataFrame, source_col: str = "Source_Status", target_col: str = "Target_Status") -> DataFrame:
    """Map heterogeneous legacy status values to the target CRM status domain."""
    normalized_status = F.upper(F.trim(F.col(source_col).cast("string")))
    mapping_expr = F.create_map([F.lit(x) for pair in STATUS_MAPPING.items() for x in pair])

    return (
        df.withColumn("Normalized_Source_Status", normalized_status)
        .withColumn(target_col, mapping_expr.getItem(F.col("Normalized_Source_Status")))
        .withColumn(
            "status_mapping_rule",
            F.when(F.col(target_col).isNotNull(), F.lit("STATUS_MAPPING_V1"))
             .otherwise(F.lit(None)),
        )
    )
