# Delete Employee Expense Account Type

> **Module:** ssi_hr_expense_account\
> **Model:** `employee_expense_account_type`\
> **Menu:** Human Resource > Configuration > Expense > Expense Account Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Expense Account Type`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is not referenced by any Employee Expense Account record.
- **Access:** User is in group
  `Human Resource - Configurator / Employee Expense Account Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Expense Account Types** menu.
2. Open the record to delete.
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.
5. Click the **Expense Account Types** breadcrumb to return to the list.

## Post-Condition

- The record is permanently removed from the system.
- The list view no longer shows the deleted record.
