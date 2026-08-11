# Edit Employee Cash Advance Settlement

> **Module:** ssi_hr_cash_advance\
> **Model:** `hr.cash_advance_settlement`\
> **Menu:** Human Resource > Expense > Cash Advance Settlements\
> **Actor:** user in group `User` (`hr_cash_advance_settlement_user_group`)\
> **Requires:** `01-create`\
> **Inline Actions:** `action_reload_cash_advance` (Reload from Cash Advance)

## Pre-Condition

- **Record:** Record is in **Draft** status.

## Flow

1. Open the **Human Resource > Expense > Cash Advance Settlements** menu.
2. Find and open the record to edit.
3. Click the **Edit** button. **(14.0 only — the form opens directly editable on
   16.0+)**
4. Optionally, in the **Details** tab, click the **Reload from Cash Advance** button
   (**Inline Action**, `action_reload_cash_advance`) to rebuild the lines from the
   linked cash advance's lines.
5. Change the required fields.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.
