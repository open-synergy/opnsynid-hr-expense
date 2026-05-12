# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrReimbursement(models.Model):
    _name = "hr.reimbursement"
    _inherit = [
        "hr.reimbursement",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
