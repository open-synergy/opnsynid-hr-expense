# Create Employee Expense Account Type

> **Module:** ssi_hr_expense_account\
> **Model:** `employee_expense_account_type`\
> **Menu:** Human Resource > Configuration > Expense > Expense Account Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Expense Account Type`\
> **Inline Actions:** `action_generate_code` (Generate Code), `action_reset_code` (Reset
> code)

## Pre-Condition

- **Config:** A `sequence.template` for this model must be configured before using the
  **Generate Code** button (see step 4). Not required when **Code** is entered manually.
- **Access:** User is in group
  `Human Resource - Configurator / Employee Expense Account Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Expense Account Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the expense account type name.
   - **Code** _(required)_: Enter a unique code for this type, or fill with **/** and
     use the **Generate Code** button later (see step 4) to assign one automatically.
   - **Accounts**: Select the accounting accounts allowed for expense accounts of this
     type. Optional — leave empty if no restriction is needed yet.
4. If **Code** was left as **/**, click the **Generate Code** button in the header to
   automatically assign a code from the configured `sequence.template`. Skip this step
   if an explicit code was entered manually — **Generate Code** only changes records
   whose **Code** is still **/**. To undo a previously generated code later, select the
   record in the **Expense Account Types** list, click **Reset code** in the list
   toolbar, then click **OK** to confirm — this clears **Code** back to **/** so it can
   be regenerated.
5. Click **Save**.

## Post-Condition

- A new Employee Expense Account Type record is created and available for selection as
  **Type** on an Employee Expense Account record.
- If **Generate Code** was used, **Code** shows the value assigned by the sequence
  template; otherwise it keeps the manually entered value.
