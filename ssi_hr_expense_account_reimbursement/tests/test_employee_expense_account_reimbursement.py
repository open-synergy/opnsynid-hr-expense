# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEmployeeExpenseAccountReimbursement(YamlTransactionCase):
    """Cover the ``employee_expense_account`` compute extensions added by
    this module (issue open-synergy/opnsynid-hr-expense#203).
    """

    def test_employee_expense_account_reimbursement_compute(self):
        """Run the reimbursement compute YAML scenario.

        Covers ``_compute_reimbursement`` and
        ``_compute_valid_reimbursement_line_ids``.
        """
        self.run_yaml_scenario(
            "test_data_employee_expense_account_reimbursement_compute.yaml"
        )
