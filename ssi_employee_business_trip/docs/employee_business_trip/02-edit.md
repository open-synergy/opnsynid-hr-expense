# Edit Employee Business Trip

> **Module:** ssi_employee_business_trip\
> **Model:** `employee_business_trip`\
> **Menu:** Human Resource > Expense > Business Trips\
> **Actor:** user in group `Employee Business Trip / User`\
> **Requires:** `01-create`\
> **Inline Actions:** `action_compute_tax` (Compute Tax)

## Pre-Condition

- **Record:** Record is in **Draft** status.

## Flow

1. Open the **Human Resource > Expense > Business Trips** menu.
2. Find and open the record to edit.
3. Click the **Edit** button. **(14.0 only — the form opens directly editable on
   16.0+)**
4. Change the required fields.
5. Optionally, on the **Accounting** tab, click the **Compute Tax** button to recompute
   the **Taxes** table from the taxes selected on each **Per Diem** line.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.
