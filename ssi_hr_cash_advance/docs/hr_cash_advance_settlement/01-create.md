# Create Employee Cash Advance Settlement

> **Module:** ssi_hr_cash_advance\
> **Model:** `hr.cash_advance_settlement`\
> **Menu:** Human Resource > Expense > Cash Advance Settlements\
> **Actor:** user in group `User` (`hr_cash_advance_settlement_user_group`)\
> **State:** `—` → `draft`

## Pre-Condition

- At least one Cash Advance record in **Open** status exists for the employee.

## Flow

1. Open the **Human Resource > Expense > Cash Advance Settlements** menu.
2. Click the **New** button.
3. Fill in the required fields:
   - **Employee**: Automatically filled with the current user's employee. Change if
     needed.
   - **Department**: Automatically filled from **Employee**. Change if needed.
   - **Manager**: Automatically filled from **Employee**. Change if needed.
   - **Job Position**: Automatically filled from **Employee**. Change if needed.
   - **Currency**: Default filled from the company currency. Change if needed.
   - **Type**: Select the expense type for this settlement.
   - **# Cash Advance**: Select the cash advance to settle. Available options are
     filtered based on **Employee**, **Type**, and **Open** status.
   - **Pricelist**: Optional. Select the pricelist to use. Available options are
     filtered based on **Type**, **Employee**, and **Currency**.
   - **Date**: Select the settlement date.
   - **Journal**: Automatically filled from **Type**. Change if needed.
4. Add lines in the **Details** tab. Lines can also be loaded automatically by clicking
   the **Reload from Cash Advance** button, which copies lines from the selected Cash
   Advance. To add lines manually, repeat the following steps as many times as needed:
   - Click **Add a line**.
   - Fill in each line with:
     - **Date Expense**: Optional. Select the date the expense occurred.
     - **Product**: Select the product or expense item.
     - **Description**: Automatically filled from **Product**. Change if needed.
     - **Usage**: Automatically filled from **Type**. Change if needed.
     - **Account**: Automatically filled from **Product** and **Usage**. Change if
       needed.
     - **Analytic Account**: Optional. Select the analytic account.
     - **Pricelist**: Optional. Select the pricelist for the line.
     - **Quantity**: Enter the quantity.
     - **UoM**: Automatically filled from **Product**. Change if needed.
     - **Unit Price**: Automatically filled from **Pricelist** and **Product** if
       pricelist is set. Change if needed.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- Document number is still **/**.
