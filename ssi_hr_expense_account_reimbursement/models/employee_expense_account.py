# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class EmployeeExpenseAccount(models.Model):
    _inherit = "employee_expense_account"

    reimbursement_line_ids = fields.One2many(
        comodel_name="hr.reimbursement_line",
        inverse_name="expense_account_id",
        domain="[('reimbursement_id.state', 'not in', ['terminate', 'cancel'])]",
        string="Reimbursements",
    )

    @api.depends(
        "reimbursement_line_ids",
        "reimbursement_line_ids.price_subtotal",
        "reimbursement_line_ids.reimbursement_id.state",
    )
    def _compute_reimbursement(self):
        for record in self:
            result = 0.0
            for line in record.reimbursement_line_ids.filtered(
                lambda x: x.reimbursement_id.state == "open"
            ):
                result += line.price_subtotal
            record.amount_reimbursement = result
            record._compute_amount()

    amount_reimbursement = fields.Monetary(
        compute="_compute_reimbursement",
        store=True,
        string="Amount Reimbursement",
    )

    def _get_expense_fields(self):
        _super = super(EmployeeExpenseAccount, self)
        res = _super._get_expense_fields()
        res.append("amount_reimbursement")
        return res
