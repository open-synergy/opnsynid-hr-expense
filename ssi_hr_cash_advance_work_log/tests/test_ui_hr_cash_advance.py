# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrCashAdvance(HttpSavepointCase):
    """Tour tests for the ``hr.cash_advance`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant the group the Cash Advances menu is gated by.

        The menu is already covered by the default membership of
        ``hr_cash_advance_validator_group`` (which implies the viewer
        group), but the grant is repeated explicitly here so the tour
        does not depend on that implication chain.
        """
        super().setUpClass()
        cls.env.ref("ssi_hr_cash_advance.hr_cash_advance_viewer_group").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

    def test_create(self):
        """Run the create tour for ``hr.cash_advance``.

        IK: docs/hr_cash_advance/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_work_log_hr_cash_advance_create",
            login="admin",
        )
