# Restart Employee Expense Account

> **Module:** ssi_hr_expense_account\
> **Model:** `employee_expense_account`\
> **Menu:** Human Resource > Expense > Expense Accounts\
> **Actor:** user in group `Expense Account / Validator`\
> **State:** `cancel`/`reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Record is in **Cancelled**, **Rejected**, or **Terminated** status.
- **Access:** User has _Can Restart_ access right.

## Flow

1. Open the **Human Resource > Expense > Expense Accounts** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog. `action_restart` carries
   `confirm="Restart data. Are you sure?"`.

## Post-Condition

- Status returns to **Draft**.
