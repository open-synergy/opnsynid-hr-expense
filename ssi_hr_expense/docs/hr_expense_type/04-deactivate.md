# Deactivate Expense Type

> **Module:** ssi_hr_expense\
> **Model:** `hr.expense_type`\
> **Menu:** Human Resource > Configuration > Expense > Types\
> **Actor:** user in group `Expense Type`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group `Expense Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Types** menu.
2. Open the Expense Type record to deactivate.
3. Click the **Edit** button.
4. Toggle the **Active** field off.
5. Click **Save**.

## Post-Condition

- The record is archived; an **Archived** ribbon appears on the form.
- The record no longer appears in the default list view.
- Deactivated Expense Types cannot be selected on new transactions. Transactions that
  already use this Expense Type can still be viewed.
