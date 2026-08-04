# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeBusinessTripType(HttpSavepointCase):
    """Tour tests for the ``employee_business_trip_type`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Prepare the group, journal, account, and sequence template.

        Grants the admin user the configurator group the menu is gated
        by, then creates the Journal/Payable Account picked by the tour
        and the ``sequence.template`` the Generate Code inline action
        needs to succeed.
        """
        super().setUpClass()
        # Pre-Condition: the "Business Trip Types" menu is gated by the
        # configurator group. Without it the tour dies on its first
        # step because the menu is never rendered.
        cls.env.ref(
            "ssi_employee_business_trip.employee_business_trip_type_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Tour Business Trip Journal",
                "code": "TOURJ",
                "type": "general",
            }
        )
        cls.payable_account = cls.env["account.account"].create(
            {
                "name": "Tour Business Trip Payable",
                "code": "TOURBTT",
                "user_type_id": cls.env.ref("account.data_account_type_payable").id,
            }
        )
        # Config: a sequence.template for this model is what makes the
        # Generate Code inline action (docs/employee_business_trip_type/
        # 01-create.md, step 8) succeed instead of raising UserError.
        cls.sequence = cls.env["ir.sequence"].create(
            {
                "name": "Tour Business Trip Type Sequence",
                "code": "tour.employee.business.trip.type",
                "prefix": "TOURTYPE",
                "padding": 4,
            }
        )
        sequence_field = cls.env["ir.model.fields"].search(
            [
                ("model", "=", "employee_business_trip_type"),
                ("name", "=", "code"),
            ],
            limit=1,
        )
        date_field = cls.env["ir.model.fields"].search(
            [
                ("model", "=", "employee_business_trip_type"),
                ("name", "=", "write_date"),
            ],
            limit=1,
        )
        cls.env["sequence.template"].create(
            {
                "name": "Tour Business Trip Type Sequence Template",
                "model_id": cls.env["ir.model"]._get("employee_business_trip_type").id,
                "sequence_field_id": sequence_field.id,
                "date_field_id": date_field.id,
                "computation_method": "use_domain",
                "domain": "[]",
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.sequence.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``employee_business_trip_type``.

        IK: docs/employee_business_trip_type/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_type_create",
            login="admin",
        )
