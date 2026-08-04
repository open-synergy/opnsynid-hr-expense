# Delete Expense Type

> **Module:** ssi_hr_expense\
> **Model:** `hr.expense_type`\
> **Menu:** Human Resource > Configuration > Expense > Types\
> **Actor:** user in group `Expense Type`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Expense Type is not referenced by any cash advance, reimbursement, or
  other transaction.
- **Access:** User is in group `Expense Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Types** menu.
2. Open the Expense Type record to delete.
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The record is permanently removed from the system.
- The list view no longer shows the deleted record.
