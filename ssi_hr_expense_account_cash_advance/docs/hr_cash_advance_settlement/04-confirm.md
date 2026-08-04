# Confirm Cash Advance Settlement

> **Module:** ssi_hr_expense_account_cash_advance
>
> **Extends:** ssi_hr_cash_advance — model `hr_cash_advance_settlement`, aksi
> `04-confirm`

## Additional Validation

When this module is installed, confirmation will also fail if any settlement line has
**Required = True** and:

- **Expense Account** is not filled (no matching active expense account found for the
  employee, account, and settlement date), or
- The linked expense account has a negative residual balance.
