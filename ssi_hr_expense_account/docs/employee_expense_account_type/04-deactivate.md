# Deactivate Employee Expense Account Type

> **Module:** ssi_hr_expense_account\
> **Model:** `employee_expense_account_type`\
> **Menu:** Human Resource > Configuration > Expense > Expense Account Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Expense Account
> Type`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group
  `Human Resource - Configurator / Employee Expense Account Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Expense Account Types** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated types cannot be selected as **Type** on new Employee Expense Account
  records.
- Employee Expense Account records that already use a deactivated type can still be
  viewed.
