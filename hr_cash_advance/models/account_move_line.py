# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"

    cash_advance_payable_id = fields.Many2one(
        string="Cash Advance Payable",
        comodel_name="hr.cash_advance",
        readonly=True,
    )
    cash_advance_id = fields.Many2one(
        string="Cash Advance",
        comodel_name="hr.cash_advance",
        readonly=True,
    )
