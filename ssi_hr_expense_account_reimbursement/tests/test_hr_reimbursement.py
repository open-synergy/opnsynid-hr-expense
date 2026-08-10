# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrReimbursement(YamlTransactionCase):
    """Cover the ``hr.reimbursement`` onchange extension added by this
    module (issue open-synergy/opnsynid-hr-expense#203).
    """

    def test_hr_reimbursement_onchange_expense_account(self):
        """Run the ``onchange_expense_account`` YAML scenario."""
        self.run_yaml_scenario(
            "test_data_hr_reimbursement_onchange_expense_account.yaml"
        )
