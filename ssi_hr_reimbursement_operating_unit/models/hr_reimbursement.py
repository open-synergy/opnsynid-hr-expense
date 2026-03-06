# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrReimbursement(models.Model):
    _name = "hr.reimbursement"
    _inherit = [
        "hr.reimbursement",
        "mixin.single_operating_unit",
    ]
