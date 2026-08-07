# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrCashAdvanceSettlement(models.Model):
    """
    Extends hr.cash_advance_settlement with operating unit support.

    Adds ``mixin.single_operating_unit`` so cash advance settlement
    documents can be scoped to a specific operating unit, locks
    ``operating_unit_id`` editability to the draft state, fills it in
    automatically from the linked Cash Advance, and propagates it to
    the accounting entry created on ``action_done``.
    """

    _name = "hr.cash_advance_settlement"
    _inherit = [
        "hr.cash_advance_settlement",
        "mixin.single_operating_unit",
    ]

    operating_unit_id = fields.Many2one(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.onchange(
        "cash_advance_id",
    )
    def onchange_operating_unit_id(self):
        self.operating_unit_id = False
        if self.cash_advance_id:
            self.operating_unit_id = self.cash_advance_id.operating_unit_id

    def _prepare_create_account_move_data(self):
        """Add ``operating_unit_id`` to the created ``account.move``.

        Extends the base ``account.move`` values with the Operating
        Unit of this settlement document, so the journal entry
        created on ``action_done`` carries the same Operating Unit as
        its source document. ``account.move.line`` records are not
        touched here — ``ssi_financial_accounting_operating_unit``
        already copies the Operating Unit from ``move_id`` when the
        lines are created.

        :return: dict of ``account.move`` values
        """
        self.ensure_one()
        res = super()._prepare_create_account_move_data()
        res.update(
            {
                "operating_unit_id": self.operating_unit_id.id,
            }
        )
        return res
