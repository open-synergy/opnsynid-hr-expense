# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeBusinessTrip(HttpSavepointCase):
    """Tour tests for the ``employee_business_trip`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant groups and create records the Work Log tour needs.

        The Business Trips menu is already covered by the default
        membership of ``employee_business_trip_validator_group`` (which
        implies the viewer group), but the grant is repeated explicitly
        here so the tour does not depend on that implication chain.

        An analytic account is created for the tour to pick in the
        **Work Log Analytic Account** field (IK Flow step 4) — this is
        Pre-Condition data, not the focus of the tour itself.
        """
        super().setUpClass()
        cls.env.ref(
            "ssi_employee_business_trip.employee_business_trip_viewer_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {"name": "TOUR Work Log Analytic Account"}
        )

    def test_create(self):
        """Run the create tour for ``employee_business_trip``.

        IK: docs/employee_business_trip/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_work_log_employee_business_trip_create",
            login="admin",
        )
