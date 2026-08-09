# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrReimbursement(models.Model):
    """
    Enables Documenso signing on the reimbursement approval flow.

    Mixes ``mixin.documenso_signing_approval`` into ``hr.reimbursement`` so
    that, when the active approval template defines a Documenso signing
    template, approval is driven by a ``documenso.signature.request``
    instead of the regular ``approval.approval`` records.
    """

    _name = "hr.reimbursement"
    _inherit = [
        "hr.reimbursement",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
