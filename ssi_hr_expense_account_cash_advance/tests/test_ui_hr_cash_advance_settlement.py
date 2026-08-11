# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrCashAdvanceSettlement(HttpSavepointCase):
    """Tour tests for the Expense Account delta on settlement lines.

    Covers the ``01-create.md`` field delta (Additional Fields) and the
    ``04-confirm.md`` validation delta (Additional Validation) of
    ``docs/hr_cash_advance_settlement/``. The confirm tour re-runs the
    base module's Confirm Flow
    (``ssi_hr_cash_advance/docs/hr_cash_advance_settlement/04-confirm.md``)
    on a settlement line whose ``require_expense_account`` /
    ``expense_account_id`` (this module's delta) already satisfy the
    Additional Validation this module adds, proving the extra
    pre-confirm check
    (``models/hr_cash_advance_settlement.py`` ``_check_expense_account``)
    does not block Confirm once the Expense Account requirement is met.
    The negative path (missing/insufficient Expense Account blocking
    Confirm) is a value/error-message assertion and stays with unit
    test ``expect_error`` (odoo-development-ui-test,
    scope-and-boundaries.md, arketipe E2b).
    """

    @classmethod
    def setUpClass(cls):
        """Grant menu access, then build the Confirm tour fixture.

        The Cash Advance Settlements menu access is already covered by
        the default membership of
        ``hr_cash_advance_settlement_validator_group`` (which implies
        the viewer group), but the grant is repeated explicitly here so
        the tour does not depend on that implication chain. The create
        tour never Saves, so no stored settlement record is needed for
        it. The confirm tour needs one full Draft settlement whose line
        already satisfies this module's Expense Account validation,
        built entirely in Python (Keputusan Desain, issue
        open-synergy/opnsynid-hr-expense#136).
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_hr_cash_advance.hr_cash_advance_settlement_viewer_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

        account_type_payable = cls.env.ref("account.data_account_type_payable")
        cls.line_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Expense Account Settlement Confirm Line Account",
                    "code": "TEASETCONFLN",
                    "user_type_id": account_type_payable.id,
                    "internal_type": "other",
                    "reconcile": True,
                }
            )
        )
        cls.ca_cash_advance_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Expense Account Settlement Confirm CA Account",
                    "code": "TEASETCONFCA",
                    "user_type_id": account_type_payable.id,
                    "internal_type": "other",
                    "reconcile": True,
                }
            )
        )
        cls.ca_payable_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": (
                        "Tour Expense Account Settlement Confirm CA Payable " "Account"
                    ),
                    "code": "TEASETCONFPAY",
                    "user_type_id": account_type_payable.id,
                    "internal_type": "other",
                    "reconcile": True,
                }
            )
        )
        cls.ca_journal = (
            cls.env["account.journal"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Expense Account Settlement Confirm CA Journal",
                    "code": "TEASCCA",
                    "type": "general",
                }
            )
        )
        cls.settlement_journal = (
            cls.env["account.journal"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Expense Account Settlement Confirm Journal",
                    "code": "TEASCST",
                    "type": "general",
                }
            )
        )
        cls.expense_type = (
            cls.env["hr.expense_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Expense Account Settlement Confirm Type",
                    "code": "TEASETCONFTYPE",
                    "cash_advance_journal_id": cls.ca_journal.id,
                    "cash_advance_account_id": cls.ca_cash_advance_account.id,
                    "cash_advance_payable_account_id": cls.ca_payable_account.id,
                    "cash_advance_settlement_journal_id": (cls.settlement_journal.id),
                }
            )
        )
        cls.product = (
            cls.env["product.product"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Expense Account Settlement Confirm Product",
                    "type": "consu",
                }
            )
        )

        # Expense account type allowing the line account, and the
        # employee expense account itself -- Pre-Condition of the
        # Additional Validation this module adds: an active expense
        # account matching the employee/account/date, with a
        # non-negative residual amount.
        cls.ea_type = (
            cls.env["employee_expense_account_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Expense Account Settlement Confirm EA Type",
                    "code": "/",
                    "account_ids": [(6, 0, [cls.line_account.id])],
                }
            )
        )
        cls.ea_currency = (
            cls.env["res.currency"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TEC",
                    "symbol": "T$",
                }
            )
        )
        # ``address_home_id`` is required: the underlying cash advance's
        # ``action_open`` -> ``_create_accounting_entry`` ->
        # ``_get_partner_id`` raises "No home address defined for
        # employee" without one (mirrors the base module's own
        # ``_create_employee`` tour fixture helper,
        # ``ssi_hr_cash_advance/tests/test_ui_hr_cash_advance_settlement.py``).
        confirm_home = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Tour Expense Account Settlement Confirm Home"})
        )
        employee_confirm = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Expense Account Settlement Confirm Employee",
                    "address_home_id": confirm_home.id,
                }
            )
        )
        cls.expense_account_confirm = (
            cls.env["employee_expense_account"]
            .with_user(cls.admin)
            .create(
                {
                    "type_id": cls.ea_type.id,
                    "currency_id": cls.ea_currency.id,
                    "employee_id": employee_confirm.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                    "amount_limit": 1000.0,
                }
            )
        )
        cls.expense_account_confirm.with_user(cls.admin).action_confirm()
        # Force a fresh read before approving -- the shared
        # ``mixin.policy`` compute caches ``approve_ok`` at a moment
        # this record's ``approval.approval`` row does not exist yet
        # otherwise (T-04, see also this module's own onchange test
        # data, ``test_data_hr_cash_advance_settlement_onchange.yaml``).
        cls.expense_account_confirm.flush()
        cls.expense_account_confirm.invalidate_cache(
            ids=cls.expense_account_confirm.ids
        )
        cls.expense_account_confirm.with_user(cls.admin).action_approve_approval()

        # The underlying cash advance, pushed to Open in Python
        # (Pre-Condition of every settlement tour: "At least one Cash
        # Advance record in Open status exists for the employee"), not
        # by clicking through the UI.
        cash_advance_confirm = (
            cls.env["hr.cash_advance"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee_confirm.id,
                    "type_id": cls.expense_type.id,
                    "journal_id": cls.ca_journal.id,
                    "cash_advance_account_id": cls.ca_cash_advance_account.id,
                    "payable_account_id": cls.ca_payable_account.id,
                    "date": "2026-01-01",
                    "date_due": "2026-01-31",
                }
            )
        )
        cash_advance_confirm.with_user(cls.admin).action_confirm()
        cash_advance_confirm.flush()
        cash_advance_confirm.invalidate_cache(ids=cash_advance_confirm.ids)
        cash_advance_confirm.with_user(cls.admin).action_approve_approval()

        # Draft settlement whose one line already satisfies this
        # module's Expense Account validation (Required = True,
        # Expense Account filled with a matching, non-negative-
        # residual account) -- set directly, not through the onchange
        # this module adds (docs/hr_cash_advance_settlement/
        # 01-create.md), since the fixture is built in Python.
        cls.settlement_confirm = (
            cls.env["hr.cash_advance_settlement"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee_confirm.id,
                    "type_id": cls.expense_type.id,
                    "cash_advance_id": cash_advance_confirm.id,
                    "journal_id": cls.settlement_journal.id,
                    "date": "2026-01-15",
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "date_expense": "2026-01-15",
                                "product_id": cls.product.id,
                                "name": (
                                    "Tour Expense Account Settlement Confirm " "Line"
                                ),
                                "account_id": cls.line_account.id,
                                "price_unit": 100.0,
                                "uom_quantity": 1.0,
                                "uom_id": cls.product.uom_id.id,
                                "require_expense_account": True,
                                "expense_account_id": (cls.expense_account_confirm.id),
                            },
                        )
                    ],
                }
            )
        )

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

    def test_confirm(self):
        """Run the Expense Account validation delta tour for Confirm.

        IK: docs/hr_cash_advance_settlement/04-confirm.md

        Re-runs the base module's Confirm Flow on a line whose
        Required / Expense Account fields already satisfy the
        Additional Validation this module adds, then asserts the base
        Post-Condition (status changes to Waiting for Approval) still
        holds once the extra pre-confirm check is installed.
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_cash_advance_hr_cash_advance_settlement_confirm",
            login="admin",
        )
