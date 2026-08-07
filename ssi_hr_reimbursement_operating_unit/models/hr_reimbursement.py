# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrReimbursement(models.Model):
    """
    Extends ``hr.reimbursement`` with Operating Unit support.

    ``operating_unit_id`` itself comes from ``mixin.single_operating_unit``
    (default: the creating user's default operating unit); this override
    only locks its editability to the draft state and propagates it to the
    accounting entry created on ``action_open``
    (``_prepare_account_move_data()``). Journal items are not touched here:
    ``ssi_financial_accounting_operating_unit`` already copies the
    Operating Unit from ``move_id`` inside ``account.move.line.create()``,
    and both the payable line and every detail expense line are created
    with ``move_id`` already set.
    """

    _name = "hr.reimbursement"
    _inherit = [
        "hr.reimbursement",
        "mixin.single_operating_unit",
    ]

    operating_unit_id = fields.Many2one(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    def _prepare_account_move_data(self):
        """Add ``operating_unit_id`` to the accounting entry values.

        :return: values used to create the ``account.move`` for this
            reimbursement.
        :rtype: dict
        """
        self.ensure_one()
        res = super()._prepare_account_move_data()
        res.update(
            {
                "operating_unit_id": self.operating_unit_id.id,
            }
        )
        return res
