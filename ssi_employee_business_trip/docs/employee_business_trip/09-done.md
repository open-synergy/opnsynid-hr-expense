# Finish Employee Business Trip

> **Module:** ssi_employee_business_trip\
> **Model:** `employee_business_trip`\
> **Menu:** Human Resource > Expense > Business Trips\
> **Actor:** system (`base.automation` `employee_business_trip_ready_2_done`)\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

**Note:** There is no manual Done action. The status transition to **Done** is handled
automatically by the system via `base.automation` when the payable journal entry line
associated with this business trip is fully reconciled (payment made). This file is kept
as reference documentation only.

## Pre-Condition

- Record is in **In Progress** status.
- The associated payable accounting journal entry line (`payable_move_line_id`) exists.

## Flow

This transition is automatic. No user action is required in the Employee Business Trip
form.

The system monitors the `realized` field, which is related to
`payable_move_line_id.reconciled`. When it changes from `False` to `True` (i.e., the
payable move line is fully matched against a payment), the automation
`employee_business_trip_ready_2_done` triggers `action_done` automatically.

To trigger reconciliation, process the payment through the accounting module
(**Accounting > Vendors > Payments** or bank statement reconciliation).

## Post-Condition

- Status changes to **Done** automatically once the payable journal entry line is fully
  reconciled.
