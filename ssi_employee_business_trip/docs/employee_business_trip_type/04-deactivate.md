# Deactivate Employee Business Trip Type

> **Module:** ssi_employee_business_trip\
> **Model:** `employee_business_trip_type`\
> **Menu:** Human Resource > Configuration > Expense > Business Trip Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Business Trip Type`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group
  `Human Resource - Configurator / Employee Business Trip Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Business Trip Types** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated types cannot be selected as **Type** on new Employee Business Trip
  records.
- Employee Business Trip records that already use a deactivated type can still be
  viewed.
