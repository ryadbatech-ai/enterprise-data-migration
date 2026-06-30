# Migration Flow

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

## Processing stages

1. **Ingestion**: load Excel, CSV or SQL/JDBC datasets.
2. **Standardization**: normalize column names and clean identifiers.
3. **Business rules**: map statuses, build target IDs and format addresses.
4. **Data quality**: isolate missing mappings, invalid statuses, missing references and duplicate keys.
5. **Export**: write CRM-ready records and anomaly logs.
```
