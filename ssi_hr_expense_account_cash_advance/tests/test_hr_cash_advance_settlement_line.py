# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrCashAdvanceSettlementLine(YamlTransactionCase):
    """Cover the ``hr.cash_advance_settlement_line`` onchange extension
    added by this module (issue open-synergy/opnsynid-hr-expense#202).
    """

    def test_hr_cash_advance_settlement_line_onchange_require_expense_account(
        self,
    ):
        """Run the ``onchange_require_expense_account`` YAML scenario."""
        self.run_yaml_scenario(
            "test_data_hr_cash_advance_settlement_line_onchange.yaml"
        )
