# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EmployeeExpenseAccountInherit(models.Model):
    _name = "employee_expense_account"
    _inherit = ["employee_expense_account"]
    _description = "Employee Expense Account Inherit"

    cash_advance_settlement_line_ids = fields.One2many(
        comodel_name="hr.cash_advance_settlement_line",
        inverse_name="expense_account_id",
        domain="[('cash_advance_settlement_id.state', 'not in', 'cancel')]",
        string="Cash Advance Settlement Lines",
    )
    amount_cash_advance = fields.Monetary(
        currency_field="currency_id",
        compute="_compute_cash_advance",
        store=True,
        string="Amount Cash Advance",
    )
