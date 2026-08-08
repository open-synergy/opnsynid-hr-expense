# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEmployeeBusinessTrip(YamlTransactionCase):
    """Scenario tests for the ``employee_business_trip`` Done auto-skip.

    Covers the fix for issue open-synergy/opnsynid-hr-expense#149:
    ``_10_skip_open`` must bypass the policy check when it pushes a
    trip without a Per Diem line straight to Done, and must leave a
    trip with a Per Diem line at Open (regression from issue #132).
    """

    def test_employee_business_trip(self):
        """Run the Done auto-skip and Per Diem regression scenarios."""
        self.run_yaml_scenario("test_data_employee_business_trip.yaml")
