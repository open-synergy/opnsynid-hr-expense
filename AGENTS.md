# Agent Instructions — opnsynid-hr-expense

This file is intended for **AI assistants** (GitHub Copilot, Claude, Cursor, ChatGPT,
and similar tools) working inside this repository.

This repository contains Odoo 14 modules for **HR Expense** features (Reimbursement,
Cash Advance, Expense Account, Business Trip), developed following SSI standard patterns
(PT. Simetri Sinergi Indonesia / OpenSynergy Indonesia).

---

## Modules in This Repository

| Module                                 | Description                                                   |
| -------------------------------------- | ------------------------------------------------------------- |
| `ssi_hr_expense`                       | Base module: expense type, product, and account configuration |
| `ssi_hr_reimbursement`                 | Employee reimbursement requests                               |
| `ssi_hr_reimbursement_operating_unit`  | Operating unit integration for reimbursement                  |
| `ssi_hr_reimbursement_work_log`        | Work log integration for reimbursement                        |
| `ssi_hr_cash_advance`                  | Employee cash advance requests and settlements                |
| `ssi_hr_cash_advance_operating_unit`   | Operating unit integration for cash advance                   |
| `ssi_hr_cash_advance_work_log`         | Work log integration for cash advance                         |
| `ssi_hr_expense_account`               | Employee expense account management (budget)                  |
| `ssi_hr_expense_account_reimbursement` | Expense account integration for reimbursement                 |
| `ssi_hr_expense_account_cash_advance`  | Expense account integration for cash advance settlement       |
| `ssi_hr_expense_account_work_log`      | Work log integration for expense account                      |
| `ssi_employee_business_trip`           | Employee business trip requests                               |
| `ssi_employee_business_trip_work_log`  | Work log integration for business trip                        |

---

## User Guide (Work Instructions)

Each module has a `docs/` directory containing **Work Instructions (IK)** — step-by-step
operational documentation for using the feature from the user's perspective.

### How to Answer User Questions About Feature Usage

1. Identify the feature being asked about (reimbursement, cash advance, expense account,
   etc.).
2. Find the relevant Work Instruction from the index below.
3. **Read that file** before answering — do not fabricate steps from assumptions.
4. If a relevant extension module is installed (marked _additive_ below), also read its
   Work Instruction and **merge** it with the base IK.
5. Answer based on the content of the Work Instruction.

### Work Instruction Location Pattern

```
<module_name>/docs/<model_name>/<number>-<action>.md
```

---

## Work Instruction Index

### `ssi_hr_reimbursement` — Model: `hr.reimbursement`

Menu: **Human Resource > Expense > Reimbursements**

| File                                                            | Action                                                |
| --------------------------------------------------------------- | ----------------------------------------------------- |
| `ssi_hr_reimbursement/docs/hr_reimbursement/01-create.md`       | Create a new reimbursement                            |
| `ssi_hr_reimbursement/docs/hr_reimbursement/02-edit.md`         | Edit a reimbursement                                  |
| `ssi_hr_reimbursement/docs/hr_reimbursement/03-delete.md`       | Delete a reimbursement                                |
| `ssi_hr_reimbursement/docs/hr_reimbursement/04-confirm.md`      | Confirm a reimbursement                               |
| `ssi_hr_reimbursement/docs/hr_reimbursement/05-approve.md`      | Approve a reimbursement                               |
| `ssi_hr_reimbursement/docs/hr_reimbursement/06-reject.md`       | Reject a reimbursement                                |
| `ssi_hr_reimbursement/docs/hr_reimbursement/07-start.md`        | Revert to In Progress (automatic via base.automation) |
| `ssi_hr_reimbursement/docs/hr_reimbursement/09-finish.md`       | Finish a reimbursement                                |
| `ssi_hr_reimbursement/docs/hr_reimbursement/10-cancel.md`       | Cancel a reimbursement                                |
| `ssi_hr_reimbursement/docs/hr_reimbursement/12-restart.md`      | Restart (back to Draft)                               |
| `ssi_hr_reimbursement/docs/hr_reimbursement/13-reset-number.md` | Reset document number                                 |

### `ssi_hr_expense_account_reimbursement` — Extends: `hr.reimbursement` _(additive)_

> Read together with `ssi_hr_reimbursement` above. This IK only documents **additional**
> fields and validations that appear when this module is installed.

| File                                                                       | Action                                          |
| -------------------------------------------------------------------------- | ----------------------------------------------- |
| `ssi_hr_expense_account_reimbursement/docs/hr_reimbursement/01-create.md`  | Additional fields when creating a reimbursement |
| `ssi_hr_expense_account_reimbursement/docs/hr_reimbursement/04-confirm.md` | Additional validations on confirmation          |

---

### `ssi_hr_cash_advance` — Model: `hr.cash_advance`

Menu: **Human Resource > Expense > Cash Advances**

| File                                                          | Action                    |
| ------------------------------------------------------------- | ------------------------- |
| `ssi_hr_cash_advance/docs/hr_cash_advance/01-create.md`       | Create a new cash advance |
| `ssi_hr_cash_advance/docs/hr_cash_advance/02-edit.md`         | Edit a cash advance       |
| `ssi_hr_cash_advance/docs/hr_cash_advance/03-delete.md`       | Delete a cash advance     |
| `ssi_hr_cash_advance/docs/hr_cash_advance/04-confirm.md`      | Confirm a cash advance    |
| `ssi_hr_cash_advance/docs/hr_cash_advance/05-approve.md`      | Approve a cash advance    |
| `ssi_hr_cash_advance/docs/hr_cash_advance/06-reject.md`       | Reject a cash advance     |
| `ssi_hr_cash_advance/docs/hr_cash_advance/07-reopen.md`       | Reopen a cash advance     |
| `ssi_hr_cash_advance/docs/hr_cash_advance/09-done.md`         | Mark cash advance as done |
| `ssi_hr_cash_advance/docs/hr_cash_advance/10-cancel.md`       | Cancel a cash advance     |
| `ssi_hr_cash_advance/docs/hr_cash_advance/12-restart.md`      | Restart a cash advance    |
| `ssi_hr_cash_advance/docs/hr_cash_advance/13-reset-number.md` | Reset document number     |

### `ssi_hr_cash_advance` — Model: `hr.cash_advance_settlement`

Menu: **Human Resource > Expense > Cash Advance Settlements**

| File                                                                     | Action                  |
| ------------------------------------------------------------------------ | ----------------------- |
| `ssi_hr_cash_advance/docs/hr_cash_advance_settlement/01-create.md`       | Create a new settlement |
| `ssi_hr_cash_advance/docs/hr_cash_advance_settlement/02-edit.md`         | Edit a settlement       |
| `ssi_hr_cash_advance/docs/hr_cash_advance_settlement/03-delete.md`       | Delete a settlement     |
| `ssi_hr_cash_advance/docs/hr_cash_advance_settlement/04-confirm.md`      | Confirm a settlement    |
| `ssi_hr_cash_advance/docs/hr_cash_advance_settlement/05-approve.md`      | Approve a settlement    |
| `ssi_hr_cash_advance/docs/hr_cash_advance_settlement/06-reject.md`       | Reject a settlement     |
| `ssi_hr_cash_advance/docs/hr_cash_advance_settlement/10-cancel.md`       | Cancel a settlement     |
| `ssi_hr_cash_advance/docs/hr_cash_advance_settlement/12-restart.md`      | Restart a settlement    |
| `ssi_hr_cash_advance/docs/hr_cash_advance_settlement/13-reset-number.md` | Reset settlement number |

### `ssi_hr_expense_account_cash_advance` — Extends: `hr.cash_advance_settlement` _(additive)_

> Read together with the `ssi_hr_cash_advance` settlement IK above.

| File                                                                                | Action                                       |
| ----------------------------------------------------------------------------------- | -------------------------------------------- |
| `ssi_hr_expense_account_cash_advance/docs/hr_cash_advance_settlement/01-create.md`  | Additional fields when creating a settlement |
| `ssi_hr_expense_account_cash_advance/docs/hr_cash_advance_settlement/04-confirm.md` | Additional validations on confirmation       |

---

### `ssi_hr_expense_account` — Model: `employee.expense_account`

Menu: **Human Resource > Expense > Expense Accounts**

| File                                                                      | Action                             |
| ------------------------------------------------------------------------- | ---------------------------------- |
| `ssi_hr_expense_account/docs/employee_expense_account/01-create.md`       | Create a new expense account       |
| `ssi_hr_expense_account/docs/employee_expense_account/02-edit.md`         | Edit an expense account            |
| `ssi_hr_expense_account/docs/employee_expense_account/03-delete.md`       | Delete an expense account          |
| `ssi_hr_expense_account/docs/employee_expense_account/04-confirm.md`      | Confirm an expense account         |
| `ssi_hr_expense_account/docs/employee_expense_account/05-approve.md`      | Approve an expense account         |
| `ssi_hr_expense_account/docs/employee_expense_account/06-reject.md`       | Reject an expense account          |
| `ssi_hr_expense_account/docs/employee_expense_account/07-start.md`        | Activate an expense account (Open) |
| `ssi_hr_expense_account/docs/employee_expense_account/09-finish.md`       | Finish an expense account          |
| `ssi_hr_expense_account/docs/employee_expense_account/10-cancel.md`       | Cancel an expense account          |
| `ssi_hr_expense_account/docs/employee_expense_account/11-terminate.md`    | Terminate an expense account       |
| `ssi_hr_expense_account/docs/employee_expense_account/12-restart.md`      | Restart an expense account         |
| `ssi_hr_expense_account/docs/employee_expense_account/13-reset-number.md` | Reset document number              |

---

### `ssi_employee_business_trip` — Model: `employee.business_trip`

Menu: **Human Resource > Expense > Business Trips**

| File                                                                        | Action                     |
| --------------------------------------------------------------------------- | -------------------------- |
| `ssi_employee_business_trip/docs/employee_business_trip/01-create.md`       | Create a new business trip |
| `ssi_employee_business_trip/docs/employee_business_trip/02-edit.md`         | Edit a business trip       |
| `ssi_employee_business_trip/docs/employee_business_trip/03-delete.md`       | Delete a business trip     |
| `ssi_employee_business_trip/docs/employee_business_trip/04-confirm.md`      | Confirm a business trip    |
| `ssi_employee_business_trip/docs/employee_business_trip/05-approve.md`      | Approve a business trip    |
| `ssi_employee_business_trip/docs/employee_business_trip/06-reject.md`       | Reject a business trip     |
| `ssi_employee_business_trip/docs/employee_business_trip/09-done.md`         | Mark business trip as done |
| `ssi_employee_business_trip/docs/employee_business_trip/10-cancel.md`       | Cancel a business trip     |
| `ssi_employee_business_trip/docs/employee_business_trip/12-restart.md`      | Restart a business trip    |
| `ssi_employee_business_trip/docs/employee_business_trip/13-reset-number.md` | Reset document number      |

---

## Module Development Guidelines

For code conventions, file structure, naming, security, views, and other SSI standard
patterns, follow the guidelines in the `copilot-instruction` repository (attached as a
separate workspace folder when available).
