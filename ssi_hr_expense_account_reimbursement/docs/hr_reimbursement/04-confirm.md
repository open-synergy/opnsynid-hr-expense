# Confirm Employee Reimbursement

> **Module:** ssi_hr_expense_account_reimbursement **Extends:** ssi_hr_reimbursement

## Additional Validation

When this module is installed, confirmation will also fail if any reimbursement line
meets one of the following conditions:

- **Require Expense Account** is `True` but **# Expense Account** is not filled — raises
  error: _"No expense account"_.
- **# Expense Account** is filled but the linked expense account has a negative residual
  balance — raises error: _"Insufficient expense account"_.
