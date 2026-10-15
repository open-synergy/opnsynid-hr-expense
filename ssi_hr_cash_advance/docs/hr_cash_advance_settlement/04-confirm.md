# Confirm Employee Cash Advance Settlement

> **Module:** `ssi_hr_cash_advance`\
> **Model:** `hr.cash_advance_settlement`\
> **Menu:** Human Resource > Expense > Cash Advance Settlements\
> **Actor:** user in group `User` (`hr_cash_advance_settlement_user_group`)\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Data:** The settlement total, plus the totals of other settlements of the same cash
  advance that are in **Waiting for Approval** status, does not exceed the cash
  advance's **Amount Unsettled**.
- **Access:** User has _Can Confirm_ access right.

## Flow

1. Open the **Human Resource > Expense > Cash Advance Settlements** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
