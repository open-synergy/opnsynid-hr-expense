# Edit Expense Type

> **Module:** ssi_hr_expense\
> **Model:** `hr.expense_type`\
> **Menu:** Human Resource > Configuration > Expense > Types\
> **Actor:** user in group `Expense Type`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_generate_code` (Generate Code), `action_reset_code` (Reset
> code)

## Pre-Condition

- **Record:** The record already exists (see `01-create`).
- **Config:** An active `sequence.template` for `hr.expense_type` is required for the
  **Generate Code** button to succeed; without it, generating raises an error.
- **Access:** User is in group `Expense Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Types** menu.
2. Find and open the Expense Type record to edit.
3. Click the **Edit** button.
4. Change the required fields (**Expense Type**, **Code**) or the **Product Category**,
   **Product**, **Product Usage**, and **Pricelist** tabs as needed.
5. Click **Save**.
6. On the header, click **Generate Code** to assign a new code automatically — for
   example after changing the **Code** field back to **/** and saving. Only works while
   the **Code** field is **/**; skipping it leaves the current code unchanged.
7. Alternatively, from the **Types** list, select the record's checkbox and click
   **Reset code** in the list header to reset its **Code** field back to **/**, making
   it eligible for automatic generation again. Click **OK** on the confirmation dialog.
   The same list header also has a **Generate code** button that generates codes for the
   selected records in bulk; it also asks for confirmation.

## Post-Condition

- The record is updated with the new values.
