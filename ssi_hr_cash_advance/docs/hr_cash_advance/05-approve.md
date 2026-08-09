# Approve Employee Cash Advance

> **Module:** ssi_hr_cash_advance\
> **Model:** `hr.cash_advance`\
> **Menu:** Human Resource > Expense > Cash Advances\
> **Actor:** user registered as approver on the pending approval level, via the\
> **Standard** approval template, group `Validator` (`hr_cash_advance_validator_group`)\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an approver on the active approval template.
- User has _Can Approve_ access right.

## Flow

1. Open the **Human Resource > Expense > Cash Advances** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes to **Open** and a journal entry
  is automatically created in the configured journal.
- If there are still pending approval levels, status remains **Waiting for Approval**.
