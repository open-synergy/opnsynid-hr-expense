# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrExpenseType(HttpSavepointCase):
    """Tour tests for the ``hr.expense_type`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant menu access and prepare fixtures for every tour.

        Pre-Conditions shared by all ``docs/hr_expense_type/*.md`` work
        instructions are prepared here, not by clicking through the UI:

        * The **Types** menu is gated by the *Expense Type* group.
          Without it every tour dies on its first step.
        * The **Generate Code** inline action requires an active
          ``sequence.template`` for ``hr.expense_type``; without one
          it raises an error instead of assigning a code.
        * The edit, delete, deactivate, and activate tours each need a
          pre-existing record to open, so one fixture is created per
          tour instead of relying on ``test_create``'s own record.
        """
        super().setUpClass()
        cls.env.ref("ssi_hr_expense.hr_expense_type_group").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )
        sequence = cls.env["ir.sequence"].create(
            {
                "name": "Tour Expense Type Sequence",
                "code": "tour.ssi_hr_expense.hr_expense_type",
                "prefix": "TOUREXP",
                "padding": 3,
            }
        )
        model = cls.env["ir.model"].search([("model", "=", "hr.expense_type")], limit=1)
        code_field = cls.env["ir.model.fields"].search(
            [("model", "=", "hr.expense_type"), ("name", "=", "code")],
            limit=1,
        )
        date_field = cls.env["ir.model.fields"].search(
            [
                ("model", "=", "hr.expense_type"),
                ("name", "=", "create_date"),
            ],
            limit=1,
        )
        cls.env["sequence.template"].create(
            {
                "name": "Tour Expense Type Sequence Template",
                "model_id": model.id,
                "sequence_field_id": code_field.id,
                "date_field_id": date_field.id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": sequence.id,
            }
        )
        cls.env["hr.expense_type"].create(
            {"name": "TOUR-EDIT-EXPENSE-TYPE", "code": "/"}
        )
        cls.env["hr.expense_type"].create(
            {"name": "TOUR-DELETE-EXPENSE-TYPE", "code": "TOURDEL001"}
        )
        cls.env["hr.expense_type"].create(
            {"name": "TOUR-DEACTIVATE-EXPENSE-TYPE", "code": "TOURDEA001"}
        )
        cls.env["hr.expense_type"].create(
            {
                "name": "TOUR-ACTIVATE-EXPENSE-TYPE",
                "code": "TOURACT001",
                "active": False,
            }
        )

    def test_create(self):
        """Run the create tour for ``hr.expense_type``.

        IK: docs/hr_expense_type/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_hr_expense_type_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.expense_type``.

        IK: docs/hr_expense_type/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_hr_expense_type_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``hr.expense_type``.

        IK: docs/hr_expense_type/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_hr_expense_type_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``hr.expense_type``.

        IK: docs/hr_expense_type/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_hr_expense_type_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``hr.expense_type``.

        IK: docs/hr_expense_type/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_hr_expense_type_activate",
            login="admin",
        )
