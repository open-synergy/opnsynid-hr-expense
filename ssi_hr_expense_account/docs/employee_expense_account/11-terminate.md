# Terminate Employee Expense Account

> **Module:** ssi_hr_expense_account\
> **Model:** `employee_expense_account`\
> **Menu:** Human Resource > Expense > Expense Accounts\
> **Actor:** user in group `Expense Account / Validator`\
> **State:** `open` → `terminate`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Record is in a status that allows termination.
- **Access:** User has _Can Terminate_ access right.

## Flow

1. Open the **Human Resource > Expense > Expense Accounts** menu.
2. Open the record to terminate.
3. Click the **Terminate** button.
4. In the wizard that appears, select the **Termination Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Terminated**.
