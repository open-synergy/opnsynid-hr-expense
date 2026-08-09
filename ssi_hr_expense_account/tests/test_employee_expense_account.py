# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEmployeeExpenseAccount(YamlTransactionCase):
    """Cover ``employee_expense_account`` CRUD, compute, and negative path."""

    def test_employee_expense_account(self):
        """Run the CRUD, form, and negative path YAML scenario."""
        self.run_yaml_scenario("test_data_employee_expense_account.yaml")
