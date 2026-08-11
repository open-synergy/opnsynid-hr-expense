# Revert Employee Reimbursement to In Progress

> **Module:** ssi_hr_reimbursement\
> **Model:** `hr.reimbursement`\
> **Menu:** Human Resource > Expense > Reimbursements\
> **Actor:** System — triggered automatically by `base.automation` (`reimbursement_ready_2_open`),
> no user action\
> **State:** `done` → `open`\
> **Requires:** `09-finish`\
> **Inline Actions:** `action_recompute_realization` (Recompute Realization)

---

> **Note:** There is no manual Revert to In Progress action. The status transition back
> to **In Progress** is handled automatically by the system via `base.automation` when
> the accounting journal entry reconciliation is reversed (payment cancelled or
> unmatched).

## Pre-Condition

- **Record:** Record is in **Done** status.
- **Data:** The associated accounting journal entry exists and was previously
  reconciled.

## Flow

This transition is triggered automatically by the system. No user action is required.

The system automatically changes the status back to **In Progress** when the payable
move line reconciliation is reversed (i.e., the `reconciled` field changes from `True`
to `False` — e.g., payment is deleted or unapplied). This typically occurs when a
payment linked to the reimbursement is cancelled or unmatched through the accounting
module (**Accounting > Vendors > Payments** or bank statement reconciliation).

Additionally, once the record is in **In Progress** or **Done** status, the user may
click the **Recompute Realization** button (**Inline Action**,
`action_recompute_realization`) on the record's header to manually re-evaluate its
realized/reconciled state, instead of waiting for the triggering event above.

## Post-Condition

- Status returns to **In Progress**.
