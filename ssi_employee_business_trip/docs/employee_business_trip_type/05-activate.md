# Activate Employee Business Trip Type

> **Module:** ssi_employee_business_trip\
> **Model:** `employee_business_trip_type`\
> **Menu:** Human Resource > Configuration > Expense > Business Trip Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Business Trip Type`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group
  `Human Resource - Configurator / Employee Business Trip Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Business Trip Types** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The types can be selected again as **Type** on new Employee Business Trip records.
