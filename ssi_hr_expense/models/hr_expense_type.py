# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrExpenseType(models.Model):
    """
    Master data for employee expense types.
    Defines the allowed products and product categories that employees
    can use, along with pricelist configuration for expense valuation.
    """

    _name = "hr.expense_type"
    _inherit = ["mixin.master_data", "mixin.product_pricelist_m2o_configurator"]
    _description = "Expense Type"

    _product_pricelist_m2o_configurator_insert_form_element_ok = True
    _product_pricelist_m2o_configurator_form_xpath = "//page[@name='pricelist']"

    name = fields.Char(
        string="Expense Type",
    )
    product_ids = fields.One2many(
        string="Product",
        comodel_name="hr.expense_type_product",
        inverse_name="type_id",
    )
    pricelist_ids = fields.Many2many(
        relation="rel_expense_type_2_pricelist",
        column1="type_id",
        column2="pricelist_id",
    )

    @api.depends(
        "product_ids",
    )
    def _compute_allowed_product_ids(self):
        """Collect the products allowed for this expense type.

        Builds the list from ``product_ids`` (the type's product lines),
        one product per line, so downstream views can restrict expense
        line selection to only those products.
        """
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
        """Collect the product categories allowed for this expense type.

        Builds the list from ``product_category_ids`` (the type's product
        category lines), one category per line, so downstream views can
        restrict expense line selection to only those categories.
        """
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

    analytic_account_selection_method = fields.Selection(
        string="Analytic Account Selection Method",
        selection=[
            ("manual", "Manual"),
            ("domain", "Domain"),
            ("code", "Python Code"),
        ],
        default="domain",
        required=True,
        help="How the analytic accounts allowed on documents using this "
        "expense type are resolved: Manual picks from "
        "'Analytic Accounts' below, Domain filters "
        "account.analytic.account with the domain expression below, "
        "Python Code runs the Python snippet below and reads its "
        "'result' variable.",
    )
    analytic_account_ids = fields.Many2many(
        string="Analytic Accounts",
        comodel_name="account.analytic.account",
        relation="rel_expense_type_2_analytic_account",
        column1="expense_type_id",
        column2="analytic_account_id",
        help="Analytic accounts allowed on documents using this expense "
        "type. Used only when 'Analytic Account Selection Method' is "
        "set to Manual.",
    )
    analytic_account_domain = fields.Text(
        string="Analytic Account Domain",
        default="[]",
        help="Domain expression evaluated against account.analytic.account "
        "to resolve the analytic accounts allowed on documents using "
        "this expense type. Used only when 'Analytic Account Selection "
        "Method' is set to Domain.",
    )
    analytic_account_python_code = fields.Text(
        string="Analytic Account Python Code",
        default="result = []",
        help="Python snippet evaluated to resolve the analytic accounts "
        "allowed on documents using this expense type; must assign a "
        "list of account.analytic.account ids to the 'result' "
        "variable. Used only when 'Analytic Account Selection Method' "
        "is set to Python Code.",
    )
