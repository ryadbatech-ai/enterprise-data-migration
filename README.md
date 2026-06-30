# Enterprise Data Migration Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PySpark](https://img.shields.io/badge/PySpark-3.x-orange)
![Databricks](https://img.shields.io/badge/Databricks-ready-red)
![Delta Lake](https://img.shields.io/badge/Delta%20Lake-supported-brightgreen)
![Tests](https://img.shields.io/badge/tests-pytest-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

Enterprise-grade ETL pipeline built with **PySpark**, **Databricks**, **Azure Blob Storage** and **Delta Lake** to prepare anonymized legacy ERP/CRM data for a Salesforce-ready target model.

This repository is a portfolio project inspired by real enterprise migration constraints: heterogeneous Excel inputs, SQL reference tables, business-rule mapping, anomaly files, mandatory field checks, duplicate detection, address formatting and final export into a clean target dataset.

> All business names, source systems, field names, values and mappings are anonymized.

---

## Features

- Distributed ingestion from Excel, CSV and SQL/JDBC sources
- Column normalization and schema alignment
- Configurable business rules engine
- Salesforce-ready target mapping
- Address splitting and target field formatting
- Reference integrity checks
- Duplicate external ID detection with diagnostic columns
- Mandatory field validation with missing-field details
- Rejection logs by anomaly type
- Delta Lake export partitioned by region
- Unit-testable Python modules
- GitHub Actions CI for automated tests

---

## Architecture

```mermaid
flowchart LR
    A[Legacy Excel files] --> D[Ingestion Layer]
    B[SQL Reference Tables] --> D
    C[Azure Blob Staging] --> D

    D --> E[Column Normalization]
    E --> F[Business Rules Engine]
    F --> G[Data Quality Framework]

    G --> H[CRM-ready Delta Output]
    G --> I[Rejection Logs by Error Type]

    H --> J[Target CRM / Salesforce-ready Model]
    I --> K[Business Remediation]
```

See [`architecture/migration_flow.md`](architecture/migration_flow.md) for the full flow.

---

## Repository structure

```text
enterprise-data-migration/
├── .github/workflows/
│   └── tests.yml
├── architecture/
├── docs/
├── notebooks/
├── sample_data/
├── src/
│   ├── ingestion/
│   ├── transformations/
│   ├── business_rules/
│   ├── validation/
│   ├── exports/
│   └── utils/
└── tests/
```

---

## Technologies

- Python
- PySpark
- Databricks
- Delta Lake
- Azure Blob Storage
- SQL Server JDBC
- Pandas
- Pytest
- GitHub Actions

---

## Example data quality logs

| Log name | Purpose |
|---|---|
| `ERR_MISSING_REGION_MAPPING` | Region code not found in reference mapping |
| `ERR_MISSING_CUSTOMER_REFERENCE` | Customer ID not present in registry |
| `ERR_DUPLICATE_EXTERNAL_ID` | Duplicate target external IDs |
| `ERR_MANDATORY_FIELDS` | Missing mandatory target fields |
| `ERR_INVALID_STATUS` | Source status cannot be mapped to target status |

---

## Example business rule

```python
from src.business_rules.status_mapping import map_status
from src.business_rules.target_mapping import apply_target_mapping

processed = (
    source_df
    .transform(map_status)
    .transform(apply_target_mapping)
)
```

The target external ID is generated with a deterministic upsert key:

```text
CRM_<Region_Code>_<External_ID>
```

---

## Quick start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest tests/ -q
```

Run the local sample pipeline:

```bash
python -m src.main --local
```

The local run writes CRM-ready records and data-quality logs into the `outputs/` folder.

In Databricks, use [`notebooks/databricks_demo.ipynb`](notebooks/databricks_demo.ipynb) as a deployment template and adapt storage paths, secrets and JDBC settings.

---

## Documentation

- [`docs/business_rules.md`](docs/business_rules.md)
- [`docs/data_quality.md`](docs/data_quality.md)
- [`architecture/migration_flow.md`](architecture/migration_flow.md)

---

## Portfolio note

This project demonstrates a production-style data migration workflow: ingestion, mapping, data quality, anomaly generation and target export. It is not connected to any real customer environment and uses anonymized sample data only.
