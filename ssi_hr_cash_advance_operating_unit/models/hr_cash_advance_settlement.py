# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrCashAdvanceSettlement(models.Model):
    """
    Extends hr.cash_advance_settlement with operating unit support.
    Adds mixin.single_operating_unit so cash advance settlement
    documents can be scoped to a specific operating unit.
    """

    _name = "hr.cash_advance_settlement"
    _inherit = [
        "hr.cash_advance_settlement",
        "mixin.single_operating_unit",
    ]
