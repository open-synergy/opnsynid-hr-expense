# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class HrEmployee(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    employee_advance_payable_account_id = fields.Many2one(
        string="Employee Advance Payable Account",
        comodel_name="account.account",
        domain=[
            ("reconcile", "=", True),
        ],
    )
    employee_advance_account_id = fields.Many2one(
        string="Employee Advance Account",
        comodel_name="account.account",
        domain=[
            ("reconcile", "=", True),
        ],
    )
