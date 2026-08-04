# Create Cash Advance Settlement

> **Module:** ssi_hr_expense_account_cash_advance
>
> **Extends:** ssi_hr_cash_advance — model `hr_cash_advance_settlement`, aksi
> `01-create`

## Additional Fields

When this module is installed, each settlement line gains the following fields in the
line form (visible in the **Expense Account** tab of each line):

- **Required**: Automatically set to `True` if the selected product requires an expense
  account (determined by the combination of **Type** and **Product** configured in the
  expense type). Read-only.
- **Expense Account**: Automatically filled from the employee's active expense accounts
  that match the line's account (`account_id`) and the settlement date. Only filled when
  **Required** is `True`. Change if needed.

> These two fields also appear as inline columns in the settlement line tree view,
> alongside **Account**.
