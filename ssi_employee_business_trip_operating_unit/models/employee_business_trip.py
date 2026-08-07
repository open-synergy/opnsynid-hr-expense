# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EmployeeBusinessTrip(models.Model):
    """
    Extends ``employee_business_trip`` with Operating Unit support.

    ``operating_unit_id`` itself comes from
    ``mixin.single_operating_unit`` (default: the creating user's
    default operating unit); this override only locks its
    editability to the draft state and propagates it to the
    accounting entry created on ``action_open``
    (``_prepare_standard_move()``). Journal items are not touched
    here: ``ssi_financial_accounting_operating_unit`` already copies
    the Operating Unit from ``move_id`` inside
    ``account.move.line.create()``, and the payable line, every
    per-diem line, and every tax line are all created with
    ``move_id`` already set.
    """

    _name = "employee_business_trip"
    _inherit = [
        "employee_business_trip",
        "mixin.single_operating_unit",
    ]

    operating_unit_id = fields.Many2one(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    def _prepare_standard_move(self):
        """Add ``operating_unit_id`` to the accounting entry values.

        :return: values used to create the ``account.move`` for this
            business trip.
        :rtype: dict
        """
        self.ensure_one()
        res = super()._prepare_standard_move()
        res.update(
            {
                "operating_unit_id": self.operating_unit_id.id,
            }
        )
        return res
