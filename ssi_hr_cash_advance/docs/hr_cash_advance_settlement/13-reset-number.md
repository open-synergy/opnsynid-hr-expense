# Reset Document Number — Employee Cash Advance Settlement

> **Module:** ssi_hr_cash_advance\
> **Model:** `hr.cash_advance_settlement`\
> **Menu:** Human Resource > Expense > Cash Advance Settlements\
> **Actor:** user in group `Validator` (`hr_cash_advance_settlement_validator_group`)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Access:** User has _Can Input Manual Document Number_ access right.

## Flow

1. Open the **Human Resource > Expense > Cash Advance Settlements** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the number field and change it to
   **/**).
4. Click **OK** on the confirmation dialog. `action_reset_document_number` carries
   `confirm="Restart document number. Are you sure?"`.

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **Done** status,
  according to the sequence template configuration.
