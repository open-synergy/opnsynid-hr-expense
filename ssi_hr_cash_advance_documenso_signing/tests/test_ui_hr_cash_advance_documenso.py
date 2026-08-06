# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrCashAdvanceDocumenso(HttpSavepointCase):
    """Tour test for the ``hr.cash_advance`` Documenso signing delta."""

    @classmethod
    def setUpClass(cls):
        """Create one cash advance already Waiting for Approval.

        ``base.user_admin`` is already a member of
        ``hr_cash_advance_validator_group`` (which implies the ``User``
        and ``Viewer`` groups) via ``ssi_hr_cash_advance``'s
        ``security/res_group_data.xml``, so it can confirm the record
        directly, without extra group setup. The record is moved to
        ``confirm`` here in Python (``action_confirm()``), not via UI
        clicks, and the accounting/master data below is created from
        scratch rather than relying on demo data, per Keputusan Desain
        (issue open-synergy/opnsynid-hr-expense#108).
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        account_type_payable = cls.env.ref("account.data_account_type_payable")
        payable_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Documenso Payable",
                    "code": "TOURCADPAY",
                    "user_type_id": account_type_payable.id,
                    "internal_type": "other",
                    "reconcile": True,
                }
            )
        )
        cash_advance_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Documenso Advance",
                    "code": "TOURCADADV",
                    "user_type_id": account_type_payable.id,
                    "internal_type": "other",
                    "reconcile": True,
                }
            )
        )
        journal = (
            cls.env["account.journal"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Documenso Journal",
                    "code": "TCADJ",
                    "type": "general",
                }
            )
        )
        expense_type = (
            cls.env["hr.expense_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Documenso Type",
                    "code": "TOURCADTYPE",
                }
            )
        )
        employee = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour Cash Advance Documenso Employee Approve"})
        )

        # Pre-Condition IK 05-approve.md (delta): record already Waiting
        # for Approval. The "Standard" approval template used by
        # ssi_hr_cash_advance has no Documenso Signing Template
        # configured, so the Signature Requests tab is present
        # (``_documenso_signing_create_page = True``) but the base
        # Approve/OK Flow is unaffected -- this tour does not exercise
        # it.
        cls.cash_advance_approve = (
            cls.env["hr.cash_advance"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": expense_type.id,
                    "date": "2026-01-01",
                    "date_due": "2026-01-31",
                    "currency_id": cls.env.company.currency_id.id,
                    "journal_id": journal.id,
                    "cash_advance_account_id": cash_advance_account.id,
                    "payable_account_id": payable_account.id,
                }
            )
        )
        cls.cash_advance_approve.action_confirm()

    def test_approve(self):
        """Run the approve tour for the Documenso signing delta.

        IK: docs/hr_cash_advance/05-approve.md (E2a delta -- Modified
        Flow)
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_documenso_signing_hr_cash_advance_approve",
            login="admin",
        )
