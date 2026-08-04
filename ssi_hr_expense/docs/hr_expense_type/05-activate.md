# Activate Expense Type

> **Module:** ssi_hr_expense\
> **Model:** `hr.expense_type`\
> **Menu:** Human Resource > Configuration > Expense > Types\
> **Actor:** user in group `Expense Type`\
> **Active:** `false` → `true`\
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group `Expense Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Types** menu.
2. Enable the **Archived** filter in the search bar.
3. Open the archived Expense Type record to reactivate.
4. Click the **Edit** button.
5. Toggle the **Active** field on.
6. Click **Save**.

## Post-Condition

- The record is restored and appears again in the default list view.
- The **Archived** ribbon no longer appears on the form.
- The Expense Type can be selected again on new transactions.
