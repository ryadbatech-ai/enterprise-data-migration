# Business Rules

This project uses anonymized business rules inspired by enterprise ERP/CRM migration projects.
The objective is to transform heterogeneous legacy source records into a stable CRM-ready model.

## Rule categories

### 1. Column normalization
Legacy files often contain inconsistent naming conventions, accents, extra spaces or non-breaking spaces.
The pipeline normalizes column names before applying any business rule.

Example:

| Source column | Target column |
|---|---|
| `ID_migration` | `External_ID` |
| `System_ID` | `Legacy_System_ID` |
| `National_ID` | `Customer_ID` |
| `CITY_CODE` | `City_Code` |

### 2. Identifier cleaning
Customer identifiers are cleaned before reference matching.
Only numeric characters are kept in `Clean_Customer_ID` to avoid mismatches caused by spaces, punctuation or formatting.

### 3. Status mapping
Legacy statuses are mapped to a controlled CRM domain.

| Legacy status | Target CRM status |
|---|---|
| `A` | `ACTIVE` |
| `ACTIVE` | `ACTIVE` |
| `I` | `INACTIVE` |
| `INACTIVE` | `INACTIVE` |

Invalid or unknown statuses are rejected into `ERR_INVALID_STATUS`.

### 4. Address formatting
Long street values are split into `Street_1`, `Street_2` and `Street_3` using target field length constraints.
The split preserves words whenever possible to avoid cutting address components in the middle.

### 5. Target external ID generation
The CRM upsert key is generated from business dimensions:

```text
CRM_<Region_Code>_<External_ID>
```

This makes IDs stable across re-runs and prevents random technical identifiers from being used as target keys.

### 6. Reference mapping
Source regions are validated against a mapping table before export.
Customer IDs are also checked against a trusted reference registry.
Records missing these references are sent to rejection logs.

## Design note

The rules are intentionally anonymized. Names, objects and mappings do not correspond to any real customer system.
