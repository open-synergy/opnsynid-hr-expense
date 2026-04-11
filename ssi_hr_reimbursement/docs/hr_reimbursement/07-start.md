# Revert Employee Reimbursement to In Progress

> **Note:** There is no manual Revert to In Progress action. The status transition back
> to **In Progress** is handled automatically by the system via `base.automation` when
> the accounting journal entry reconciliation is reversed (payment cancelled or
> unmatched).

## Pre-Condition

- Record is in **Done** status.
- The associated accounting journal entry exists and was previously reconciled.

## Flow

This transition is automatic. No user action is required in the Reimbursement form.

The system monitors the `reconciled` field. When it changes from `True` to `False`
(i.e., the payable move line reconciliation is reversed — e.g., payment is deleted or
unapplied), the automation `reimbursement_ready_2_open` triggers `action_open`
automatically.

To reverse the reconciliation, cancel or delete the payment through the accounting
module (**Accounting > Vendors > Payments** or bank statement reconciliation).

## Post-Condition

- Status returns to **In Progress** automatically once the journal entry reconciliation
  is reversed.
