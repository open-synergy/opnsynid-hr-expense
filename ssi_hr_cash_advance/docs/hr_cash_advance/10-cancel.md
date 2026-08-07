# Cancel Employee Cash Advance

## Pre-Condition

- Record is in a status that allows cancellation (**Draft**, **Waiting for Approval**,
  or **Open**).
- User has _Can Cancel_ access right.

## Flow

1. Open the **Human Resource > Expense > Cash Advances** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- If the record was in **Open** status, the associated journal entry is automatically
  deleted.
