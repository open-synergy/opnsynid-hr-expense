# Cancel Employee Reimbursement

> **Module:** ssi*hr_reimbursement\
> **Model:** `hr.reimbursement`\
> **Menu:** Human Resource > Expense > Reimbursements\
> **Actor:** user in group \_Reimbursement — Validator*\
> **State:** `draft` | `confirm` | `open` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Record is in **Draft**, **Waiting for Approval**, or **In Progress**
  status.
- **Access:** User has _Can Cancel_ access right.

## Flow

1. Open the **Human Resource > Expense > Reimbursements** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- If the record was in **In Progress** status, the accounting journal entry is deleted
  automatically.
