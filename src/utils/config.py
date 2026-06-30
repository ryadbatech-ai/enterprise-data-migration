COLUMN_MAPPING = {
    "ID_migration": "External_ID",
    "Status": "Source_Status",
    "System_ID": "Legacy_System_ID",
    "National_ID": "Customer_ID",
    "Account_ID": "Legacy_System_ID",
    "CITY_NAME": "City_Name",
    "CITY_CODE": "City_Code",
    "REGION_NAME": "Region_Name",
    "REGION_CODE": "Region_Code",
}

MANDATORY_TARGET_FIELDS = [
    "External_ID",
    "Legacy_System_ID",
    "Customer_ID",
    "Target_Status",
    "Region_Code",
    "Street_1",
]

STATUS_MAPPING = {
    "ACTIVE": "Active",
    "INACTIVE": "Inactive",
    "BLOCKED": "Blocked",
    "ARCHIVED": "Archived",
}
