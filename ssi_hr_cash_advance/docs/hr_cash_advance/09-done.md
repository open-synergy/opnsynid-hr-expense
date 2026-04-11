# Done Employee Cash Advance

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
