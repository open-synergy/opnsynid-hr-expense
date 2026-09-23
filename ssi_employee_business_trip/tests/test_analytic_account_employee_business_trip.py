# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAnalyticAccountEmployeeBusinessTrip(YamlTransactionCase):
    """Scenario tests for the analytic account m2o configurator.

    Covers ``employee_business_trip_type``'s
    ``analytic_account_selection_method`` (manual/domain/code) and its
    effect on ``employee_business_trip.allowed_analytic_account_ids``,
    including the ``type_id``-empty fallback, an empty manual list, and
    a Python code script that raises (issue
    open-synergy/opnsynid-hr-expense#236).
    """

    def test_analytic_account_employee_business_trip(self):
        """Run the analytic account m2o configurator scenarios."""
        self.run_yaml_scenario("test_data_employee_business_trip_analytic_account.yaml")
