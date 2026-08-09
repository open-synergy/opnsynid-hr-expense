# Confirm Employee Reimbursement

> **Module:** ssi_hr_reimbursement
> **Model:** `hr.reimbursement`
> **Menu:** Human Resource > Expense > Reimbursements
> **Actor:** user in group *Reimbursement — User*
> **State:** `draft` → `confirm`
> **Requires:** `01-create`

## Pre-Condition

- Record is in **Draft** status.
- User has _Can Confirm_ access right.

## Flow

1. Open the **Human Resource > Expense > Reimbursements** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
