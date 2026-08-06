# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrReimbursementDocumenso(HttpSavepointCase):
    """Tour test for the ``hr.reimbursement`` Documenso signing delta."""

    @classmethod
    def setUpClass(cls):
        """Create one reimbursement already Waiting for Approval.

        ``base.user_admin`` is already a member of
        ``hr_reimbursement_validator_group`` (which implies the ``User``
        and ``Viewer`` groups) via ``ssi_hr_reimbursement``'s
        ``security/res_group_data.xml``, so it can confirm the record
        directly, without extra group setup. The record is moved to
        ``confirm`` here in Python (``action_confirm()``), not via UI
        clicks, and the accounting/master data below is created from
        scratch rather than relying on demo data, per Keputusan Desain
        (issue open-synergy/opnsynid-hr-expense#113).
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        account_type_payable = cls.env.ref("account.data_account_type_payable")
        account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Reimbursement Documenso Account",
                    "code": "TOURRMBACC",
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
                    "name": "Tour Reimbursement Documenso Journal",
                    "code": "TRMBJ",
                    "type": "general",
                }
            )
        )
        expense_type = (
            cls.env["hr.expense_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Reimbursement Documenso Type",
                    "code": "TOURRMBTYPE",
                }
            )
        )
        employee = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour Reimbursement Documenso Employee Approve"})
        )

        # Pre-Condition IK 05-approve.md (delta): record already Waiting
        # for Approval. The "Standard" approval template used by
        # ssi_hr_reimbursement has no Documenso Signing Template
        # configured, so the Signature Requests tab is present
        # (``_documenso_signing_create_page = True``) but the base
        # Approve/OK Flow is unaffected -- this tour does not exercise
        # it.
        cls.reimbursement_approve = (
            cls.env["hr.reimbursement"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": expense_type.id,
                    "date": "2026-01-01",
                    "date_due": "2026-01-31",
                    "currency_id": cls.env.company.currency_id.id,
                    "journal_id": journal.id,
                    "account_id": account.id,
                }
            )
        )
        cls.reimbursement_approve.action_confirm()

    def test_approve(self):
        """Run the approve tour for the Documenso signing delta.

        IK: docs/hr_reimbursement/05-approve.md (E2a delta -- Modified
        Flow)
        """
        self.start_tour(
            "/web",
            "ssi_hr_reimbursement_documenso_signing_hr_reimbursement_approve",
            login="admin",
        )
