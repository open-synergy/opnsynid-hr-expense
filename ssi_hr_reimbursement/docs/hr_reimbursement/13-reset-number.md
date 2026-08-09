# Reset Document Number — Employee Reimbursement

> **Module:** ssi_hr_reimbursement
> **Model:** `hr.reimbursement`
> **Menu:** Human Resource > Expense > Reimbursements
> **Actor:** user in group *Reimbursement — Validator*
> **Requires:** `01-create`

## Pre-Condition

- Record is in **Draft** status.
- User has _Can Input Manual Document Number_ access right.

## Flow

1. Open the **Human Resource > Expense > Reimbursements** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the number field and change it to
   **/**).

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number upon transitioning to **In Progress**
  status, according to the sequence template configuration.
