# Cancel Employee Cash Advance Settlement

> **Module:** `ssi_hr_cash_advance`\
> **Model:** `hr.cash_advance_settlement`\
> **Menu:** Human Resource > Expense > Cash Advance Settlements\
> **Actor:** user in group `Validator` (`hr_cash_advance_settlement_validator_group`)\
> **State:** `draft` | `confirm` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Record is in a status that allows cancellation (**Draft**, **Waiting for
  Approval**, or **Done**).
- **Access:** User has _Can Cancel_ access right.

## Flow

1. Open the **Human Resource > Expense > Cash Advance Settlements** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- If the record was in **Done** status, the associated journal entry is automatically
  deleted and the reconciliation of every credit line with the cash advance move lines
  is reversed.
- Any other **Done** settlement of the same cash advance whose journal entry has a
  credit line that is not fully reconciled is automatically reconciled again, oldest
  first, with the open residual of the cash advance line that has the same analytic
  account. The cash advance's unsettled amount and status follow the new reconciliation.
  Without such a settlement, the residual of the cash advance simply stays open.
