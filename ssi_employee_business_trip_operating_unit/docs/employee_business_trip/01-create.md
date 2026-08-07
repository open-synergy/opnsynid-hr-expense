# Create Employee Business Trip

> **Module:** ssi_employee_business_trip_operating_unit
>
> **Extends:** ssi_employee_business_trip — model `employee_business_trip`, action
> `01-create`

## Additional Pre-Condition

- **Access:** The user is a member of the **Operating Unit / Multiple Operating Units**
  group (`operating_unit.group_multi_operating_unit`). Without this group the Operating
  Unit field described below is not rendered on the form — there is no error message,
  the field simply does not appear.
- **Module:** `ssi_employee_business_trip_operating_unit` is installed.

## Additional Fields

When this module is installed, the create form gains one field, shown only to users in
the **Operating Unit / Multiple Operating Units** group
(`operating_unit.group_multi_operating_unit`):

- **Operating Unit**: The operating unit the business trip document belongs to.
  Displayed after the **Company** field. Editable while the document is in **Draft**
  status; becomes read-only once the document leaves Draft. Propagated to the
  `account.move` (and its journal items) created when the document is opened.

## Modified — Record Visibility

- The Business Trips list is filtered by operating unit (record rule). A user in the
  **Operating Unit** data ownership group of this module only sees business trip
  documents whose operating unit is in the list of operating units assigned to that
  user. This is not a Flow step.
