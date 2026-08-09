# Reject Employee Reimbursement

> **Module:** ssi*hr_reimbursement\
> **Model:** `hr.reimbursement`\
> **Menu:** Human Resource > Expense > Reimbursements\
> **Actor:** user registered as an approver on the active approval template (approvers drawn
> from group \_Reimbursement — Validator*)\
> **State:** `confirm` → `reject`\
> **Requires:** `04-confirm`

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an approver on the active approval template.
- User has _Can Reject_ access right.

## Flow

1. Open the **Human Resource > Expense > Reimbursements** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
