# Approve Employee Cash Advance Settlement

## Pre-Condition

- Record is in **Waiting for Approval** status.
- User is registered as an approver on the active approval template.
- User has _Can Approve_ access right.

## Flow

1. Open the **Human Resource > Expense > Cash Advance Settlements** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes to **Done** and a journal entry
  is automatically created in the configured journal to reconcile the settlement against
  the original cash advance.
- If there are still pending approval levels, status remains **Waiting for Approval**.
