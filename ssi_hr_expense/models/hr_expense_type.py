# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
    allowed_product_usage_ids = fields.Many2many(
        string="Allowed Product Usage",
        comodel_name="product.usage_type",
        relation="rel_expense_type_2_product_usage",
        column1="expense_type_id",
        column2="product_usage_id",
    )
    default_product_usage_id = fields.Many2one(
        string="Default Product Usage",
        comodel_name="product.usage_type",
    )

    analytic_account_method = fields.Selection(
        string="Analytic Account Selection Method",
        selection=[
            ("fixed", "Fixed"),
            ("python", "Python Code"),
        ],
        default="fixed",
    )
    analytic_account_ids = fields.Many2many(
        string="Analytic Accounts",
        comodel_name="account.analytic.account",
        relation="rel_expense_type_2_analytic_account",
        column1="expense_type_id",
        column2="analytic_account_id",
    )
    python_code = fields.Text(
        string="Python Code",
        default="""# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: record on which the action is triggered; may be void.
#  - result: Return result, the value is list of Analytic Accounts.
result = []""",
        copy=True,
    )
