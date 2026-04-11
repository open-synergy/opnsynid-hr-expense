# Cancel Employee Cash Advance Settlement

## Pre-Condition

- Record is in a status that allows cancellation (**Draft**, **Waiting for Approval**,
  or **Done**).
- User has _Can Cancel_ access right.

## Flow

1. Open the **Human Resource > Expense > Cash Advance Settlements** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.

## Post-Condition

- Status changes to **Cancelled**.
- If the record was in **Done** status, the associated journal entry is automatically
  deleted and the reconciliation with the cash advance move line is reversed.
