# Create Expense Type

> **Module:** ssi_hr_expense\
> **Model:** `hr.expense_type`\
> **Menu:** Human Resource > Configuration > Expense > Types\
> **Actor:** user in group `Expense Type`\
> **Inline Actions:** `action_generate_code` (Generate Code), `action_reset_code` (Reset
> code)

## Pre-Condition

- **Config:** An active `sequence.template` for `hr.expense_type` is required for the
  **Generate Code** button to succeed; without it, generating raises an error and the
  **Code** field must be filled in manually instead.
- **Access:** User is in group `Expense Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Expense Type** _(required)_: Enter the name of the expense type.
   - **Code** _(required)_: Enter a unique code identifying this expense type, or enter
     **/** to generate it later with the **Generate Code** button.
   - **Product Category** tab: Optionally add the product categories employees are
     allowed to submit expenses against. Click **Add a line**, then select a **Product
     Category**. Repeat as many times as needed. Leave empty to allow all categories.
   - **Product** tab: Optionally add the products employees are allowed to submit
     expenses against. Click **Add a line**, then select a **Product**. Repeat as many
     times as needed. Leave empty to allow all products.
   - **Product Usage** tab — **Allowed**: Optionally select the product usage types
     employees may use for this expense type. **Default**: Select the default product
     usage type, taken from **Allowed**.
   - **Pricelist** tab — **Selection Method**: Choose how the pricelist is determined —
     **Manual**, **Domain**, or **Python Code**. **Pricelists**: Select the allowed
     pricelists, shown only when **Selection Method** is **Manual**. **Domain**: Enter
     the domain used to filter pricelists, shown only when **Selection Method** is
     **Domain**. **Python Code**: Enter the code used to compute the allowed pricelists,
     shown only when **Selection Method** is **Python Code**.
4. Click **Save**.
5. On the header, click **Generate Code** to assign a code automatically from the
   configured `sequence.template`, if the **Code** field was left as **/**. You may also
   type the code directly at step 3 instead. Skipping this leaves the code as **/**
   until it is generated or entered manually. The **Types** list header also provides a
   **Reset code** button (confirmation required) that resets an already assigned code
   back to **/**, making the record eligible for automatic generation again.

## Post-Condition

- A new Expense Type record is created and active.
- The record becomes selectable wherever an Expense Type is required (e.g. cash advance,
  reimbursement).
