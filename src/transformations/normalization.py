from pyspark.sql import functions as F
from src.utils.config import COLUMN_MAPPING


def normalize_column_names(df):
    for old_col in df.columns:
        clean_col = old_col.replace("\xa0", " ").strip()
        new_col = COLUMN_MAPPING.get(clean_col, clean_col)
        if old_col != new_col:
            df = df.withColumnRenamed(old_col, new_col)
    return df


def clean_customer_id(df):
    return df.withColumn(
        "Clean_Customer_ID",
        F.regexp_replace(F.col("Customer_ID").cast("string"), "[^0-9]", "")
    )


def normalize_text_column(df, column_name: str):
    return df.withColumn(column_name, F.upper(F.trim(F.col(column_name))))
