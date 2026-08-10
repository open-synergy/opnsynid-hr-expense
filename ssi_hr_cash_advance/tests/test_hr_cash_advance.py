# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrCashAdvance(YamlTransactionCase):
    """Cover the ``hr.cash_advance`` search filters, onchange, and
    action methods (issue open-synergy/opnsynid-hr-expense#199).
    """

    def test_hr_cash_advance(self):
        """Run the cash advance and settlement YAML scenario."""
        self.run_yaml_scenario("test_data_hr_cash_advance.yaml")

    def test_hr_cash_advance_onchange(self):
        """Run the ``hr.cash_advance`` onchange coverage scenario."""
        self.run_yaml_scenario("test_data_hr_cash_advance_onchange.yaml")

    def test_hr_cash_advance_action(self):
        """Run the ``hr.cash_advance`` action method scenario.

        Covers ``action_open``, ``action_cancel`` (through the
        select-reason wizard), and ``action_recompute_realization``.
        """
        self.run_yaml_scenario("test_data_hr_cash_advance_action.yaml")
