# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class EmployeeExpenseAccount(models.Model):
    """Add Documenso e-signature support to expense account approval.

    Mixes in ``mixin.documenso_signing_approval`` so an expense account's
    approval can be driven by a Documenso signature request instead of
    per-approver clicks, whenever the active approval template has a
    Documenso Signing Template configured. ``_documenso_signing_create_page
    = True`` injects the **Signature Requests** tab on the form
    regardless of whether Documenso signing is actually used.
    """

    _name = "employee_expense_account"
    _inherit = [
        "employee_expense_account",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
