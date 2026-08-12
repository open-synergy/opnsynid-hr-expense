# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrReimbursement(HttpSavepointCase):
    """Tour tests for the Expense Account delta on reimbursement lines.

    Covers the field delta on create
    (``docs/hr_reimbursement/01-create.md``) and the confirm
    validation delta (``docs/hr_reimbursement/04-confirm.md``) added
    by issue open-synergy/opnsynid-hr-expense#197.
    """

    @classmethod
    def setUpClass(cls):
        """Grant menu access and build the confirm tour's fixture.

        The Reimbursements menu group is already covered by the
        default membership of ``hr_reimbursement_validator_group``
        (which implies the viewer group), but the grant is repeated
        explicitly here so the tour does not depend on that
        implication chain, built from scratch with ``sudo()`` and
        without relying on demo data.

        The confirm tour additionally needs a stored Draft
        ``hr.reimbursement`` whose only line is flagged **Require
        Expense Account** and already links a matching, sufficiently
        funded ``employee_expense_account`` -- the Pre-Condition that
        lets this module's ``_check_expense_account``
        (``pre_confirm_action`` hook, ``models/hr_reimbursement.py``)
        pass, so the tour can exercise the base IK's normal Confirm
        Flow instead of a server-rejected one (see ``test_confirm``
        docstring for why). All master data is built from scratch in
        Python (Keputusan Desain, issue
        open-synergy/opnsynid-hr-expense#130): the create tour still
        does not Save, so it needs no stored record of its own.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.env.ref("ssi_hr_reimbursement.hr_reimbursement_viewer_group").sudo().write(
            {"users": [(4, cls.admin.id)]}
        )

        account_type_payable = cls.env.ref("account.data_account_type_payable")
        header_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Confirm Reimbursement Header Account",
                    "code": "TOURRMBCFRHDR",
                    "user_type_id": account_type_payable.id,
                    "internal_type": "other",
                    "reconcile": True,
                }
            )
        )
        line_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Confirm Reimbursement Line Account",
                    "code": "TOURRMBCFRLN",
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
                    "name": "Tour Confirm Reimbursement Journal",
                    "code": "TRMBCFRJ",
                    "type": "general",
                }
            )
        )
        usage_type = (
            cls.env["product.usage_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Confirm Reimbursement Usage",
                    "code": "TOURRMBCFRUSAGE",
                    "account_id": line_account.id,
                }
            )
        )
        product = (
            cls.env["product.product"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Confirm Reimbursement Product",
                    "type": "consu",
                }
            )
        )
        # `require_expense_account` on the type-product line is what
        # `_get_require_expense_products` (ssi_hr_expense_account,
        # models/hr_expense_type.py) reads; the line below sets the
        # equivalent flag directly on the reimbursement line since
        # this fixture is built in Python, not via the UI onchange.
        expense_type = (
            cls.env["hr.expense_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Confirm Reimbursement Type",
                    "code": "TOURRMBCFRTYPE",
                    "reimbursement_journal_id": journal.id,
                    "reimbursement_account_id": header_account.id,
                    "default_product_usage_id": usage_type.id,
                    "product_ids": [
                        (
                            0,
                            0,
                            {
                                "product_id": product.id,
                                "require_expense_account": True,
                            },
                        )
                    ],
                }
            )
        )
        partner = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Tour Confirm Reimbursement Employee Home"})
        )
        employee = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Confirm Reimbursement Employee",
                    "address_home_id": partner.id,
                }
            )
        )
        bank = (
            cls.env["res.partner.bank"]
            .with_user(cls.admin)
            .create(
                {
                    "acc_number": "TOURRMBCFRBANK",
                    "partner_id": partner.id,
                }
            )
        )
        # This module's Additional Validation
        # (``_check_expense_account``) only requires a linked
        # ``employee_expense_account`` with a non-negative
        # ``amount_residual`` -- it does not read the account's own
        # workflow ``state``. ``amount_residual`` is computed as
        # ``amount_limit - amount_realized`` (models/
        # employee_expense_account.py ``_compute_amount``), and a
        # freshly created account has no realized amount yet, so a
        # bare Draft record with a positive ``amount_limit`` already
        # satisfies the check.
        ea_currency = (
            cls.env["res.currency"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TRC",
                    "symbol": "TR$",
                }
            )
        )
        ea_type = (
            cls.env["employee_expense_account_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Confirm Reimbursement EA Type",
                    "code": "TOURRMBCFREATYPE",
                }
            )
        )
        expense_account = (
            cls.env["employee_expense_account"]
            .with_user(cls.admin)
            .create(
                {
                    "type_id": ea_type.id,
                    "currency_id": ea_currency.id,
                    "employee_id": employee.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                    "amount_limit": 1000.0,
                }
            )
        )
        cls.reimbursement_confirm = (
            cls.env["hr.reimbursement"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee.id,
                    "employee_bank_account_id": bank.id,
                    "type_id": expense_type.id,
                    "journal_id": journal.id,
                    "account_id": header_account.id,
                    "date": "2026-01-01",
                    "date_due": "2026-01-31",
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "date_expense": "2026-01-01",
                                "product_id": product.id,
                                "name": "Tour Confirm Reimbursement Expense Line",
                                "usage_id": usage_type.id,
                                "account_id": line_account.id,
                                "price_unit": 100.0,
                                "uom_quantity": 1.0,
                                "uom_id": product.uom_id.id,
                                "require_expense_account": True,
                                "expense_account_id": expense_account.id,
                            },
                        )
                    ],
                }
            )
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

    def test_confirm(self):
        """Run the base Confirm Flow with this module's check satisfied.

        IK: docs/hr_reimbursement/04-confirm.md

        Flow and Post-Condition are taken verbatim from the base IK
        (``ssi_hr_reimbursement/docs/hr_reimbursement/04-confirm.md``)
        -- this module adds no UI step to Confirm, only a pre-confirm
        check (``models/hr_reimbursement.py``
        ``_check_expense_account``). The fixture line already
        satisfies that check (Require Expense Account = True with a
        linked, sufficiently funded ``employee_expense_account``), so
        this tour proves the base Flow still completes once the extra
        check is installed. The negative path (missing/insufficient
        expense account blocking Confirm with "No expense account" /
        "Insuficient expense account") is a value/error-message
        assertion and stays with unit test ``expect_error``, not this
        tour (``odoo-development-ui-test``,
        ``scope-and-boundaries.md``, arketipe E2b) -- the same
        resolution already used by the sibling delta tour in
        ``ssi_hr_expense_account_cash_advance`` (issue
        open-synergy/opnsynid-hr-expense#136).
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_reimbursement_hr_reimbursement_confirm",
            login="admin",
        )
