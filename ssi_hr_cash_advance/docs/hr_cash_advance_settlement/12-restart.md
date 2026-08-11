# Restart Employee Cash Advance Settlement

> **Module:** ssi_hr_cash_advance\
> **Model:** `hr.cash_advance_settlement`\
> **Menu:** Human Resource > Expense > Cash Advance Settlements\
> **Actor:** user in group `Validator` (`hr_cash_advance_settlement_validator_group`)\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Record is in **Cancelled** or **Rejected** status.
- **Access:** User has _Can Restart_ access right.

## Flow

1. Open the **Human Resource > Expense > Cash Advance Settlements** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog. `action_restart` carries
   `confirm="Restart data. Are you sure?"`.

## Post-Condition

- Status returns to **Draft**.
