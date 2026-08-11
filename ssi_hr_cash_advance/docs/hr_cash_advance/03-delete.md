# Delete Employee Cash Advance

> **Module:** ssi_hr_cash_advance\
> **Model:** `hr.cash_advance`\
> **Menu:** Human Resource > Expense > Cash Advances\
> **Actor:** user in group `User` (`hr_cash_advance_user_group`)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Record:** Document number is still **/** (not yet generated).

## Flow

1. Open the **Human Resource > Expense > Cash Advances** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
