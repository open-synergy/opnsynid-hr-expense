# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrExpenseTypeProduct(models.Model):
    _name = "hr.expense_type_product"
    _description = "Expense Type Product"

    type_id = fields.Many2one(
        string="Expense Type",
        comodel_name="hr.expense_type",
        ondelete="cascade",
        required=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        ondelete="restrict",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
