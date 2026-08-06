# Activate Employee Expense Account Type

> **Module:** ssi_hr_expense_account\
> **Model:** `employee_expense_account_type`\
> **Menu:** Human Resource > Configuration > Expense > Expense Account Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Expense Account
> Type`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group
  `Human Resource - Configurator / Employee Expense Account Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Expense Account Types** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The types can be selected again as **Type** on new Employee Expense Account records.
