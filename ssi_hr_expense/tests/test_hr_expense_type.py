# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrExpenseType(YamlTransactionCase):
    """Cover the ``hr.expense_type`` compute methods (issue
    open-synergy/opnsynid-hr-expense#204).
    """

    def test_hr_expense_type_compute(self):
        """Run the ``hr.expense_type`` allowed product/category scenario."""
        self.run_yaml_scenario("test_data_hr_expense_type_compute.yaml")
