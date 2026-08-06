# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrCashAdvanceSettlement(HttpSavepointCase):
    """Tour tests for the ``hr.cash_advance_settlement`` OU delta."""

    @classmethod
    def setUpClass(cls):
        """Grant admin the groups needed to see the Operating Unit field.

        The menu is already covered by the default membership of
        ``hr_cash_advance_settlement_validator_group`` (which implies
        the viewer group), but the grant is repeated explicitly here
        so the tour does not depend on that implication chain. The
        multi operating unit group is required for the Operating Unit
        field itself to be rendered on the form.
        """
        super().setUpClass()
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_hr_cash_advance.hr_cash_advance_settlement_viewer_group"
        ).sudo().write({"users": [(4, cls.user_admin.id)]})
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.user_admin.id)]}
        )

    def test_field_ou(self):
        """Run the delta tour for the settlement create form.

        IK: docs/hr_cash_advance_settlement/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_operating_unit_hr_cash_advance_settlement_field_ou",
            login="admin",
        )
