# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEmployeeExpenseAccount(YamlTransactionCase):
    """Cover the ``employee_expense_account`` compute extensions added by
    this module (issue open-synergy/opnsynid-hr-expense#202).
    """

    def test_employee_expense_account_compute(self):
        """Run the cash advance compute YAML scenario.

        Covers ``_compute_cash_advance`` and
        ``_compute_valid_cash_advance_settlement_line_ids``.
        """
        self.run_yaml_scenario("test_data_employee_expense_account_compute.yaml")
