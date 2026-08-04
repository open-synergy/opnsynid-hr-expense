# Delete Employee Business Trip Type

> **Module:** ssi_employee_business_trip\
> **Model:** `employee_business_trip_type`\
> **Menu:** Human Resource > Configuration > Expense > Business Trip Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Business Trip Type`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is not referenced by any Employee Business Trip record.
- **Access:** User is in group
  `Human Resource - Configurator / Employee Business Trip Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Business Trip Types** menu.
2. Open the record to delete.
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.
5. Click the **Business Trip Types** breadcrumb to return to the list.

## Post-Condition

- The record is permanently removed from the system.
- The list view no longer shows the deleted record.
