# Reset Document Number — Employee Business Trip

> **Module:** ssi_employee_business_trip\
> **Model:** `employee_business_trip`\
> **Menu:** Human Resource > Expense > Business Trips\
> **Actor:** user in group `Employee Business Trip / Validator` (`manual_number_ok` policy)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Access:** User has _Can Input Manual Document Number_ access right.

## Flow

1. Open the **Human Resource > Expense > Business Trips** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the number field and change it to
   **/**).
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **In Progress**,
  according to the sequence template configuration.
