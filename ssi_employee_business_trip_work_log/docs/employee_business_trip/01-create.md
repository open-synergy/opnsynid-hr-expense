# Create Employee Business Trip

> **Module:** ssi_employee_business_trip_work_log **Extends:**
> ssi_employee_business_trip — model `employee_business_trip`, action `01-create`

## Additional Pre-Condition

- **Module:** `ssi_employee_business_trip_work_log` is installed.

## Additional Fields

When this module is installed, the create form gains a **Work Log** tab:

- **Estimation**: The planned amount of work for this business trip, entered in hours.
  Optional.
- **Work Log Analytic Account**: The analytic account used to track work logged against
  this business trip. Optional.
- **Work Logs**: A list below **Work Log Analytic Account** where work performed against
  this business trip is recorded. Click **Add a line** to open the Work Log entry
  dialog; repeat as many times as needed.
- **Total**, **Remaining**, **Excess**: Read-only values, automatically computed from
  **Estimation** and the **Work Logs** lines. **Total** is the sum of the logged **Work
  Logs** amounts, **Remaining** is **Estimation** minus **Total** (floored at zero), and
  **Excess** is how much the logged amount exceeds **Estimation**. Not filled by the
  user.
