# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrCashAdvance(models.Model):
    _name = "hr.cash_advance"
    _inherit = [
        "hr.cash_advance",
        "mixin.single_operating_unit",
    ]
