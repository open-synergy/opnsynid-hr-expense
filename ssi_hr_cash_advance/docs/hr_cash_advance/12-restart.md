# Restart Employee Cash Advance

> **Module:** ssi_hr_cash_advance\
> **Model:** `hr.cash_advance`\
> **Menu:** Human Resource > Expense > Cash Advances\
> **Actor:** user in group `Validator` (`hr_cash_advance_validator_group`)\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- Record is in **Cancelled** or **Rejected** status.
- User has _Can Restart_ access right.

## Flow

1. Open the **Human Resource > Expense > Cash Advances** menu.
2. Open the record to restart.
3. Click the **Restart** button.

## Post-Condition

- Status returns to **Draft**.
