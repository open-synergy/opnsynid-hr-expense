# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class HrExpenseTypeProductCategory(models.Model):
    _name = "hr.expense_type_product_category"
    _description = "Expense Type Product Category"

    type_id = fields.Many2one(
        string="Expense Type",
        comodel_name="hr.expense_type",
        ondelete="cascade",
        required=True,
    )
    categ_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        ondelete="restrict",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
