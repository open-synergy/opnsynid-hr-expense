# Cancel Employee Expense Account

> **Module:** ssi_hr_expense_account\
> **Model:** `employee_expense_account`\
> **Menu:** Human Resource > Expense > Expense Accounts\
> **Actor:** user in group `Expense Account / Validator`\
> **State:** `draft`/`confirm`/`open` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- Record is in a status that allows cancellation (usually **Draft**, **Waiting for
  Approval**, or **In Progress**).
- User has _Can Cancel_ access right.

## Flow

1. Open the **Human Resource > Expense > Expense Accounts** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
