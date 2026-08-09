# Finish Employee Reimbursement

> **Module:** ssi_hr_reimbursement\
> **Model:** `hr.reimbursement`\
> **Menu:** Human Resource > Expense > Reimbursements\
> **Actor:** System — triggered automatically by `base.automation` (`reimbursement_ready_2_done`),
> no user action\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

---

> **Note:** There is no manual Finish action. The status transition to **Done** is
> handled automatically by the system via `base.automation` when the accounting journal
> entry associated with this reimbursement is fully reconciled (payment received). This
> file is kept as reference documentation only.

## Pre-Condition

- Record is in **In Progress** status.
- The associated accounting journal entry exists.

## Flow

This transition is automatic. No user action is required in the Reimbursement form.

The system monitors the `reconciled` field. When it changes from `False` to `True`
(i.e., the payable move line is fully matched against a payment), the automation
`reimbursement_ready_2_done` triggers `action_done` automatically.

To trigger reconciliation, process the payment through the accounting module
(**Accounting > Vendors > Payments** or bank statement reconciliation).

## Post-Condition

- Status changes to **Done** automatically once the journal entry is fully reconciled.
