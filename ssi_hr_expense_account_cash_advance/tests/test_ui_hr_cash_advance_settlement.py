# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrCashAdvanceSettlement(HttpSavepointCase):
    """Tour tests for the Expense Account delta on settlement lines."""

    @classmethod
    def setUpClass(cls):
        """Grant the group the Cash Advance Settlements menu is gated by.

        The menu is already covered by the default membership of
        ``hr_cash_advance_settlement_validator_group`` (which implies
        the viewer group), but the grant is repeated explicitly here
        so the tour does not depend on that implication chain. No
        stored settlement record is created: the tour never Saves, so
        only the menu access is a Pre-Condition worth preparing.
        """
        super().setUpClass()
        cls.env.ref(
            "ssi_hr_cash_advance.hr_cash_advance_settlement_viewer_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})

    def test_create(self):
        """Run the Expense Account delta tour for the settlement line.

        IK: docs/hr_cash_advance_settlement/01-create.md

        The tour stops right after asserting the Require Expense
        Account / Expense Account columns and the Expense Account tab
        are rendered -- it does not fill any field, does not Save,
        and does not continue to the confirm action.
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_cash_advance_hr_cash_advance_settlement_create",
            login="admin",
        )
