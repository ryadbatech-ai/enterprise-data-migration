import argparse
from datetime import datetime
from pathlib import Path

from pyspark.sql import functions as F
from zoneinfo import ZoneInfo

from src.ingestion.local_reader import read_csv
from src.utils.spark import get_spark
from src.transformations.normalization import normalize_column_names, clean_customer_id
from src.transformations.address import apply_address_formatting
from src.business_rules.status_mapping import map_status
from src.business_rules.target_mapping import apply_target_mapping, select_target_columns
from src.validation.reference_integrity import (
    get_missing_region_mapping,
    get_missing_customer_reference,
    get_invalid_status,
)
from src.validation.duplicates import get_duplicate_external_ids
from src.validation.mandatory_fields import get_missing_mandatory_records
from src.exports.writers import write_local_csv


def run_local_pipeline():
    spark = get_spark("local-enterprise-data-migration")
    base = Path(__file__).resolve().parents[1] / "sample_data"
    output = Path(__file__).resolve().parents[1] / "outputs"
    output.mkdir(exist_ok=True)

    source = spark.createDataFrame(read_csv(base / "source_records.csv"))
    crm = spark.createDataFrame(read_csv(base / "crm_accounts.csv"))
    city = spark.createDataFrame(read_csv(base / "city_mapping.csv"))
    registry = spark.createDataFrame(read_csv(base / "customer_registry.csv"))

    source = clean_customer_id(normalize_column_names(source))
    crm = normalize_column_names(crm)
    city = normalize_column_names(city)
    registry = normalize_column_names(registry)

    # Keep a single business Region_Code in the pipeline.
    # The city reference also contains a Region_Code column, so it is renamed
    # before the join to avoid AMBIGUOUS_REFERENCE errors downstream.
    city_lookup = city.select(
        F.col("Region_Code").alias("City_Region_Code"),
        F.col("Region_Name"),
        F.col("City_Code"),
        F.col("City_Name"),
    )

    processed = (
        source.alias("src")
        .join(crm.alias("crm"), "Legacy_System_ID", "left")
        .join(
            city_lookup.alias("city"),
            F.col("src.Region_Code") == F.col("city.City_Region_Code"),
            "left",
        )
        .join(
            registry.alias("ref"),
            F.col("src.Clean_Customer_ID") == F.col("ref.registry_id"),
            "left",
        )
        .drop("City_Region_Code")
    )

    processed = apply_address_formatting(processed, "BillingStreet")
    processed = map_status(processed)
    processed = apply_target_mapping(processed)

    logs = {
        "ERR_MISSING_REGION_MAPPING": get_missing_region_mapping(processed),
        "ERR_MISSING_CUSTOMER_REFERENCE": get_missing_customer_reference(processed),
        "ERR_INVALID_STATUS": get_invalid_status(processed),
    }

    target = select_target_columns(processed)
    logs["ERR_DUPLICATE_EXTERNAL_ID"] = get_duplicate_external_ids(target)
    logs["ERR_MANDATORY_FIELDS"] = get_missing_mandatory_records(target)

    valid_records = (
        target
        .filter("City_Code is not null")
        .filter("Target_Status is not null")
        .filter("Clean_Customer_ID is not null")
    )

    timestamp = datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y%m%d_%H%M")
    write_local_csv(valid_records, output / f"crm_ready_records_{timestamp}.csv")

    for name, df_log in logs.items():
        write_local_csv(df_log, output / f"{name}_{timestamp}.csv")

    print(f"Pipeline completed. Outputs written to {output}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", action="store_true", help="Run with anonymized local sample data")
    args = parser.parse_args()

    if args.local:
        run_local_pipeline()
    else:
        parser.error("No execution mode selected. Use --local to run the anonymized portfolio demo. For Databricks/Azure deployment, open notebooks/databricks_demo.ipynb and adapt secrets, storage paths and JDBC settings to your environment.")


if __name__ == "__main__":
    main()
