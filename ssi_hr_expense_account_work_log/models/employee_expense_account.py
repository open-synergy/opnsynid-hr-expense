# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class EmployeeExpenseAccount(models.Model):
    """
    Extends employee_expense_account to support work log tracking.
    Adds mixin.work_object so that work logs can be recorded
    directly on expense account documents.
    """

    _name = "employee_expense_account"
    _inherit = [
        "employee_expense_account",
        "mixin.work_object",
    ]

    _work_log_create_page = True
