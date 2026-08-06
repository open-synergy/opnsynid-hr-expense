# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeExpenseAccountDocumenso(HttpSavepointCase):
    """Tour test for the ``employee_expense_account`` Documenso delta."""

    @classmethod
    def setUpClass(cls):
        """Create one expense account already Waiting for Approval.

        ``base.user_admin`` is already a member of
        ``employee_expense_account_validator_group`` (which implies the
        ``User`` group, which implies the ``Viewer`` group) via
        ``ssi_hr_expense_account``'s ``security/res_group_data.xml``, so it
        can confirm the record directly, without extra group setup. The
        viewer grant is repeated explicitly below so the tour does not
        depend on that implication chain. The record is moved to
        ``confirm`` here in Python (``action_confirm()``), not via UI
        clicks, and the master data below is created from scratch rather
        than relying on demo data, per Keputusan Desain (issue
        open-synergy/opnsynid-hr-expense#111).
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_hr_expense_account.employee_expense_account_viewer_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

        expense_type = (
            cls.env["employee_expense_account_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EEA Documenso Expense Type",
                    "code": "TOUREEADTYPE",
                }
            )
        )
        employee = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour EEA Documenso Employee Approve"})
        )

        # Pre-Condition IK 05-approve.md (delta): record already Waiting
        # for Approval. The "Standard" approval template used by
        # ssi_hr_expense_account demo data has no Documenso Signing
        # Template configured, so the Signature Requests tab is present
        # (``_documenso_signing_create_page = True``) but the base
        # Approve/OK Flow is unaffected -- this tour does not exercise it.
        cls.expense_account_approve = (
            cls.env["employee_expense_account"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": expense_type.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-01-31",
                    "currency_id": cls.env.company.currency_id.id,
                    "amount_limit": 1000000.0,
                }
            )
        )
        cls.expense_account_approve.action_confirm()

    def test_approve(self):
        """Run the approve tour for the Documenso signing delta.

        IK: docs/employee_expense_account/05-approve.md (E2a delta --
        Modified Flow)
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_documenso_signing_employee_expense_account_approve",
            login="admin",
        )
