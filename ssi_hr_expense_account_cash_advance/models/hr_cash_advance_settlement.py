# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, models

from odoo.addons.ssi_decorator import ssi_decorator


class HrCashAdvanceSettlement(models.Model):
    """
    Extends hr.cash_advance_settlement to validate expense account linkage.
    Enforces that settlement lines flagged as requiring an expense account
    have a valid expense account assigned before confirmation.
    """

    _inherit = "hr.cash_advance_settlement"

    @ssi_decorator.pre_confirm_action()
    def _check_expense_account(self):
        """Validate expense accounts before confirmation.

        Runs as a pre-confirm check (``action_confirm``): delegates to
        each settlement line's own ``_check_expense_account`` so a
        missing or insufficient expense account blocks confirmation.

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
        """Recompute ``expense_account_id`` for every settlement line.

        Clears ``expense_account_id`` on each line, then searches for
        a matching open ``employee_expense_account`` based on the
        line's ``account_id``, the settlement's ``employee_id``, and
        the settlement ``date`` (the account's validity window must
        cover it). When a line requires an expense account
        (``require_expense_account``) but no matching account is
        found, the field is left empty, so confirmation later fails
        in ``_check_expense_account``.
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
