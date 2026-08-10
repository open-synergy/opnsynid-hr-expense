# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrReimbursementLine(YamlTransactionCase):
    """Cover the ``hr.reimbursement_line`` onchange methods (issue
    open-synergy/opnsynid-hr-expense#200).
    """

    def test_hr_reimbursement_line_onchange(self):
        """Run the ``hr.reimbursement_line`` onchange coverage scenario."""
        self.run_yaml_scenario("test_data_hr_reimbursement_line_onchange.yaml")
