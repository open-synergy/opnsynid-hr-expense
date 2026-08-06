# Create Employee Expense Account

> **Module:** ssi_hr_expense_account_work_log
>
> **Extends:** ssi_hr_expense_account — model `employee_expense_account`, action
> `01-create`

## Additional Pre-Condition

- **Module:** `ssi_hr_expense_account_work_log` is installed.

## Additional Fields

When this module is installed, the create form gains a **Work Log** tab:

- **Estimation**: The planned amount of work for this expense account, entered in hours.
  Optional.
- **Work Log Analytic Account**: The analytic account used to track work logged against
  this expense account. Optional.
- **Work Logs**: A list below **Work Log Analytic Account** where work performed against
  this expense account is recorded. Click **Add a line** to open the Work Log entry
  dialog; repeat as many times as needed.
- **Total**, **Remaining**, **Excess**: Read-only values, automatically computed from
  **Estimation** and the **Work Logs** lines. **Total** is the sum of the logged **Work
  Logs** amounts, **Remaining** is **Estimation** minus **Total** (floored at zero), and
  **Excess** is how much the logged amount exceeds **Estimation**. Not filled by the
  user.
