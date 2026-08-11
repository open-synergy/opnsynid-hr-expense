# Done Employee Cash Advance

> **Module:** ssi_hr_cash_advance\
> **Model:** `hr.cash_advance`\
> **Menu:** Human Resource > Expense > Cash Advances\
> **Actor:** system (`base.automation` record `cash_advance_open_2_done`, no user action)\
> **State:** `open` → `done`\
> **Requires:** `05-approve`\
> **Inline Actions:** `action_recompute_realization` (Recompute Realization)

## Pre-Condition

- **Record:** Record is in **Open** status.
- **Record:** Cash Advance Account move line is reconciled (**Settled** = True).

## Flow

This transition is triggered automatically by the system. No user action is required.

The system automatically changes the status to **Done** when the Cash Advance Account
move line is reconciled. This typically occurs when a Cash Advance Settlement for this
cash advance is posted (status **Done**).

Additionally, once the record is in **Open** or **Done** status, the user may click the
**Recompute Realization** button (**Inline Action**, `action_recompute_realization`) on
the record's header to manually re-evaluate its realized/settled state, instead of
waiting for the triggering event above.

## Post-Condition

- Status changes to **Done**.
