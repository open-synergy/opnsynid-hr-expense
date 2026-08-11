# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrCashAdvance(HttpSavepointCase):
    """Tour tests for the ``hr.cash_advance`` work instructions.

    Covers the base create/confirm/approve/cancel flow
    (``docs/hr_cash_advance/01-create.md``, ``04-confirm.md``,
    ``05-approve.md``, ``10-cancel.md``) plus the edit/delete/reject/
    reopen/done/restart/reset-number flows added by issue
    open-synergy/opnsynid-hr-expense#192
    (``02-edit.md``, ``03-delete.md``, ``06-reject.md``,
    ``07-reopen.md``, ``09-done.md``, ``12-restart.md``,
    ``13-reset-number.md``). All master data is built from scratch in
    ``setUpClass`` -- no demo data is relied upon.
    """

    @classmethod
    def setUpClass(cls):
        """Create shared master data and one fixture record per tour.

        Builds the accounting and expense-type master data shared by
        all four tours, then one ``hr.cash_advance`` record per tour
        (except create, which the tour itself creates via the UI)
        with a unique employee name used as the list-row marker
        (Keputusan Desain, issue
        open-synergy/opnsynid-hr-expense#131). The create tour relies
        on the Employee field's existing default
        (``mixin.employee_document._default_employee_id``) instead of
        a fixture employee -- see the comment above that fixture's
        (deliberately absent) block for why.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        account_type_payable = cls.env.ref("account.data_account_type_payable")
        cash_advance_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Advance Account",
                    "code": "TOURCADADV",
                    "user_type_id": account_type_payable.id,
                    "internal_type": "other",
                    "reconcile": True,
                }
            )
        )
        payable_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Payable Account",
                    "code": "TOURCADPAY",
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
                    "name": "Tour Cash Advance Journal",
                    "code": "TCADJ",
                    "type": "general",
                }
            )
        )
        # Shared by all four tours. Its name matches the literal
        # string the create tour's JS types into the Type field, and
        # its cash-advance accounting fields let Journal, Cash
        # Advance Account, and Payable Account auto-fill via onchange
        # once Type is selected (Keputusan Desain).
        cls.expense_type = (
            cls.env["hr.expense_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Create Type",
                    "code": "TOURCADTYPE",
                    "cash_advance_journal_id": journal.id,
                    "cash_advance_account_id": cash_advance_account.id,
                    "cash_advance_payable_account_id": payable_account.id,
                }
            )
        )
        cls.journal = journal
        cls.cash_advance_account = cash_advance_account
        cls.payable_account = payable_account
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Cancel Reason",
                    "code": "TOURCADCANCEL",
                    "global_use": True,
                }
            )
        )

        # Fixture for the create tour: only the master data the tour
        # picks from a dropdown is needed (the type above) -- the
        # tour itself creates the ``hr.cash_advance`` record via the
        # UI. No dedicated employee is created here: ``hr.employee``
        # has a unique constraint on ``user_id``
        # (``hr_employee_user_uniq``), and the CI database already
        # links ``base.user_admin`` to a default employee via demo
        # data, so the Employee field's default
        # (``mixin.employee_document._default_employee_id``) already
        # resolves without any fixture -- the tour never asserts
        # which employee it resolves to (Keputusan Desain, issue
        # open-synergy/opnsynid-hr-expense#131: "nilai turunan ...
        # dibiarkan apa adanya").

        # Fixture for the confirm tour -- Pre-Condition: Draft
        # status.
        employee_confirm = cls._create_employee("Tour Cash Advance Confirm Employee")
        cls.cash_advance_confirm = cls._create_cash_advance(employee_confirm)

        # Fixture for the approve tour -- Pre-Condition: Waiting for
        # Approval status, reached in Python via ``action_confirm()``,
        # not by clicking through the UI. The employee needs a home
        # address: reaching Open triggers
        # ``_create_accounting_entry`` -> ``_get_partner_id``, which
        # raises without one.
        employee_approve = cls._create_employee(
            "Tour Cash Advance Approve Employee", with_address=True
        )
        cls.cash_advance_approve = cls._create_cash_advance(employee_approve)
        cls.cash_advance_approve.action_confirm()

        # Fixture for the cancel tour -- Pre-Condition: any of Draft,
        # Waiting for Approval, or Open status; Draft is used since
        # no extra state transition is required for it.
        employee_cancel = cls._create_employee("Tour Cash Advance Cancel Employee")
        cls.cash_advance_cancel = cls._create_cash_advance(employee_cancel)

        # Fixture for the edit tour -- Pre-Condition: Draft status.
        employee_edit = cls._create_employee("Tour Cash Advance Edit Employee")
        cls.cash_advance_edit = cls._create_cash_advance(employee_edit)

        # Fixture for the delete tour -- Pre-Condition: Draft status,
        # document number still "/".
        employee_delete = cls._create_employee("Tour Cash Advance Delete Employee")
        cls.cash_advance_delete = cls._create_cash_advance(employee_delete)

        # Fixture for the reject tour -- Pre-Condition: Waiting for
        # Approval status, reached in Python via action_confirm(), not
        # by clicking through the UI -- the reject tour itself clicks
        # Reject.
        employee_reject = cls._create_employee("Tour Cash Advance Reject Employee")
        cls.cash_advance_reject = cls._create_cash_advance(employee_reject)
        cls.cash_advance_reject.action_confirm()

        # Fixture for the restart tour -- Pre-Condition: Cancelled or
        # Rejected status; Rejected is used, reached in Python via
        # action_confirm() then action_reject_approval() (mirrors the
        # confirm->approve refresh dance below, T-04).
        employee_restart = cls._create_employee("Tour Cash Advance Restart Employee")
        cls.cash_advance_restart = cls._create_cash_advance(employee_restart)
        cls.cash_advance_restart.action_confirm()
        cls.cash_advance_restart.flush()
        cls.cash_advance_restart.invalidate_cache(ids=cls.cash_advance_restart.ids)
        cls.cash_advance_restart.action_reject_approval()

        # Fixture for the reset-number tour -- Pre-Condition: Draft
        # status.
        employee_reset_number = cls._create_employee(
            "Tour Cash Advance Reset Number Employee"
        )
        cls.cash_advance_reset_number = cls._create_cash_advance(employee_reset_number)

        # Fixture for the done and reopen tours -- Pre-Condition: Open
        # status reached via the confirm->approve refresh dance (T-04),
        # then `realized`/`settled` are written directly (mirrors
        # tests/test_data_hr_cash_advance_action.yaml "Action Recompute
        # Realization" scenario) and `action_recompute_realization` is
        # called in Python -- exactly the path the real
        # `cash_advance_open_2_done` / `cash_advance_done_2_open`
        # `base.automation` records take, per Keputusan Desain (issue
        # #192): "Tour untuk IK base.automation menyiapkan kondisi di
        # Python, lalu hanya memverifikasi tampilannya."
        employee_done = cls._create_employee(
            "Tour Cash Advance Done Employee", with_address=True
        )
        cls.cash_advance_done = cls._create_open_cash_advance(employee_done)
        cls.cash_advance_done.write({"realized": True, "settled": True})
        cls.cash_advance_done.action_recompute_realization()

        employee_reopen = cls._create_employee(
            "Tour Cash Advance Reopen Employee", with_address=True
        )
        cls.cash_advance_reopen = cls._create_open_cash_advance(employee_reopen)
        cls.cash_advance_reopen.write({"realized": True, "settled": True})
        cls.cash_advance_reopen.action_recompute_realization()
        cls.cash_advance_reopen.write({"realized": False})
        cls.cash_advance_reopen.action_recompute_realization()

    @classmethod
    def _create_open_cash_advance(cls, employee):
        """Create and open an ``hr.cash_advance`` for the given employee.

        Pushed to **Open** in Python via ``action_confirm()`` then
        ``action_approve_approval()`` -- not by clicking through the
        UI (Keputusan Desain, issue
        open-synergy/opnsynid-hr-expense#131).

        Between the two calls the record is flushed and its cache
        invalidated (scoped to its own ids) -- without the refresh,
        ``action_approve_approval()`` reads a stale cached
        ``approve_ok`` and raises "Document is not allowed to
        approve" nondeterministically (T-04, mirrors
        ``test_ui_hr_cash_advance_settlement.py``
        ``_create_open_cash_advance``).

        :param employee: ``hr.employee`` the record is submitted for,
            requires a home address (``action_open`` ->
            ``_create_accounting_entry`` -> ``_get_partner_id`` raises
            without one)
        :return: the created ``hr.cash_advance``, in Open status
        """
        cash_advance = cls._create_cash_advance(employee)
        cash_advance.action_confirm()
        cash_advance.flush()
        cash_advance.invalidate_cache(ids=cash_advance.ids)
        cash_advance.action_approve_approval()
        return cash_advance

    @classmethod
    def _create_employee(cls, name, with_address=False):
        """Create an employee, optionally with a home-address partner.

        :param name: unique employee name, also used as the tour's
            list-row marker
        :param with_address: when ``True``, link a new
            ``res.partner`` as the employee's home address (needed by
            ``hr.cash_advance._get_partner_id`` when a fixture must
            reach the **Open** status)
        :return: the created ``hr.employee``
        """
        vals = {"name": name}
        if with_address:
            partner = (
                cls.env["res.partner"]
                .with_user(cls.admin)
                .create({"name": name + " Home"})
            )
            vals["address_home_id"] = partner.id
        return cls.env["hr.employee"].with_user(cls.admin).create(vals)

    @classmethod
    def _create_cash_advance(cls, employee):
        """Create a draft ``hr.cash_advance`` for the given employee.

        Built entirely in Python (Pre-Condition setup), not by
        clicking through the UI, per Keputusan Desain (issue
        open-synergy/opnsynid-hr-expense#131).

        :param employee: ``hr.employee`` the record is submitted for
        :return: the created ``hr.cash_advance`` record, in Draft
        """
        return (
            cls.env["hr.cash_advance"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": cls.expense_type.id,
                    "journal_id": cls.journal.id,
                    "cash_advance_account_id": cls.cash_advance_account.id,
                    "payable_account_id": cls.payable_account.id,
                    "date": "2026-01-01",
                    "date_due": "2026-01-31",
                }
            )
        )

    def test_create(self):
        """Run the create tour for ``hr.cash_advance``.

        IK: docs/hr_cash_advance/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``hr.cash_advance``.

        IK: docs/hr_cash_advance/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``hr.cash_advance``.

        IK: docs/hr_cash_advance/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_approve",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``hr.cash_advance``.

        IK: docs/hr_cash_advance/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_cancel",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.cash_advance``.

        IK: docs/hr_cash_advance/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``hr.cash_advance``.

        IK: docs/hr_cash_advance/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_delete",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``hr.cash_advance``.

        IK: docs/hr_cash_advance/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_reject",
            login="admin",
        )

    def test_reopen(self):
        """Run the reopen tour for ``hr.cash_advance``.

        The Done -> Open transition itself is automatic
        (``base.automation`` ``cash_advance_done_2_open``); the
        fixture is already Open before this tour starts, reached in
        Python exactly as the automation would run it
        (odoo-development-ui-test, scope-and-boundaries.md §1 aturan
        6). This tour observes the result and exercises the inline
        Recompute Realization action hosted on this IK.

        IK: docs/hr_cash_advance/07-reopen.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_reopen",
            login="admin",
        )

    def test_done(self):
        """Run the done tour for ``hr.cash_advance``.

        The Open -> Done transition itself is automatic
        (``base.automation`` ``cash_advance_open_2_done``); the
        fixture is already Done before this tour starts, reached in
        Python exactly as the automation would run it
        (odoo-development-ui-test, scope-and-boundaries.md §1 aturan
        6). This tour observes the result and exercises the inline
        Recompute Realization action hosted on this IK.

        IK: docs/hr_cash_advance/09-done.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_done",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``hr.cash_advance``.

        IK: docs/hr_cash_advance/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_restart",
            login="admin",
        )

    def test_reset_number(self):
        """Run the reset document number tour for ``hr.cash_advance``.

        IK: docs/hr_cash_advance/13-reset-number.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_reset_number",
            login="admin",
        )
