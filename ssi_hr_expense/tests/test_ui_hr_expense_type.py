# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrExpenseType(HttpCase):
    """Tour tests for the ``hr.expense_type`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant menu access and configure the code sequence.

        Two Pre-Conditions of ``docs/hr_expense_type/01-create.md`` are
        prepared here, not by clicking through the UI:

        * The **Types** menu is gated by the *Expense Type* group.
          Without it the tour dies on its first step.
        * The **Generate Code** inline action requires an active
          ``sequence.template`` for ``hr.expense_type``; without one
          it raises an error instead of assigning a code.
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

    def test_create(self):
        """Run the create tour for ``hr.expense_type``.

        IK: docs/hr_expense_type/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_hr_expense_type_create",
            login="admin",
        )
