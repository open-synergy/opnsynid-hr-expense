# Delete Employee Expense Account

> **Module:** ssi_hr_expense_account\
> **Model:** `employee_expense_account`\
> **Menu:** Human Resource > Expense > Expense Accounts\
> **Actor:** user in group `Expense Account / User`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Record:** Document number is still **/** (not yet generated).

## Flow

1. Open the **Human Resource > Expense > Expense Accounts** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
