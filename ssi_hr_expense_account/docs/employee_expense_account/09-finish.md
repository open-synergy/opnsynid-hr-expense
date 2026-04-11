# Finish Employee Expense Account

## Pre-Condition

- Record is in **In Progress** status.
- The **Residual** amount on the expense account is **0.00**, meaning the full budget
  has been utilized by linked expense transactions.

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
