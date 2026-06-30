from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def get_missing_region_mapping(df: DataFrame) -> DataFrame:
    """Records where the source region could not be mapped to a target city/region code."""
    return (
        df.filter(F.col("City_Code").isNull())
        .withColumn("error_code", F.lit("ERR_MISSING_REGION_MAPPING"))
        .withColumn(
            "error_message",
            F.concat(F.lit("No region mapping found for Region_Code="), F.coalesce(F.col("Region_Code"), F.lit("<null>"))),
        )
    )


def get_missing_customer_reference(df: DataFrame) -> DataFrame:
    """Records not found in the trusted customer registry."""
    return (
        df.filter(F.col("registry_id").isNull())
        .withColumn("error_code", F.lit("ERR_MISSING_CUSTOMER_REFERENCE"))
        .withColumn(
            "error_message",
            F.concat(F.lit("Customer reference not found for Clean_Customer_ID="), F.coalesce(F.col("Clean_Customer_ID"), F.lit("<null>"))),
        )
    )


def get_invalid_status(df: DataFrame) -> DataFrame:
    """Records where source status cannot be translated to the target CRM status list."""
    return (
        df.filter(F.col("Target_Status").isNull())
        .withColumn("error_code", F.lit("ERR_INVALID_STATUS"))
        .withColumn(
            "error_message",
            F.concat(F.lit("Invalid or unmapped Source_Status="), F.coalesce(F.col("Source_Status"), F.lit("<null>"))),
        )
    )
