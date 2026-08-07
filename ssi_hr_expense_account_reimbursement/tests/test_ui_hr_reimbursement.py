# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrReimbursement(HttpSavepointCase):
    """Tour tests for the Expense Account delta on reimbursement lines."""

    @classmethod
    def setUpClass(cls):
        """Grant the group the Reimbursements menu is gated by.

        The menu is already covered by the default membership of
        ``hr_reimbursement_validator_group`` (which implies the
        viewer group), but the grant is repeated explicitly here so
        the tour does not depend on that implication chain, built
        from scratch with ``sudo()`` and without relying on demo
        data. No stored reimbursement record is created: the tour
        never Saves, so menu access is the only Pre-Condition worth
        preparing.
        """
        super().setUpClass()
        cls.env.ref("ssi_hr_reimbursement.hr_reimbursement_viewer_group").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

    def test_create(self):
        """Run the Expense Account delta tour for the reimbursement line.

        IK: docs/hr_reimbursement/01-create.md

        The tour stops right after asserting the Expense Account tab
        and its Required / # Expense Account field labels are
        rendered in the line dialog -- it does not fill any field,
        does not Save, and does not continue to the confirm action.
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_reimbursement_hr_reimbursement_create",
            login="admin",
        )
