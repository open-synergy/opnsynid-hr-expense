# Create Employee Reimbursement

> **Module:** ssi_hr_expense_account_reimbursement
>
> **Extends:** ssi_hr_reimbursement — model `hr_reimbursement`, aksi `01-create`

## Additional Fields

When this module is installed, each reimbursement line gains the following fields:

- **Require Expense Account**: Automatically set based on the selected **Product** and
  **Expense Type**. If the product is listed as a product that requires an expense
  account in the expense type configuration, this field is set to `True`. Read-only.
- **# Expense Account**: Automatically filled when **Require Expense Account** is
  `True`. The system searches for the employee's active expense accounts that match all
  of the following criteria:

  - Linked to the same **Employee** as the reimbursement header.
  - Status is **Open**.
  - The expense account type includes the line's **Account** (`account_id`).
  - `Date Start` ≤ reimbursement **Date** ≤ `Date End` (or `Date End` is not set).

  If a matching expense account is found, the first result is assigned automatically.
  Read-only.
