# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeExpenseAccount(HttpSavepointCase):
    """Tour tests for the ``employee_expense_account`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant the group the Expense Accounts menu is gated by.

        The menu is already covered by the default membership of
        ``employee_expense_account_validator_group`` (which implies the
        viewer group), but the grant is repeated explicitly here so the
        tour does not depend on that implication chain.
        """
        super().setUpClass()
        cls.env.ref(
            "ssi_hr_expense_account.employee_expense_account_viewer_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})

    def test_create(self):
        """Run the create tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_work_log_employee_expense_account_create",
            login="admin",
        )
