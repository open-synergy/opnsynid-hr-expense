# Finish Employee Reimbursement

> **Module:** ssi_hr_reimbursement\
> **Model:** `hr.reimbursement`\
> **Menu:** Human Resource > Expense > Reimbursements\
> **Actor:** System — triggered automatically by `base.automation` (`reimbursement_ready_2_done`),
> no user action\
> **State:** `open` → `done`\
> **Requires:** `05-approve`\
> **Inline Actions:** `action_recompute_realization` (Recompute Realization)

---

> **Note:** There is no manual Finish action. The status transition to **Done** is
> handled automatically by the system via `base.automation` when the accounting journal
> entry associated with this reimbursement is fully reconciled (payment received). This
> file is kept as reference documentation only.

## Pre-Condition

- **Record:** Record is in **In Progress** status.
- **Data:** The associated accounting journal entry exists.

## Flow

This transition is triggered automatically by the system. No user action is required.

The system automatically changes the status to **Done** when the payable move line is
fully reconciled (i.e., the `reconciled` field changes from `False` to `True`). This
typically occurs when a payment for this reimbursement is processed through the
accounting module (**Accounting > Vendors > Payments** or bank statement
reconciliation).

Additionally, once the record is in **In Progress** or **Done** status, the user may
click the **Recompute Realization** button (**Inline Action**,
`action_recompute_realization`) on the record's header to manually re-evaluate its
realized/reconciled state, instead of waiting for the triggering event above.

## Post-Condition

- Status changes to **Done**.
