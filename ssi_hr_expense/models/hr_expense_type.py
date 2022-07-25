# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class HrExpenseType(models.Model):
    _name = "hr.expense_type"
    _inherit = ["mixin.master_data"]
    _description = "Expense Type"

    name = fields.Char(
        string="Expense Type",
    )
    product_ids = fields.One2many(
        string="Product",
        comodel_name="hr.expense_type_product",
        inverse_name="type_id",
    )

    @api.depends(
        "product_ids",
    )
    def _compute_allowed_product_ids(self):
        for record in self:
            result = []
            if record.product_ids:
                for product in record.product_ids:
                    result.append(product.product_id.id)
            record.allowed_product_ids = result

    allowed_product_ids = fields.Many2many(
        string="Allowed Product",
        comodel_name="product.product",
        compute="_compute_allowed_product_ids",
        store=False,
        compute_sudo=True,
    )
    product_category_ids = fields.One2many(
        string="Product Category",
        comodel_name="hr.expense_type_product_category",
        inverse_name="type_id",
    )

    @api.depends(
        "product_category_ids",
    )
    def _compute_allowed_product_category_ids(self):
        for record in self:
            result = []
            if record.product_category_ids:
                for categ in record.product_category_ids:
                    result.append(categ.categ_id.id)
            record.allowed_product_category_ids = result

    allowed_product_category_ids = fields.Many2many(
        string="Allowed Product Category",
        comodel_name="product.category",
        compute="_compute_allowed_product_category_ids",
        store=False,
        compute_sudo=True,
    )
