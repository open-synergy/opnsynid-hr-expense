# Reopen Employee Cash Advance

## Pre-Condition

- Record is in **Done** status.
- Cash Advance Account move line reconciliation is removed (**Settled** = False).

## Flow

This transition is triggered automatically by the system. No user action is required.

The system automatically changes the status back to **Open** when the Cash Advance
Account move line reconciliation is removed. This typically occurs when the associated
Cash Advance Settlement is cancelled.

## Post-Condition

- Status changes back to **Open**.
