# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrReimbursementStatusCheck(YamlTransactionCase):
    """Cover the status check and state change constrain mixins on
    ``hr.reimbursement`` (issue open-synergy/opnsynid-hr-expense#296).
    """

    def test_hr_reimbursement_status_check(self):
        """Run the status check template selection and constrain scenario.

        Covers template selection on ``create`` and on the ``type_id``
        onchange, plus the ``UserError`` raised on confirm when a required
        status check item fails and the passing counterpart.
        """
        self.run_yaml_scenario("test_data_hr_reimbursement_status_check.yaml")
