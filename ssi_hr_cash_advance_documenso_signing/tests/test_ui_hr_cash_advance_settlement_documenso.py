# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrCashAdvanceSettlementDocumenso(HttpSavepointCase):
    """Tour test for the ``hr.cash_advance_settlement`` Documenso delta."""

    @classmethod
    def setUpClass(cls):
        """Create one settlement already Waiting for Approval.

        ``base.user_admin`` is already a member of
        ``hr_cash_advance_validator_group`` and
        ``hr_cash_advance_settlement_validator_group`` (each implying its
        own ``User``/``Viewer`` groups) via ``ssi_hr_cash_advance``'s
        ``security/res_group_data.xml``, so it can confirm/approve
        directly, without extra group setup. A cash advance is first
        driven to **Open** status (required by ``cash_advance_id``, a
        mandatory field on the settlement) via ``action_confirm()`` then
        ``action_approve_approval()``; its "Standard" approval template
        has no Documenso Signing Template configured, so this step is
        unaffected by this module. The settlement itself is then moved to
        ``confirm`` -- this is the record under test. All state
        transitions are driven in Python, not via UI clicks, and the
        accounting/master data below is created from scratch rather than
        relying on demo data, per Keputusan Desain (issue
        open-synergy/opnsynid-hr-expense#108).
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        account_type_payable = cls.env.ref("account.data_account_type_payable")
        payable_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Settlement Documenso Payable",
                    "code": "TOURCASPAY",
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
                    "name": "Tour Cash Advance Settlement Documenso Advance",
                    "code": "TOURCASADV",
                    "user_type_id": account_type_payable.id,
                    "internal_type": "other",
                    "reconcile": True,
                }
            )
        )
        ca_journal = (
            cls.env["account.journal"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Settlement Documenso CA Journal",
                    "code": "TCASCAJ",
                    "type": "general",
                }
            )
        )
        settlement_journal = (
            cls.env["account.journal"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Settlement Documenso Journal",
                    "code": "TCASJ",
                    "type": "general",
                }
            )
        )
        expense_type = (
            cls.env["hr.expense_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Settlement Documenso Type",
                    "code": "TOURCASTYPE",
                }
            )
        )
        employee = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour Cash Advance Settlement Documenso Employee Approve"})
        )

        # Helper fixture: a cash advance already Open, referenced by the
        # settlement below via the required `cash_advance_id` field. Not
        # itself the record under test.
        cash_advance = (
            cls.env["hr.cash_advance"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": expense_type.id,
                    "date": "2026-01-01",
                    "date_due": "2026-01-31",
                    "currency_id": cls.env.company.currency_id.id,
                    "journal_id": ca_journal.id,
                    "cash_advance_account_id": cash_advance_account.id,
                    "payable_account_id": payable_account.id,
                }
            )
        )
        cash_advance.action_confirm()
        # `approve_ok` is a computed policy field whose dependencies are
        # not declared via `@api.depends` (see
        # ssi_transaction_confirm_mixin), so it is not automatically
        # invalidated by `action_confirm()` within the same environment.
        # Force recomputation before calling `action_approve_approval()`,
        # mirroring `test_data_hr_cash_advance.yaml`.
        cash_advance.invalidate_cache()
        cash_advance.action_approve_approval()

        # Pre-Condition IK 05-approve.md (delta): record already Waiting
        # for Approval. The "Standard" approval template used by
        # ssi_hr_cash_advance has no Documenso Signing Template
        # configured, so the Signature Requests tab is present
        # (``_documenso_signing_create_page = True``) but the base
        # Approve/OK Flow is unaffected -- this tour does not exercise
        # it.
        cls.settlement_approve = (
            cls.env["hr.cash_advance_settlement"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": expense_type.id,
                    "cash_advance_id": cash_advance.id,
                    "date": "2026-02-01",
                    "currency_id": cls.env.company.currency_id.id,
                    "journal_id": settlement_journal.id,
                }
            )
        )
        cls.settlement_approve.action_confirm()

    def test_approve(self):
        """Run the approve tour for the Documenso signing delta.

        IK: docs/hr_cash_advance_settlement/05-approve.md (E2a delta --
        Modified Flow)
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_documenso_signing_hr_cash_advance_settlement_approve",
            login="admin",
        )
