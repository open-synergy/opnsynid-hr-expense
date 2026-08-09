# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EmployeeExpenseAccount(models.Model):
    """
    Extends employee_expense_account to track linked cash advance
    settlement lines. Computes the total cash advance amount that
    has been applied against this expense account.
    """

    _inherit = "employee_expense_account"

    cash_advance_settlement_line_ids = fields.One2many(
        comodel_name="hr.cash_advance_settlement_line",
        inverse_name="expense_account_id",
        string="All Cash Advance Settlement",
    )

    @api.depends(
        "cash_advance_settlement_line_ids",
        "cash_advance_settlement_line_ids.cash_advance_settlement_id",
        "cash_advance_settlement_line_ids.cash_advance_settlement_id.state",
    )
    def _compute_valid_cash_advance_settlement_line_ids(self):
        """Filter out cash advance settlement lines in dead-end states.

        Excludes lines whose settlement is ``reject``, ``cancel``, or
        ``terminate``, leaving only the lines still relevant to this
        expense account.
        """
        for record in self:
            result = record.cash_advance_settlement_line_ids.filtered(
                lambda x: x.cash_advance_settlement_id.state
                not in ("reject", "cancel", "terminate")
            )
            record.valid_cash_advance_settlement_line_ids = result

    valid_cash_advance_settlement_line_ids = fields.One2many(
        string="Cash Advance Settlement",
        comodel_name="hr.cash_advance_settlement_line",
        compute="_compute_valid_cash_advance_settlement_line_ids",
        compute_sudo=True,
    )

    @api.depends(
        "cash_advance_settlement_line_ids",
        "cash_advance_settlement_line_ids.price_subtotal",
        "cash_advance_settlement_line_ids.cash_advance_settlement_id.state",
    )
    def _compute_cash_advance(self):
        """Sum settled cash advance amounts applied to this account.

        Adds ``price_subtotal`` of every settlement line whose settlement
        is not ``terminate``/``cancel``, then triggers
        ``_compute_amount`` to refresh the account totals accordingly.
        """
        for record in self:
            result = 0.0
            for line in record.cash_advance_settlement_line_ids.filtered(
                lambda x: x.cash_advance_settlement_id.state
                not in ("terminate", "cancel")
            ):
                result += line.price_subtotal
            record.amount_cash_advance = result
            record._compute_amount()

    amount_cash_advance = fields.Monetary(
        compute="_compute_cash_advance",
        store=True,
        string="Cash Advance",
        compute_sudo=True,
    )

    def _get_expense_fields(self):
        """Extend the expense field list with ``amount_cash_advance``.

        Overridden so ``amount_cash_advance`` is included wherever the
        base expense account totals are aggregated or displayed.

        :return: list of field names
        """
        _super = super(EmployeeExpenseAccount, self)
        res = _super._get_expense_fields()
        res.append("amount_cash_advance")
        return res
