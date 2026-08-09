# Reset Document Number — Employee Expense Account

> **Module:** ssi_hr_expense_account\
> **Model:** `employee_expense_account`\
> **Menu:** Human Resource > Expense > Expense Accounts\
> **Actor:** user in group `Expense Account / Validator`\
> **Requires:** `01-create`

## Pre-Condition

- Record is in **Draft** status.
- User has _Can Input Manual Document Number_ access right.

## Flow

1. Open the **Human Resource > Expense > Expense Accounts** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the number field and change it to
   **/**).

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **In Progress**,
  according to the sequence template configuration.
