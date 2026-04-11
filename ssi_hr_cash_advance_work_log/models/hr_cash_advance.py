# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class HrCashAdvance(models.Model):
    """
    Extends hr.cash_advance to support work log tracking.
    Adds mixin.work_object so that work logs can be recorded
    directly on cash advance documents.
    """

    _name = "hr.cash_advance"
    _inherit = [
        "hr.cash_advance",
        "mixin.work_object",
    ]

    _work_log_create_page = True
