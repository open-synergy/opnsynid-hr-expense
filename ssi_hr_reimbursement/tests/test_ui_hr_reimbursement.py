# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrReimbursement(HttpSavepointCase):
    """Tour tests for the ``hr.reimbursement`` work instructions.

    Covers the base create/confirm/approve/cancel flow
    (``docs/hr_reimbursement/01-create.md``, ``04-confirm.md``,
    ``05-approve.md``, ``10-cancel.md``) plus the edit/delete/reject/
    start/finish/restart/reset-number flows added by issue
    open-synergy/opnsynid-hr-expense#193
    (``02-edit.md``, ``03-delete.md``, ``06-reject.md``,
    ``07-start.md``, ``09-finish.md``, ``12-restart.md``,
    ``13-reset-number.md``). All master data is built from scratch in
    ``setUpClass`` -- no demo data is relied upon.
    """

    @classmethod
    def setUpClass(cls):
        """Create shared master data and one fixture record per tour.

        Grants the Reimbursements menu group to ``admin`` (already
        implied by ``hr_reimbursement_validator_group`` membership from
        ``security/res_group_data.xml``, repeated here so the tour does
        not depend on that implication chain), then builds the
        accounting, product, and expense-type master data shared by all
        tours, and one ``hr.reimbursement`` record per tour with a
        unique employee name used as the list-row marker (Keputusan
        Desain, issue open-synergy/opnsynid-hr-expense#130).
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
                    "name": "Tour Reimbursement Header Account",
                    "code": "TOURRMBHDR",
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
                    "name": "Tour Reimbursement Line Account",
                    "code": "TOURRMBLN",
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
                    "name": "Tour Reimbursement Journal",
                    "code": "TRMBJ",
                    "type": "general",
                }
            )
        )
        usage_type = (
            cls.env["product.usage_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Reimbursement Usage",
                    "code": "TOURRMBUSAGE",
                    "account_id": line_account.id,
                }
            )
        )
        product = (
            cls.env["product.product"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Reimbursement Product",
                    "type": "consu",
                }
            )
        )
        # Shared by all four tours; its name matches the literal
        # string the create tour's JS types into the Type field.
        cls.expense_type = (
            cls.env["hr.expense_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Reimbursement Create Type",
                    "code": "TOURRMBTYPE",
                    "reimbursement_journal_id": journal.id,
                    "reimbursement_account_id": header_account.id,
                    "default_product_usage_id": usage_type.id,
                    "product_ids": [(0, 0, {"product_id": product.id})],
                }
            )
        )
        cls.product = product
        cls.journal = journal
        cls.header_account = header_account
        cls.line_account = line_account
        cls.usage_type = usage_type
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Reimbursement Cancel Reason",
                    "code": "TOURRMBCANCEL",
                    "global_use": True,
                }
            )
        )

        # Fixture for the create tour: only the master data the tour
        # picks from dropdowns is needed -- the tour itself creates the
        # ``hr.reimbursement`` record via the UI. The bank account
        # number must match the literal string the JS tour searches
        # for (static, not derived from a runtime id).
        cls._create_employee_with_bank(
            "Tour Reimbursement Create Employee", "TOURRMBCREATEBANK"
        )

        # Fixture for the confirm tour -- Pre-Condition: Draft status.
        employee_confirm, bank_confirm = cls._create_employee_with_bank(
            "Tour Reimbursement Confirm Employee", "TOURRMBCONFIRMBANK"
        )
        cls.reimbursement_confirm = cls._create_reimbursement(
            employee_confirm, bank_confirm
        )

        # Fixture for the approve tour -- Pre-Condition: Waiting for
        # Approval status, reached in Python via ``action_confirm()``,
        # not by clicking through the UI.
        employee_approve, bank_approve = cls._create_employee_with_bank(
            "Tour Reimbursement Approve Employee", "TOURRMBAPPROVEBANK"
        )
        cls.reimbursement_approve = cls._create_reimbursement(
            employee_approve, bank_approve
        )
        cls.reimbursement_approve.action_confirm()

        # Fixture for the cancel tour -- Pre-Condition: any of Draft,
        # Waiting for Approval, or In Progress status; Draft is used
        # since no extra state transition is required for it.
        employee_cancel, bank_cancel = cls._create_employee_with_bank(
            "Tour Reimbursement Cancel Employee", "TOURRMBCANCELBANK"
        )
        cls.reimbursement_cancel = cls._create_reimbursement(
            employee_cancel, bank_cancel
        )

        # Fixture for the edit tour -- Pre-Condition: Draft status.
        employee_edit, bank_edit = cls._create_employee_with_bank(
            "Tour Reimbursement Edit Employee", "TOURRMBEDITBANK"
        )
        cls.reimbursement_edit = cls._create_reimbursement(employee_edit, bank_edit)

        # Fixture for the delete tour -- Pre-Condition: Draft status,
        # document number still "/".
        employee_delete, bank_delete = cls._create_employee_with_bank(
            "Tour Reimbursement Delete Employee", "TOURRMBDELETEBANK"
        )
        cls.reimbursement_delete = cls._create_reimbursement(
            employee_delete, bank_delete
        )

        # Fixture for the reject tour -- Pre-Condition: Waiting for
        # Approval status, reached in Python via ``action_confirm()``,
        # not by clicking through the UI -- the reject tour itself
        # clicks Reject.
        employee_reject, bank_reject = cls._create_employee_with_bank(
            "Tour Reimbursement Reject Employee", "TOURRMBREJECTBANK"
        )
        cls.reimbursement_reject = cls._create_reimbursement(
            employee_reject, bank_reject
        )
        cls.reimbursement_reject.action_confirm()

        # Fixture for the restart tour -- Pre-Condition: Cancelled or
        # Rejected status; Rejected is used, reached in Python via
        # ``action_confirm()`` then ``action_reject_approval()``.
        employee_restart, bank_restart = cls._create_employee_with_bank(
            "Tour Reimbursement Restart Employee", "TOURRMBRESTARTBANK"
        )
        cls.reimbursement_restart = cls._create_reimbursement(
            employee_restart, bank_restart
        )
        cls.reimbursement_restart.action_confirm()
        cls.reimbursement_restart.action_reject_approval()

        # Fixture for the reset-number tour -- Pre-Condition: Draft
        # status.
        employee_reset_number, bank_reset_number = cls._create_employee_with_bank(
            "Tour Reimbursement Reset Number Employee", "TOURRMBRESETBANK"
        )
        cls.reimbursement_reset_number = cls._create_reimbursement(
            employee_reset_number, bank_reset_number
        )

        # Fixture for the finish and start tours -- Pre-Condition: In
        # Progress status, reached in Python via ``action_confirm()``
        # then ``action_open()`` directly (mirrors
        # ``tests/test_data_hr_reimbursement_action.yaml`` "Action
        # Recompute Realization" scenario). The computed+stored
        # ``reconciled`` field is then written directly and
        # ``action_recompute_realization`` is called -- exactly the
        # path the real ``reimbursement_ready_2_done`` /
        # ``reimbursement_ready_2_open`` ``base.automation`` records
        # take, per Keputusan Desain (issue #193, mirrors issue #192
        # for ``ssi_hr_cash_advance``): "Tour untuk IK
        # base.automation menyiapkan kondisi di Python, lalu hanya
        # memverifikasi tampilannya."
        employee_finish, bank_finish = cls._create_employee_with_bank(
            "Tour Reimbursement Finish Employee", "TOURRMBFINISHBANK"
        )
        cls.reimbursement_finish = cls._create_open_reimbursement(
            employee_finish, bank_finish
        )
        cls.reimbursement_finish.write({"reconciled": True})
        cls.reimbursement_finish.action_recompute_realization()

        employee_start, bank_start = cls._create_employee_with_bank(
            "Tour Reimbursement Start Employee", "TOURRMBSTARTBANK"
        )
        cls.reimbursement_start = cls._create_open_reimbursement(
            employee_start, bank_start
        )
        cls.reimbursement_start.write({"reconciled": True})
        cls.reimbursement_start.action_recompute_realization()
        cls.reimbursement_start.write({"reconciled": False})
        cls.reimbursement_start.action_recompute_realization()

    @classmethod
    def _create_open_reimbursement(cls, employee, bank):
        """Create and open an ``hr.reimbursement`` for the given employee.

        Pushed to **In Progress** in Python via ``action_confirm()``
        then ``action_open()`` directly -- not via
        ``action_approve_approval()`` nor by clicking through the UI,
        mirroring the already-passing sequence in
        ``tests/test_data_hr_reimbursement_action.yaml`` ("Action
        Recompute Realization" scenario), per the create-in-Python
        convention (Keputusan Desain, issue
        open-synergy/opnsynid-hr-expense#130).

        :param employee: ``hr.employee`` the record is submitted for
        :param bank: ``res.partner.bank`` used as the payment account
        :return: the created ``hr.reimbursement``, in In Progress
            status
        """
        reimbursement = cls._create_reimbursement(employee, bank)
        reimbursement.action_confirm()
        reimbursement.action_open()
        return reimbursement

    @classmethod
    def _create_employee_with_bank(cls, name, bank_acc_number):
        """Create an employee and a bank account tied to its address.

        The bank account is linked to the employee's home-address
        contact, matching the domain ``mixin.employee_bank_account``
        uses to compute ``allowed_bank_account_ids``, so it appears as
        a selectable option for ``employee_bank_account_id``. The
        employee's own ``bank_account_id`` is left unset so the tour's
        manual Bank Account selection step is not a no-op.

        :param name: unique employee name, also used as the tour's
            list-row marker
        :param bank_acc_number: static, unique account number -- for
            the create tour this must equal the literal string the JS
            tour types into the Bank Account field, since it cannot
            reference a runtime-generated id
        :return: tuple of the created ``hr.employee`` and
            ``res.partner.bank`` records
        """
        partner = (
            cls.env["res.partner"].with_user(cls.admin).create({"name": name + " Home"})
        )
        employee = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create(
                {
                    "name": name,
                    "address_home_id": partner.id,
                }
            )
        )
        bank = (
            cls.env["res.partner.bank"]
            .with_user(cls.admin)
            .create(
                {
                    "acc_number": bank_acc_number,
                    "partner_id": partner.id,
                }
            )
        )
        return employee, bank

    @classmethod
    def _create_reimbursement(cls, employee, bank):
        """Create a draft ``hr.reimbursement`` with one expense line.

        Built entirely in Python (Pre-Condition setup), not by clicking
        through the UI, per Keputusan Desain (issue
        open-synergy/opnsynid-hr-expense#130).

        :param employee: ``hr.employee`` the record is submitted for
        :param bank: ``res.partner.bank`` used as the payment account
        :return: the created ``hr.reimbursement`` record, in Draft
        """
        return (
            cls.env["hr.reimbursement"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee.id,
                    "employee_bank_account_id": bank.id,
                    "type_id": cls.expense_type.id,
                    "journal_id": cls.journal.id,
                    "account_id": cls.header_account.id,
                    "date": "2026-01-01",
                    "date_due": "2026-01-31",
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "date_expense": "2026-01-01",
                                "product_id": cls.product.id,
                                "name": "Tour Reimbursement Expense Line",
                                "usage_id": cls.usage_type.id,
                                "account_id": cls.line_account.id,
                                "price_unit": 100.0,
                                "uom_quantity": 1.0,
                                "uom_id": cls.product.uom_id.id,
                            },
                        )
                    ],
                }
            )
        )

    def test_create(self):
        """Run the create tour for ``hr.reimbursement``.

        IK: docs/hr_reimbursement/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_reimbursement_hr_reimbursement_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``hr.reimbursement``.

        IK: docs/hr_reimbursement/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_reimbursement_hr_reimbursement_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``hr.reimbursement``.

        IK: docs/hr_reimbursement/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_reimbursement_hr_reimbursement_approve",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``hr.reimbursement``.

        IK: docs/hr_reimbursement/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_reimbursement_hr_reimbursement_cancel",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.reimbursement``.

        IK: docs/hr_reimbursement/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_reimbursement_hr_reimbursement_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``hr.reimbursement``.

        IK: docs/hr_reimbursement/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_reimbursement_hr_reimbursement_delete",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``hr.reimbursement``.

        IK: docs/hr_reimbursement/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_reimbursement_hr_reimbursement_reject",
            login="admin",
        )

    def test_start(self):
        """Run the start (revert to In Progress) tour for ``hr.reimbursement``.

        The Done -> In Progress transition itself is automatic
        (``base.automation`` ``reimbursement_ready_2_open``); the
        fixture is already In Progress before this tour starts,
        reached in Python exactly as the automation would run it
        (odoo-development-ui-test, scope-and-boundaries.md §1 aturan
        6). This tour observes the result and exercises the inline
        Recompute Realization action hosted on this IK.

        IK: docs/hr_reimbursement/07-start.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_reimbursement_hr_reimbursement_start",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``hr.reimbursement``.

        The In Progress -> Done transition itself is automatic
        (``base.automation`` ``reimbursement_ready_2_done``); the
        fixture is already Done before this tour starts, reached in
        Python exactly as the automation would run it
        (odoo-development-ui-test, scope-and-boundaries.md §1 aturan
        6). This tour observes the result and exercises the inline
        Recompute Realization action hosted on this IK.

        IK: docs/hr_reimbursement/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_reimbursement_hr_reimbursement_finish",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``hr.reimbursement``.

        IK: docs/hr_reimbursement/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_reimbursement_hr_reimbursement_restart",
            login="admin",
        )

    def test_reset_number(self):
        """Run the reset document number tour for ``hr.reimbursement``.

        IK: docs/hr_reimbursement/13-reset-number.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_reimbursement_hr_reimbursement_reset_number",
            login="admin",
        )
