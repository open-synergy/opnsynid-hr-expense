# Restart Employee Business Trip

> **Module:** ssi_employee_business_trip\
> **Model:** `employee_business_trip`\
> **Menu:** Human Resource > Expense > Business Trips\
> **Actor:** user in group `Employee Business Trip / Validator` (`restart_ok` policy)\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Record is in **Cancelled** or **Rejected** status.
- **Access:** User has _Can Restart_ access right.

## Flow

1. Open the **Human Resource > Expense > Business Trips** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
