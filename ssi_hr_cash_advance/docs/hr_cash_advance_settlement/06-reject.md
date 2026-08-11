# Reject Employee Cash Advance Settlement

> **Module:** ssi_hr_cash_advance\
> **Model:** `hr.cash_advance_settlement`\
> **Menu:** Human Resource > Expense > Cash Advance Settlements\
> **Actor:** user registered as approver on the pending approval level, via the\
> **Standard** approval template, group `Validator`\
> (`hr_cash_advance_settlement_validator_group`)\
> **State:** `confirm` → `reject`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Record is in **Waiting for Approval** status.
- **Access:** User is registered as an approver on the active approval template.
- **Access:** User has _Can Reject_ access right.

## Flow

1. Open the **Human Resource > Expense > Cash Advance Settlements** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
