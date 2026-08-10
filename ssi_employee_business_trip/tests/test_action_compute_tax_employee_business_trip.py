# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestActionComputeTaxEmployeeBusinessTrip(YamlTransactionCase):
    """Scenario tests for ``employee_business_trip.action_compute_tax``.

    Covers recomputation of ``tax_ids`` from the taxes set on the
    trip's Per Diem lines, and that calling the action again does not
    duplicate the recomputed tax lines.
    """

    def test_action_compute_tax_employee_business_trip(self):
        """Run the ``action_compute_tax`` recompute scenario."""
        self.run_yaml_scenario(
            "test_data_employee_business_trip_action_compute_tax.yaml"
        )
