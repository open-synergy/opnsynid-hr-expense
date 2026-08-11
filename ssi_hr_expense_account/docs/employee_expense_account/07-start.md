# Start Employee Expense Account

> **Module:** ssi_hr_expense_account\
> **Model:** `employee_expense_account`\
> **Menu:** Human Resource > Expense > Expense Accounts\
> **Actor:** — (triggered automatically, no user action)\
> **State:** `done` → `open`\
> **Requires:** `09-finish`

## Pre-Condition

- **Record:** Record is in **Done** status.
- **Data:** The **Residual** amount on the expense account returns to above **0.00**,
  for example because a linked expense transaction has been cancelled or reversed.

## Flow

This state transition happens **automatically** via system automation. No button action
is required from the user.

The system monitors the **Residual** field of each **Done** expense account. When the
**Residual** amount changes from **0.00** back to greater than **0.00** (as a result of
a linked expense transaction being cancelled or reversed), the system automatically
changes the status back to **In Progress**.

## Post-Condition

- Status returns to **In Progress**.
- The expense account can accept new expense transactions again.
