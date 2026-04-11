# Create Employee Cash Advance

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Expense > Cash Advances** menu.
2. Click the **New** button.
3. Fill in the required fields:
   - **Employee**: Automatically filled with the current user's employee. Change if
     needed.
   - **Department**: Automatically filled from **Employee**. Change if needed.
   - **Manager**: Automatically filled from **Employee**. Change if needed.
   - **Job Position**: Automatically filled from **Employee**. Change if needed.
   - **Date**: Select the date of the cash advance request.
   - **Duration**: Optional. Select a duration to auto-calculate the due date.
   - **Date Due**: Automatically filled if **Duration** is selected. Change if needed.
   - **Type**: Select the expense type for this cash advance.
   - **Currency**: Default filled from the company currency. Change if needed.
   - **Pricelist**: Optional. Select the pricelist to use for this cash advance.
     Available options are filtered based on **Type**, **Employee**, and **Currency**.
   - **Journal**: Automatically filled from **Type**. Change if needed.
   - **Cash Advance Account**: Automatically filled from **Type**. Change if needed.
   - **Payable Account**: Automatically filled from **Type**. Change if needed.
4. Add lines in the **Details** tab. Repeat the following steps as many times as needed:
   - Click **Add a line**.
   - Fill in each line with:
     - **Date Expense**: Optional. Select the date the expense occurred.
     - **Product**: Select the product or expense item.
     - **Description**: Automatically filled from **Product**. Change if needed.
     - **Usage**: Automatically filled from **Type**. Change if needed.
     - **Account**: Automatically filled from **Product** and **Usage**. Change if
       needed.
     - **Analytic Account**: Optional. Select the analytic account.
     - **Pricelist**: Automatically filled from the parent's currency. Change if needed.
     - **Quantity**: Enter the quantity.
     - **UoM**: Automatically filled from **Product**. Change if needed.
     - **Unit Price**: Automatically filled from **Pricelist** and **Product** if
       pricelist is set. Change if needed.
     - **Tax(es)**: Automatically filled from **Product** and **Usage**. Change if
       needed.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- Document number is still **/**.
