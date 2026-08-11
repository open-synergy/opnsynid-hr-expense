# Approve Employee Reimbursement

> **Module:** ssi*hr_reimbursement\
> **Model:** `hr.reimbursement`\
> **Menu:** Human Resource > Expense > Reimbursements\
> **Actor:** user registered as an approver on the active approval template (approvers drawn
> from group \_Reimbursement — Validator*)\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Record is in **Waiting for Approval** status.
- **Access:** User is registered as an approver on the active approval template.
- **Access:** User has _Can Approve_ access right.

## Flow

1. Open the **Human Resource > Expense > Reimbursements** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled: status changes to **In Progress** and an
  accounting journal entry is created automatically.
- If there are still pending approval levels: status remains **Waiting for Approval**.
