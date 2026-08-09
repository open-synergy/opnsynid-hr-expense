# Create Employee Reimbursement

> **Module:** ssi*hr_reimbursement\
> **Model:** `hr.reimbursement`\
> **Menu:** Human Resource > Expense > Reimbursements\
> **Actor:** user in group \_Reimbursement — User*\
> **State:** `—` → `draft`

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Expense > Reimbursements** menu.
2. Click the **New** button.
3. Fill in the required fields in the header:
   - **Employee**: Select the employee submitting the reimbursement.
   - **Currency**: Select the currency. Default is the company currency.
   - **Type**: Select the expense type. This determines allowed products, journal, and
     account.
   - **Bank Account**: Select the employee's bank account for payment.
   - **Pricelist** _(optional)_: Select the pricelist if available and relevant.
   - **Date**: Enter the document date.
   - **Duration** _(optional)_: Select a duration to automatically calculate **Date
     Due**.
   - **Date Due**: Enter the due date. Automatically filled if **Duration** is selected.
     Change if needed.
4. Fill in the **Accounting** tab:
   - **Journal**: Automatically filled from **Type**. Change if needed.
   - **Account**: Automatically filled from **Type**. Change if needed.
5. Add expense lines in the **Details** tab. Repeat the following steps as many times as
   needed:
   - Click **Add a line**.
   - Fill in each line with:
     - **Date Expense**: Date the expense occurred.
     - **Product**: Select the expense product/item (restricted by the selected Type).
     - **Description**: Brief description of the expense.
     - **Analytic Account** _(optional)_: Select the analytic account if available.
     - **Price Unit**: Unit price.
     - **Qty**: Quantity.
     - **UoM**: Unit of measure.
6. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
