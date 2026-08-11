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
        by, then creates the Journal/Payable Account picked by the
        create/edit tours, the ``sequence.template`` the Generate Code
        inline action needs to succeed, and one fixture record per
        delete/deactivate/activate tour.
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
                # Payable/receivable account types must be reconcilable, or
                # Odoo core rejects the record with a ValidationError.
                "reconcile": True,
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

        # Fixture for the edit tour -- a record whose Name the tour
        # changes to a distinct value (odoo-development-ui-test,
        # patterns.md §L).
        cls.type_edit = cls.env["employee_business_trip_type"].create(
            {
                "name": "Tour EBT Type Edit",
                "code": "TOUREBTTYPEEDIT",
                "journal_id": cls.journal.id,
                "payable_account_id": cls.payable_account.id,
            }
        )

        # Fixture for the delete tour -- Pre-Condition: not referenced
        # by any Employee Business Trip record. This record is never
        # picked as Type anywhere, so it always qualifies.
        cls.type_delete = cls.env["employee_business_trip_type"].create(
            {
                "name": "Tour EBT Type Delete",
                "code": "TOUREBTTYPEDEL",
                "journal_id": cls.journal.id,
                "payable_account_id": cls.payable_account.id,
            }
        )

        # Fixture for the deactivate tour -- Pre-Condition: active
        # (``mixin.master_data`` default).
        cls.type_deactivate = cls.env["employee_business_trip_type"].create(
            {
                "name": "Tour EBT Type Deactivate",
                "code": "TOUREBTTYPEDEACT",
                "journal_id": cls.journal.id,
                "payable_account_id": cls.payable_account.id,
            }
        )

        # Fixture for the activate tour -- Pre-Condition: archived,
        # reached in Python by writing ``active=False`` directly rather
        # than through the deactivate tour's own UI flow.
        cls.type_activate = cls.env["employee_business_trip_type"].create(
            {
                "name": "Tour EBT Type Activate",
                "code": "TOUREBTTYPEACT",
                "journal_id": cls.journal.id,
                "payable_account_id": cls.payable_account.id,
            }
        )
        cls.type_activate.write({"active": False})

    def test_create(self):
        """Run the create tour for ``employee_business_trip_type``.

        IK: docs/employee_business_trip_type/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_type_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``employee_business_trip_type``.

        IK: docs/employee_business_trip_type/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_type_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``employee_business_trip_type``.

        IK: docs/employee_business_trip_type/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_type_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``employee_business_trip_type``.

        IK: docs/employee_business_trip_type/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_type_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``employee_business_trip_type``.

        IK: docs/employee_business_trip_type/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_type_activate",
            login="admin",
        )
