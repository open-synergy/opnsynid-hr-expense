# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openerp import models

from odoo.addons.ssi_decorator import ssi_decorator


class HrReimbursement(models.Model):
    _inherit = "hr.reimbursement"

    @ssi_decorator.pre_confirm_action()
    def _check_expense_account(self):
        self.ensure_one()
        for line in self.line_ids:
            line._check_expense_account()

        return True
