# Approve Employee Business Trip

> **Module:** ssi_employee_business_trip\
> **Model:** `employee_business_trip`\
> **Menu:** Human Resource > Expense > Business Trips\
> **Actor:** user registered as an approver on the active `approval.template` (`approve_ok`
> policy)\
> **State:** `confirm` → `open` | `done`\
> **Requires:** `04-confirm`

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an approver on the active approval template.
- User has _Can Approve_ access right.

## Flow

1. Open the **Human Resource > Expense > Business Trips** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled:
  - Status changes to **In Progress**.
  - Document number is generated automatically according to the sequence configuration.
  - If the record has per-diem lines, an accounting journal entry is created
    automatically.
  - If the record has no per-diem lines, status changes directly to **Done**.
- If there are still pending approval levels, status remains **Waiting for Approval**.
