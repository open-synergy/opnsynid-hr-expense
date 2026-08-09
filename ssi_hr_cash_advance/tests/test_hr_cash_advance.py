# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrCashAdvance(YamlTransactionCase):
    """Cover the ``hr.cash_advance`` and settlement workflows."""

    def test_hr_cash_advance(self):
        """Run the cash advance and settlement YAML scenario."""
        self.run_yaml_scenario("test_data_hr_cash_advance.yaml")
