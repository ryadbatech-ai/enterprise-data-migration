# Data Quality Framework

The data quality layer separates valid CRM-ready records from records that require correction before migration.
Each anomaly type is exported as a dedicated rejection log to make remediation easier for business and technical teams.

## Controls implemented

| Error code | Description | Typical remediation |
|---|---|---|
| `ERR_MISSING_REGION_MAPPING` | Source region has no target mapping | Complete the region mapping table |
| `ERR_MISSING_CUSTOMER_REFERENCE` | Customer ID not found in trusted registry | Correct the source ID or update registry |
| `ERR_INVALID_STATUS` | Source status cannot be mapped | Add mapping or fix source status |
| `ERR_DUPLICATE_EXTERNAL_ID` | Multiple records generate the same target external ID | Deduplicate source records or refine key logic |
| `ERR_MANDATORY_FIELDS` | Required target fields are empty | Enrich or correct source data |

## Log structure

Each rejection log keeps the original business context and adds diagnostic columns such as:

- `error_code`
- `error_message`
- `duplicate_count`
- `missing_mandatory_fields`
- source identifiers used for remediation

## Why logs are separated by anomaly type

In migration projects, business users and technical users often own different corrections.
Separating logs by error type allows each team to work on its own remediation file without filtering a large generic error table.

## Validation principles

1. **Do not silently drop records.** Invalid records must be traceable.
2. **Keep source identifiers.** Every anomaly must be linkable to the original record.
3. **Make errors actionable.** Logs include enough information to understand what must be fixed.
4. **Keep target exports clean.** Only records passing blocking checks are exported as CRM-ready data.

## Portfolio note

This framework is a simplified and anonymized version of common controls used in enterprise data migration projects.
