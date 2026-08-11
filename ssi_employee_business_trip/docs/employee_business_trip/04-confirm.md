# Confirm Employee Business Trip

> **Module:** ssi_employee_business_trip\
> **Model:** `employee_business_trip`\
> **Menu:** Human Resource > Expense > Business Trips\
> **Actor:** user in group `Employee Business Trip / User` (`confirm_ok` policy)\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Access:** User has _Can Confirm_ access right.

## Flow

1. Open the **Human Resource > Expense > Business Trips** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
