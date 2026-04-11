# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrReimbursement(models.Model):
    """
    Extends hr.reimbursement with operating unit support.
    Adds mixin.single_operating_unit so reimbursement documents
    can be scoped to a specific operating unit.
    """

    _name = "hr.reimbursement"
    _inherit = [
        "hr.reimbursement",
        "mixin.single_operating_unit",
    ]
