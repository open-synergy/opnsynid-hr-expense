# Restart Employee Reimbursement

> **Module:** ssi*hr_reimbursement\
> **Model:** `hr.reimbursement`\
> **Menu:** Human Resource > Expense > Reimbursements\
> **Actor:** user in group \_Reimbursement — Validator*\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Record is in **Cancelled** or **Rejected** status.
- **Access:** User has _Can Restart_ access right.

## Flow

1. Open the **Human Resource > Expense > Reimbursements** menu.
2. Open the record to restart.
3. Click the **Restart** button.

## Post-Condition

- Status returns to **Draft**.
