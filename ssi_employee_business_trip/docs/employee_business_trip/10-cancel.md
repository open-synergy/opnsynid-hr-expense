# Cancel Employee Business Trip

> **Module:** ssi_employee_business_trip\
> **Model:** `employee_business_trip`\
> **Menu:** Human Resource > Expense > Business Trips\
> **Actor:** user in group `Employee Business Trip / Validator` (`cancel_ok` policy)\
> **State:** `draft` | `confirm` | `open` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- Record is in a status that allows cancellation (**Draft**, **Waiting for Approval**,
  or **In Progress**).
- User has _Can Cancel_ access right.

## Flow

1. Open the **Human Resource > Expense > Business Trips** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- If the record was **In Progress** with an accounting journal entry, the journal entry
  is deleted automatically.
