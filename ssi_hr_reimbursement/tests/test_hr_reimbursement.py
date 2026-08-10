# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrReimbursement(YamlTransactionCase):
    """Cover ``hr.reimbursement`` form rendering, onchange, and action
    method state transitions (issue open-synergy/opnsynid-hr-expense#200).
    """

    def test_hr_reimbursement(self):
        """Run the form and negative path YAML scenario."""
        self.run_yaml_scenario("test_data_hr_reimbursement.yaml")

    def test_hr_reimbursement_onchange(self):
        """Run the ``hr.reimbursement`` onchange coverage scenario."""
        self.run_yaml_scenario("test_data_hr_reimbursement_onchange.yaml")

    def test_hr_reimbursement_action(self):
        """Run the ``hr.reimbursement`` action method scenario.

        Covers ``action_open``, ``action_cancel`` (through the
        select-reason wizard), and ``action_recompute_realization``.
        """
        self.run_yaml_scenario("test_data_hr_reimbursement_action.yaml")
