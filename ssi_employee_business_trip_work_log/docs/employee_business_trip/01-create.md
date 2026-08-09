# Create Employee Business Trip

> **Module:** ssi_employee_business_trip_work_log
>
> **Model:** `employee_business_trip`
>
> **Menu:** Human Resource > Expense > Business Trips
>
> **Actor:** user in group _Employee Business Trip — User_
>
> **State:** `—` → `draft`
>
> **Requires:** `ssi_employee_business_trip/employee_business_trip/01-create`

This document is an **IK extension**: it covers only the **Work Log** tab added by this
module to the `employee_business_trip` create form. It does not repeat the base header,
**Trip Information**, **Per Diem**, or **Accounting** steps — see `Requires:` above for
the full base Flow.

## Pre-Condition

- **Module:** `ssi_employee_business_trip_work_log` is installed.

## Flow

1. Open the **Human Resource > Expense > Business Trips** menu, then click the **New**
   button. _(Same entry point as `employee_business_trip/01-create`.)_
2. Click the **Work Log** tab.
3. Enter a value in the **Estimation** field. Optional.
4. Select an account in the **Work Log Analytic Account** field. Optional.
5. Click **Add a line** below **Work Log Analytic Account** to open the Work Log entry
   dialog.
6. Click **Discard** to close the dialog without saving a line. Work Log lines are
   optional at create time; this document does not continue through saving a line, nor
   through the rest of the base create Flow (Trip Information, Per Diem, Accounting,
   Save).

## Post-Condition

- The Work Log entry dialog is closed and the Employee Business Trip create form remains
  open, still in edit mode.
- No Work Log line has been added. **Total**, **Remaining**, and **Excess** are
  read-only values computed from **Estimation** and the **Work Logs** lines; they are
  not filled by the user and are not verified by this document.
