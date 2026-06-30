from pyspark.sql import DataFrame
from pyspark.sql import functions as F

TARGET_COLUMNS = [
    "Target_External_ID",
    "External_ID",
    "Legacy_System_ID",
    "Customer_ID",
    "Clean_Customer_ID",
    "Target_Status",
    "Region_Code",
    "City_Code",
    "Street_1",
    "Street_2",
    "Street_3",
]


def build_target_external_id(df: DataFrame) -> DataFrame:
    """Build stable target IDs used for CRM upsert operations."""
    return df.withColumn(
        "Target_External_ID",
        F.concat_ws("_", F.lit("CRM"), F.upper(F.trim(F.col("Region_Code"))), F.col("External_ID")),
    )


def apply_target_mapping(df: DataFrame) -> DataFrame:
    """Apply target-oriented formatting rules before export."""
    return (
        build_target_external_id(df)
        .withColumn("Region_Code", F.upper(F.trim(F.col("Region_Code"))))
        .withColumn("City_Code", F.upper(F.trim(F.col("City_Code"))))
    )


def select_target_columns(df: DataFrame) -> DataFrame:
    """Select final CRM-ready columns in deterministic order."""
    available = [c for c in TARGET_COLUMNS if c in df.columns]
    return df.select(*available)
