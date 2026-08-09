# Done Employee Cash Advance

> **Module:** ssi_hr_cash_advance\
> **Model:** `hr.cash_advance`\
> **Menu:** Human Resource > Expense > Cash Advances\
> **Actor:** system (`base.automation` record `cash_advance_open_2_done`, no user action)\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- Record is in **Open** status.
- Cash Advance Account move line is reconciled (**Settled** = True).

## Flow

This transition is triggered automatically by the system. No user action is required.

The system automatically changes the status to **Done** when the Cash Advance Account
move line is reconciled. This typically occurs when a Cash Advance Settlement for this
cash advance is posted (status **Done**).

## Post-Condition

- Status changes to **Done**.
