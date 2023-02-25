# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EmployeeExpenseAccountTypeField(models.Model):
    _name = "employee_expense_account_type.field"
    _description = "Employee Expense Account Type Field"
    _order = "type_id, sequence, id"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="employee_expense_account_type",
        ondelete="cascade",
        required=True,
    )
    sequence = fields.Integer(string="Sequence", required=True, default=10)
    field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Field",
        domain="[('model', '=', 'employee_expense_account'), ('ttype', '=', 'monetary')]",
    )
