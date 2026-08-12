# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, models

from odoo.addons.ssi_decorator import ssi_decorator


class HrReimbursement(models.Model):
    """
    Extends hr.reimbursement to validate expense account linkage.
    Enforces that reimbursement lines requiring an expense account
    have a valid expense account assigned before confirmation.
    """

    _inherit = "hr.reimbursement"

    @ssi_decorator.pre_confirm_action()
    def _check_expense_account(self):
        """Validate expense account linkage before confirmation.

        Runs as a ``pre_confirm_action`` hook: delegates the check to
        every line's ``_check_expense_account``, which raises
        ``UserError`` when a line requires an expense account but
        none is linked, or when the linked account has insufficient
        balance.

        :return: ``True`` when every line passes validation
        """
        self.ensure_one()
        for line in self.line_ids:
            line._check_expense_account()
        return True

    @api.onchange(
        "employee_id",
        "line_ids",
        "line_ids.account_id",
        "line_ids.require_expense_account",
    )
    def onchange_expense_account(self):
        """Resolve ``expense_account_id`` for every reimbursement line.

        Clears each line's ``expense_account_id`` then re-selects a
        matching open ``employee_expense_account`` based on the
        line's ``account_id``, the reimbursement's ``employee_id``,
        and the document's ``date``. A line that requires an expense
        account but has no matching account is left unresolved and
        later fails ``_check_expense_account``, which raises
        ``UserError`` at confirmation.
        """
        for line in self.line_ids:
            line.expense_account_id = False
            domain = []
            if line.account_id:
                domain = [
                    ("employee_id", "=", self.employee_id.id),
                    ("state", "=", "open"),
                    ("type_id.account_ids", "in", [line.account_id.id]),
                    ("date_start", "<=", self.date),
                    "|",
                    ("date_end", "=", False),
                    ("date_end", ">=", self.date),
                ]

                if line.require_expense_account:
                    expense_accounts = self.env["employee_expense_account"].search(
                        domain
                    )
                    if len(expense_accounts) > 0:
                        line.expense_account_id = expense_accounts[0]
