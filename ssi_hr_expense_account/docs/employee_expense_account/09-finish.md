# Finish Employee Expense Account

> **Module:** ssi_hr_expense_account\
> **Model:** `employee_expense_account`\
> **Menu:** Human Resource > Expense > Expense Accounts\
> **Actor:** — (triggered automatically, no user action)\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Record is in **In Progress** status.
- **Data:** The **Residual** amount on the expense account is **0.00**, meaning the full
  budget has been utilized by linked expense transactions.

## Flow

This state transition happens **automatically** via system automation. No button action
is required from the user.

The system monitors the **Residual** field of each **In Progress** expense account. When
the **Residual** amount changes from greater than **0.00** to exactly **0.00** (as a
result of expense transactions being processed), the system automatically changes the
status to **Done**.

## Post-Condition

- Status changes to **Done**.
- The expense account no longer accepts new expense transactions.
