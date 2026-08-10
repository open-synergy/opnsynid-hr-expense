# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestOnchangeEmployeeBusinessTrip(YamlTransactionCase):
    """Scenario tests for ``employee_business_trip`` onchange handlers.

    Covers ``onchange_journal_id`` and ``onchange_payable_account_id``,
    both triggered by changing ``type_id`` on the trip form: a positive
    scenario where selecting a Type fills Journal/Payable Account, and
    a negative scenario where clearing the Type resets them.
    """

    def test_onchange_employee_business_trip(self):
        """Run the ``type_id`` onchange scenarios via the Form API."""
        self.run_yaml_scenario("test_data_employee_business_trip_onchange.yaml")
