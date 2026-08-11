# Reopen Employee Cash Advance

> **Module:** ssi_hr_cash_advance\
> **Model:** `hr.cash_advance`\
> **Menu:** Human Resource > Expense > Cash Advances\
> **Actor:** system (`base.automation` record `cash_advance_done_2_open`, no user action)\
> **State:** `done` → `open`\
> **Requires:** `09-done`\
> **Inline Actions:** `action_recompute_realization` (Recompute Realization)

## Pre-Condition

- **Record:** Record is in **Done** status.
- **Record:** Cash Advance Account move line reconciliation is removed (**Settled** =
  False).

## Flow

This transition is triggered automatically by the system. No user action is required.

The system automatically changes the status back to **Open** when the Cash Advance
Account move line reconciliation is removed. This typically occurs when the associated
Cash Advance Settlement is cancelled.

Additionally, once the record is in **Open** or **Done** status, the user may click the
**Recompute Realization** button (**Inline Action**, `action_recompute_realization`) on
the record's header to manually re-evaluate its realized/settled state, instead of
waiting for the triggering event above.

## Post-Condition

- Status changes back to **Open**.
