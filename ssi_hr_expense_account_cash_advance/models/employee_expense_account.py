# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EmployeeExpenseAccountInherit(models.Model):
    _name = "employee_expense_account"
    _inherit = ["employee_expense_account"]
    _description = "Employee Expense Account Inherit"

    reimbursement_line_ids = fields.One2many(
        comodel_name="hr.reimbursement_line",
        inverse_name="expense_account_id",
        domain=[("reimbursement_id.state", "not in", ("terminate", "cancel"))],
        string="Reimbursements",
    )
    amount_reimbursement = fields.Monetary(
        currency_field="currency_id",
        compute="_compute_reimbursement",
        store=True,
        string="Amount Reimbursement",
    )
