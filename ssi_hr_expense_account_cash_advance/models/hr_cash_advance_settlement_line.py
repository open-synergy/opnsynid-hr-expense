# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrCashAdvanceSettlementLineInherit(models.Model):
    _inherit = "hr.cash_advance_settlement_line"

    require_expense_account = fields.Boolean(
        string="Require Expense Account",
        readonly=False,
    )
    expense_account_id = fields.Many2one(
        comodel_name="employee_expense_account",
        string="Expense Account",
        readonly=True,
    )

    def _check_expense_account(self):
        self.ensure_one()
        result = True
        if self.require_expense_account:
            if not self.expense_account_id:
                error_msg = _("No expense account")
                raise UserError(error_msg)

            if self.expense_account_id.amount_residual < 0.0:
                error_msg = _("Insuficient expense account")
                raise UserError(error_msg)
        return result

    @api.onchange(
        "product_id",
    )
    def onchange_require_expense_account(self):
        result = False

        if self.type_id:
            if self.product_id:
                expense_products = self.search(
                    [
                        ("type_id", "=", self.type_id.id),
                        ("product_id", "=", self.product_id.id),
                    ]
                )
                if len(expense_products) > 0:
                    result = True
                else:
                    ExpTypeProdCateg = self.env["hr.expense_type_product_category"]
                    expense_categories = ExpTypeProdCateg.search(
                        [
                            ("type_id", "=", self.type_id.id),
                            ("categ_id", "=", self.product_id.categ_id.id),
                        ]
                    )
                    if len(expense_categories) > 0:
                        result = True

        self.require_expense_account = result

    @api.onchange("product_id", "account_id", "require_expense_account")
    def onchange_expense_account(self):
        self.expense_account_id = False
        domain = []
        if self.account_id:
            domain = [
                ("employee_id", "=", self.cash_advance_settlement_id.employee_id.id),
                ("state", "=", "open"),
                ("type_id.account_ids", "in", [self.account_id.id]),
                ("date_start", "<=", self.cash_advance_settlement_id.date),
                "|",
                ("date_end", "=", False),
                ("date_end", ">=", self.cash_advance_settlement_id.date),
            ]

            if self.require_expense_account:
                expense_accounts = self.env["employee_expense_account"].search(domain)
                if len(expense_accounts) > 0:
                    self.expense_account_id = expense_accounts[0]
