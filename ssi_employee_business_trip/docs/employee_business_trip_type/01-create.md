# Create Employee Business Trip Type

> **Module:** ssi_employee_business_trip\
> **Model:** `employee_business_trip_type`\
> **Menu:** Human Resource > Configuration > Expense > Business Trip Types\
> **Actor:** user in group `Human Resource - Configurator / Employee Business Trip Type`\
> **Inline Actions:** `action_generate_code` (Generate Code), `action_reset_code` (Reset
> code)

## Pre-Condition

- **Config:** A `sequence.template` for this model must be configured before using the
  **Generate Code** button (see step 8). Not required when **Code** is entered manually.
- **Data:** At least one **Journal** and one **Payable Account** exist to be selected on
  the **Accounting** tab.
- **Access:** User is in group
  `Human Resource - Configurator / Employee Business Trip Type`.

## Flow

1. Open the **Human Resource > Configuration > Expense > Business Trip Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the business trip type name.
   - **Code** _(required)_: Enter a unique code for this type, or fill with **/** and
     use the **Generate Code** button later (see step 8) to assign one automatically.
4. On the **Product** tab, set:
   - **Product Selection Method**: Select how per diem products allowed on a business
     trip of this type are determined: **Manual**, **Domain** (default), or **Python
     Code**.
   - **Products**: Only visible when Product Selection Method = **Manual**. Select the
     allowed products.
   - **Product Domain**: Only visible when Product Selection Method = **Domain**. Enter
     the domain expression evaluated against Product. Default: `[]`.
   - **Product Python Code**: Only visible when Product Selection Method = **Python
     Code**. Enter the Python code that sets the `result` variable to a recordset of
     Product. Default: `result = []`.
5. On the **Currencies & Pricelist** tab, set:
   - **Currency Selection Method**: Select how currencies allowed on a business trip of
     this type are determined: **Manual**, **Domain** (default), or **Python Code**.
   - **Currencies**: Only visible when Currency Selection Method = **Manual**. Select
     the allowed currencies.
   - **Currency Domain**: Only visible when Currency Selection Method = **Domain**.
     Enter the domain expression evaluated against Currency. Default: `[]`.
   - **Currency Python Code**: Only visible when Currency Selection Method = **Python
     Code**. Enter the Python code that sets the `result` variable to a recordset of
     Currency. Default: `result = []`.
   - **Pricelist Selection Method**: Select how pricelists allowed on a business trip of
     this type are determined: **Manual**, **Domain** (default), or **Python Code**.
   - **Pricelists**: Only visible when Pricelist Selection Method = **Manual**. Select
     the allowed pricelists.
   - **Pricelist Domain**: Only visible when Pricelist Selection Method = **Domain**.
     Enter the domain expression evaluated against Pricelist. Default: `[]`.
   - **Pricelist Python Code**: Only visible when Pricelist Selection Method = **Python
     Code**. Enter the Python code that sets the `result` variable to a recordset of
     Pricelist. Default: `result = []`.
6. On the **Origin & Destination** tab, set:
   - **Origin Selection Method**: Select how origin cities allowed on a business trip of
     this type are determined: **Manual**, **Domain** (default), or **Python Code**.
   - **Origins**: Only visible when Origin Selection Method = **Manual**. Select the
     allowed origin cities.
   - **Origin Domain**: Only visible when Origin Selection Method = **Domain**. Enter
     the domain expression evaluated against Origin. Default: `[]`.
   - **Origin Python Code**: Only visible when Origin Selection Method = **Python
     Code**. Enter the Python code that sets the `result` variable to a recordset of
     Origin. Default: `result = []`.
   - **Destination Selection Method**: Select how destination cities allowed on a
     business trip of this type are determined: **Manual**, **Domain** (default), or
     **Python Code**.
   - **Destinations**: Only visible when Destination Selection Method = **Manual**.
     Select the allowed destination cities.
   - **Destination Domain**: Only visible when Destination Selection Method =
     **Domain**. Enter the domain expression evaluated against Destination. Default:
     `[]`.
   - **Destination Python Code**: Only visible when Destination Selection Method =
     **Python Code**. Enter the Python code that sets the `result` variable to a
     recordset of Destination. Default: `result = []`.
7. On the **Accounting** tab, fill in:
   - **Journal** _(required)_: Select the accounting journal used to post business trip
     documents of this type.
   - **Payable Account** _(required)_: Select the payable account used to post business
     trip documents of this type.
8. If **Code** was left as **/**, click the **Generate Code** button in the header to
   automatically assign a code from the configured `sequence.template`. Skip this step
   if an explicit code was entered manually — **Generate Code** only changes records
   whose **Code** is still **/**. To undo a previously generated code later, select the
   record in the **Business Trip Types** list, click **Reset code** in the list toolbar,
   then click **OK** to confirm — this clears **Code** back to **/** so it can be
   regenerated.
9. Click **Save**.

## Post-Condition

- A new Employee Business Trip Type record is created and available for selection as
  **Type** on an Employee Business Trip record.
- If **Generate Code** was used, **Code** shows the value assigned by the sequence
  template; otherwise it keeps the manually entered value.
