# Create Employee Business Trip

## Pre-Condition

- None.

## Flow

1. Open the **Human Resource > Expense > Business Trips** menu.
2. Click the **New** button.
3. Fill in the required fields in the header:
   - **Employee**: Select the employee submitting the business trip request.
   - **Department**: Automatically filled from **Employee**. Read-only.
   - **Manager**: Automatically filled from **Employee**. Read-only.
   - **Job Position**: Automatically filled from **Employee**. Read-only.
   - **Type**: Select the business trip type.
   - **Date**: Enter the accounting/document date.
4. In the **Trip Information** tab, fill in:
   - **Date Start**: Enter the travel start date.
   - **Date End**: Enter the travel end date.
   - **Origin**: Select the origin city. Available options are based on **Type**.
   - **Destination**: Select the destination city. Available options are based on
     **Type**.
5. In the **Per Diem** tab, fill in:
   - **Currency**: Select the currency. Available options are based on **Type**.
   - **Pricelist**: Select the pricelist. Available options are based on **Type**.
   - **Analytic Account**: Select the analytic account if applicable.
   - **Date Due**: Enter the payment due date.
   - Add lines in the **Per Diem** table. Repeat the following steps as many times as
     needed:
     - Click **Add a line**.
     - Fill in each line with:
       - **Product**: Select the per-diem product. Available options are based on
         **Type**.
       - **Description**: Automatically filled from **Product**. Change if needed.
       - **Usage**: Select the usage category.
       - **Account**: Automatically filled from **Product**. Change if needed.
       - **Analytic Account**: Select if applicable.
       - **Qty.**: Enter the quantity.
       - **UoM**: Automatically filled from **Product**. Change if needed.
       - **Price**: Automatically filled from **Pricelist** and **Product**. Change if
         needed.
       - **Taxes**: Select applicable taxes if any.
6. In the **Accounting** tab, verify:
   - **Journal**: Automatically filled from **Type**. Change if needed.
   - **Payable Account**: Automatically filled from **Type**. Change if needed.
7. Click **Save**.

## Post-Condition

- A new Employee Business Trip record is created in **Draft** status.
- Document number is still **/** (not yet generated).
