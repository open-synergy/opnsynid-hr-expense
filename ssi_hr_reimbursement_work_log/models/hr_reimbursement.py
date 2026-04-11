# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class HrReimbursement(models.Model):
    """
    Extends hr.reimbursement to support work log tracking.
    Adds mixin.work_object so that work logs can be recorded
    directly on reimbursement documents.
    """

    _name = "hr.reimbursement"
    _inherit = [
        "hr.reimbursement",
        "mixin.work_object",
    ]

    _work_log_create_page = True
