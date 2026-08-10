# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrCashAdvanceLine(YamlTransactionCase):
    """Cover the ``hr.cash_advance_line`` onchange methods (issue
    open-synergy/opnsynid-hr-expense#199).
    """

    def test_hr_cash_advance_line_onchange(self):
        """Run the ``hr.cash_advance_line`` onchange coverage scenario."""
        self.run_yaml_scenario("test_data_hr_cash_advance_line_onchange.yaml")
