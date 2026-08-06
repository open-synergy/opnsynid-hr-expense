# Approve Employee Business Trip

> **Module:** ssi_employee_business_trip_documenso_signing
>
> **Extends:** ssi_employee_business_trip — model `employee_business_trip`, aksi
> `05-approve`

## Additional Pre-Condition

- **Config:** The record's active Approval Template has a Documenso Signing Template
  configured (`approval_template_id.documenso_signing_template_id`). Only then does the
  behavior described below apply; if it does not, the base Flow (steps 3–4, Click
  **Approve** / click **OK**) applies unchanged, exactly as documented in
  `ssi_employee_business_trip/docs/employee_business_trip/05-approve.md`.
- **Module:** `ssi_employee_business_trip_documenso_signing` is installed.

## Modified Flow

- Anchor: at Flow base step 2 (open the record to approve), the form already shows a
  **Signature Requests** tab (injected because `_documenso_signing_create_page = True`).
  This tab is always present once this module is installed, regardless of whether
  Documenso signing is actually used for the current approval.
- When a Documenso Signing Template **is** configured (see Additional Pre-Condition): no
  per-approver approval record is created for this document — a single
  `documenso.signature.request` is created and linked instead (during the earlier
  Confirm action, before this record reaches **Waiting for Approval**). Because there is
  no per-approver record naming the current user as an active approver, the **Approve**
  button (Flow base step 3) stays invisible for every user — it can never be clicked.
- Instead of clicking Approve, the user opens the linked request — shown under the
  **Approval Signing Request** group as the **Approval Signature Request** field in the
  **Signature Requests** tab (or via the **Open Signature Requests** button in the same
  tab) — and, on that request's own form, clicks **Send to Documenso** to send the
  document for e-signature. The designated signer(s) then sign the document outside
  Odoo, in Documenso.

## Additional Post-Condition

- Approval completes automatically — without any button click on this Employee Business
  Trip record — once the linked signature request reaches the **Signed** status (checked
  manually via **Check Status** on the request, or synced automatically by the
  connector). At that point, the base Post-Condition applies as usual: status changes to
  **In Progress** (or, if the record has no per-diem lines, directly to **Done**), the
  document number is generated automatically, and — if the record has per-diem lines —
  an accounting journal entry is created automatically. If other approval levels are
  still pending, status remains **Waiting for Approval**.
- If the linked signature request is **cancelled** instead (e.g. a signer declines in
  Documenso), the record moves directly to **Rejected** — the same end state as the base
  Reject action, but triggered automatically by the cancelled request rather than by a
  user clicking Reject.
