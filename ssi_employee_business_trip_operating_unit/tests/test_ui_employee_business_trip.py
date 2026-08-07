# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeBusinessTrip(HttpSavepointCase):
    """Tour tests for the ``employee_business_trip`` operating unit delta."""

    @classmethod
    def setUpClass(cls):
        """Grant admin the groups needed to see the Operating Unit field.

        The menu is already covered by the default membership of
        ``employee_business_trip_validator_group`` (which implies the
        viewer group), but the grant is repeated explicitly here so the
        tour does not depend on that implication chain. The multi
        operating unit group is required for the Operating Unit field
        itself to be rendered on the form.
        """
        super().setUpClass()
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_employee_business_trip.employee_business_trip_viewer_group"
        ).sudo().write({"users": [(4, cls.user_admin.id)]})
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.user_admin.id)]}
        )

    def test_field_ou(self):
        """Run the delta tour for the ``employee_business_trip`` create form.

        IK: docs/employee_business_trip/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_operating_unit_employee_business_trip_field_ou",
            login="admin",
        )
