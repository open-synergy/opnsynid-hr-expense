# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    reimbursement_id = fields.Many2one(
        string="Reimbursement",
        comodel_name="hr.reimbursement",
        readonly=True,
    )
