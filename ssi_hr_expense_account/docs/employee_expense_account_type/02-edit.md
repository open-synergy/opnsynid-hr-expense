# Edit Employee Expense Account Type

> **Module:** ssi_hr_expense_account\
> **Model:** `employee_expense_account_type`\
> **Menu:** Human Resource > Configuration > Expense > Expense Account Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Expense Account
> Type`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_generate_code` (Generate Code), `action_reset_code` (Reset
> code)

## Pre-Condition

- **Access:** User is in group
  `Human Resource - Configurator / Employee Expense Account Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Expense Account Types** menu.
2. Find and open the record to edit.
3. Click the **Edit** button. **(14.0 only — the form opens directly editable on
   16.0+)**
4. Change **Name** or **Accounts** as needed.
5. If **Code** needs to be reassigned, first select the record in the **Expense Account
   Types** list and click **Reset code** in the list toolbar, then click **OK** to
   confirm — this clears **Code** back to **/**. Reopen the record, click **Edit**, then
   click the **Generate Code** button in the header to assign a new code from the
   configured `sequence.template`. Both steps are optional; skip them to keep the
   current code unchanged.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.
