# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class HrCashAdvanceLine(models.Model):
    _name = "hr.cash_advance_line"
    _inherit = [
        "mixin.product_line_account",
    ]
    _description = "Employee Cash Advance Line"

    cash_advance_id = fields.Many2one(
        string="# Employee Cash Advance",
        comodel_name="hr.cash_advance",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        required=True,
    )
