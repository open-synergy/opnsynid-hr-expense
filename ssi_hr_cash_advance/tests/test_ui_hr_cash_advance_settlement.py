# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrCashAdvanceSettlement(HttpSavepointCase):
    """Tour tests for the ``hr.cash_advance_settlement`` work instructions.

    Covers the base create/confirm/approve/cancel flow
    (``docs/hr_cash_advance_settlement/01-create.md``, ``04-confirm.md``,
    ``05-approve.md``, ``10-cancel.md``) plus the edit/delete/reject/
    restart/reset-number flows added by issue
    open-synergy/opnsynid-hr-expense#192
    (``02-edit.md``, ``03-delete.md``, ``06-reject.md``,
    ``12-restart.md``, ``13-reset-number.md``). All master data is
    built from scratch in ``setUpClass`` -- no demo data is relied
    upon, except the employee ``base.user_admin`` already resolves to
    via ``mixin.employee_document._default_employee_id`` (Keputusan
    Desain, issue open-synergy/opnsynid-hr-expense#136).
    """

    @classmethod
    def setUpClass(cls):
        """Create shared master data and one fixture record per tour.

        Builds the accounting, product, and expense-type master data
        shared by all four tours, an **Open** ``hr.cash_advance`` for
        every fixture employee (Pre-Condition of every settlement tour),
        and one ``hr.cash_advance_settlement`` record per tour (except
        create, which the tour itself creates via the UI) with a unique
        employee name used as the list-row marker.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_hr_cash_advance.hr_cash_advance_settlement_viewer_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

        account_type_payable = cls.env.ref("account.data_account_type_payable")
        cls.ca_cash_advance_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Settlement CA Account",
                    "code": "TOURCASETADV",
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
                    "name": "Tour Cash Advance Settlement CA Payable Account",
                    "code": "TOURCASETPAY",
                    "user_type_id": account_type_payable.id,
                    "internal_type": "other",
                    "reconcile": True,
                }
            )
        )
        cls.line_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Settlement Line Account",
                    "code": "TOURCASETLN",
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
                    "name": "Tour Cash Advance Settlement CA Journal",
                    "code": "TCSCA",
                    "type": "general",
                }
            )
        )
        cls.settlement_journal = (
            cls.env["account.journal"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Settlement Journal",
                    "code": "TCSST",
                    "type": "general",
                }
            )
        )
        # ``account_id`` is the fallback used by
        # ``product.product._get_product_account`` when neither the
        # product, its template, nor its category defines an override
        # (``ssi_product_usage_account_type``), so the settlement
        # line's ``onchange_account_id`` resolves ``account_id`` from
        # this usage type once the tour selects the product below.
        cls.usage_type = (
            cls.env["product.usage_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Settlement Usage",
                    "code": "TOURCASETUSAGE",
                    "account_id": cls.line_account.id,
                }
            )
        )
        cls.product = (
            cls.env["product.product"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Settlement Product",
                    "type": "consu",
                }
            )
        )
        # Shared by all four tours. Its name matches the literal
        # string the create tour's JS types into the Type field.
        # ``cash_advance_settlement_journal_id`` lets Journal
        # auto-fill via ``onchange_journal_id`` once Type is selected;
        # ``default_product_usage_id`` lets the line's Usage (and,
        # through it, Account) auto-fill once Product is selected.
        cls.expense_type = (
            cls.env["hr.expense_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Settlement Create Type",
                    "code": "TOURCASETTYPE",
                    "cash_advance_journal_id": cls.ca_journal.id,
                    "cash_advance_account_id": cls.ca_cash_advance_account.id,
                    "cash_advance_payable_account_id": cls.ca_payable_account.id,
                    "cash_advance_settlement_journal_id": cls.settlement_journal.id,
                    "default_product_usage_id": cls.usage_type.id,
                    "product_ids": [(0, 0, {"product_id": cls.product.id})],
                }
            )
        )
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Cash Advance Settlement Cancel Reason",
                    "code": "TOURCASETCANCEL",
                    "global_use": True,
                }
            )
        )

        # Fixture for the create tour: the settlement form's Employee
        # field is left at its default (Keputusan Desain, issue #136,
        # mirrors the base ``hr_cash_advance`` create tour, issue
        # #131), which resolves to ``base.user_admin``'s own employee
        # via ``mixin.employee_document._default_employee_id``. That
        # employee needs a home address (the underlying cash advance's
        # ``action_open`` -> ``_create_accounting_entry`` ->
        # ``_get_partner_id`` raises without one) and an **Open** cash
        # advance to pick from the # Cash Advance dropdown -- given a
        # manual, literal document number here since the auto-assigned
        # sequence value cannot be known ahead of running the tour.
        cls.admin_employee = cls.env["hr.employee"].search(
            [("user_id", "=", cls.admin.id)], limit=1
        )
        admin_home = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create({"name": "Tour Cash Advance Settlement Admin Home"})
        )
        cls.admin_employee.with_user(cls.admin).write(
            {"address_home_id": admin_home.id}
        )
        cls.cash_advance_create = cls._create_open_cash_advance(
            cls.admin_employee, name="TOURCASETTLECREATECA"
        )

        # Fixture for the confirm tour -- Pre-Condition: Draft status.
        employee_confirm = cls._create_employee(
            "Tour Cash Advance Settlement Confirm Employee"
        )
        cash_advance_confirm = cls._create_open_cash_advance(employee_confirm)
        cls.settlement_confirm = cls._create_settlement(
            employee_confirm,
            cash_advance_confirm,
            "Tour Cash Advance Settlement Confirm Line",
        )

        # Fixture for the approve tour -- Pre-Condition: Waiting for
        # Approval status, reached in Python via ``action_confirm()``,
        # not by clicking through the UI.
        employee_approve = cls._create_employee(
            "Tour Cash Advance Settlement Approve Employee"
        )
        cash_advance_approve = cls._create_open_cash_advance(employee_approve)
        cls.settlement_approve = cls._create_settlement(
            employee_approve,
            cash_advance_approve,
            "Tour Cash Advance Settlement Approve Line",
        )
        cls.settlement_approve.action_confirm()

        # Fixture for the cancel tour -- Pre-Condition: any of Draft,
        # Waiting for Approval, or Done status; Draft is used since no
        # extra state transition is required for it.
        employee_cancel = cls._create_employee(
            "Tour Cash Advance Settlement Cancel Employee"
        )
        cash_advance_cancel = cls._create_open_cash_advance(employee_cancel)
        cls.settlement_cancel = cls._create_settlement(
            employee_cancel,
            cash_advance_cancel,
            "Tour Cash Advance Settlement Cancel Line",
        )

        # Fixture for the delete tour -- Pre-Condition: Draft status,
        # document number still "/".
        employee_delete = cls._create_employee(
            "Tour Cash Advance Settlement Delete Employee"
        )
        cash_advance_delete = cls._create_open_cash_advance(employee_delete)
        cls.settlement_delete = cls._create_settlement(
            employee_delete,
            cash_advance_delete,
            "Tour Cash Advance Settlement Delete Line",
        )

        # Fixture for the reject tour -- Pre-Condition: Waiting for
        # Approval status, reached in Python via action_confirm(), not
        # by clicking through the UI -- the reject tour itself clicks
        # Reject.
        employee_reject = cls._create_employee(
            "Tour Cash Advance Settlement Reject Employee"
        )
        cash_advance_reject = cls._create_open_cash_advance(employee_reject)
        cls.settlement_reject = cls._create_settlement(
            employee_reject,
            cash_advance_reject,
            "Tour Cash Advance Settlement Reject Line",
        )
        cls.settlement_reject.action_confirm()

        # Fixture for the restart tour -- Pre-Condition: Cancelled or
        # Rejected status; Rejected is used, reached in Python via
        # action_confirm() then action_reject_approval() (mirrors the
        # confirm->approve refresh dance above, T-04).
        employee_restart = cls._create_employee(
            "Tour Cash Advance Settlement Restart Employee"
        )
        cash_advance_restart = cls._create_open_cash_advance(employee_restart)
        cls.settlement_restart = cls._create_settlement(
            employee_restart,
            cash_advance_restart,
            "Tour Cash Advance Settlement Restart Line",
        )
        cls.settlement_restart.action_confirm()
        cls.settlement_restart.flush()
        cls.settlement_restart.invalidate_cache(ids=cls.settlement_restart.ids)
        cls.settlement_restart.action_reject_approval()

        # Fixture for the reset-number tour -- Pre-Condition: Draft
        # status.
        employee_reset_number = cls._create_employee(
            "Tour Cash Advance Settlement Reset Number Employee"
        )
        cash_advance_reset_number = cls._create_open_cash_advance(employee_reset_number)
        cls.settlement_reset_number = cls._create_settlement(
            employee_reset_number,
            cash_advance_reset_number,
            "Tour Cash Advance Settlement Reset Number Line",
        )

        # Fixture for the edit tour -- Pre-Condition: Draft status.
        # The settlement itself starts with NO lines while its cash
        # advance carries exactly one, distinctly-named line, so the
        # Reload from Cash Advance inline action
        # (docs/hr_cash_advance_settlement/02-edit.md "Inline
        # Actions:") produces a real, deterministic delta a tour gate
        # can bind to -- impossible to match before the click, certain
        # to match after (odoo-development-ui-test, patterns.md §P
        # uji lakmus), unlike an idempotent action with no delta to
        # gate on.
        employee_edit = cls._create_employee(
            "Tour Cash Advance Settlement Edit Employee"
        )
        cash_advance_edit = cls._create_open_cash_advance(employee_edit)
        cls.env["hr.cash_advance_line"].with_user(cls.admin).create(
            {
                "cash_advance_id": cash_advance_edit.id,
                "date_expense": "2026-01-01",
                "product_id": cls.product.id,
                "name": "Tour Cash Advance Settlement Edit Reload Marker",
                "usage_id": cls.usage_type.id,
                "account_id": cls.line_account.id,
                "price_unit": 50.0,
                "uom_quantity": 1.0,
                "uom_id": cls.product.uom_id.id,
            }
        )
        cls.settlement_edit = (
            cls.env["hr.cash_advance_settlement"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee_edit.id,
                    "type_id": cls.expense_type.id,
                    "cash_advance_id": cash_advance_edit.id,
                    "journal_id": cls.settlement_journal.id,
                    "date": "2026-01-15",
                }
            )
        )

    @classmethod
    def _create_employee(cls, name):
        """Create an employee with a home-address partner.

        :param name: unique employee name, also used as the tour's
            list-row marker
        :return: the created ``hr.employee``
        """
        partner = (
            cls.env["res.partner"].with_user(cls.admin).create({"name": name + " Home"})
        )
        return (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": name, "address_home_id": partner.id})
        )

    @classmethod
    def _create_open_cash_advance(cls, employee, name=False):
        """Create and open an ``hr.cash_advance`` for the given employee.

        Pushed to **Open** in Python via ``action_confirm()`` then
        ``action_approve_approval()`` -- Pre-Condition of every
        settlement tour ("At least one Cash Advance record in Open
        status exists for the employee"), not by clicking through the
        UI (Keputusan Desain, issue open-synergy/opnsynid-hr-expense#131).

        Between the two calls the record is flushed and its cache
        invalidated (scoped to its own ids). ``action_confirm()``'s
        policy check reads ``confirm_ok``, which -- via the shared
        ``mixin.policy`` compute -- also caches ``approve_ok`` at a
        moment this record's ``approval.approval`` row does not exist
        yet, so it caches ``False``. Without the refresh,
        ``action_approve_approval()`` reads that stale cached value
        and raises "Document is not allowed to approve" nondeterminis-
        tically, even though ``base.user_admin`` is a member of
        ``hr_cash_advance_validator_group`` and would otherwise be a
        valid approver (see ``odoo-development-unit-test`` skill,
        ``test-traps.md`` T-04, and ``odoo_yaml_test.case`` ``_refresh``
        on the 14.0 branch, which this mirrors).

        :param employee: ``hr.employee`` the record is submitted for
        :param name: optional manual document number; when set it
            survives sequence generation at Open (``mixin.sequence``
            only auto-generates while the field still holds the "/"
            placeholder), letting the create tour pick this record
            from the # Cash Advance dropdown by a literal string
        :return: the created ``hr.cash_advance``, in Open status
        """
        vals = {
            "employee_id": employee.id,
            "type_id": cls.expense_type.id,
            "journal_id": cls.ca_journal.id,
            "cash_advance_account_id": cls.ca_cash_advance_account.id,
            "payable_account_id": cls.ca_payable_account.id,
            "date": "2026-01-01",
            "date_due": "2026-01-31",
        }
        if name:
            vals["name"] = name
        cash_advance = cls.env["hr.cash_advance"].with_user(cls.admin).create(vals)
        cash_advance.action_confirm()
        # Force a fresh read of approve_ok -- see docstring above (T-04).
        cash_advance.flush()
        cash_advance.invalidate_cache(ids=cash_advance.ids)
        cash_advance.action_approve_approval()
        return cash_advance

    @classmethod
    def _create_settlement(cls, employee, cash_advance, line_name):
        """Create a draft ``hr.cash_advance_settlement`` with one line.

        Built entirely in Python (Pre-Condition setup), not by
        clicking through the UI, per Keputusan Desain (issue
        open-synergy/opnsynid-hr-expense#136).

        :param employee: ``hr.employee`` the record is submitted for
        :param cash_advance: the **Open** ``hr.cash_advance`` being
            settled
        :param line_name: description of the single detail line
        :return: the created ``hr.cash_advance_settlement``, in Draft
        """
        return (
            cls.env["hr.cash_advance_settlement"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": cls.expense_type.id,
                    "cash_advance_id": cash_advance.id,
                    "journal_id": cls.settlement_journal.id,
                    "date": "2026-01-15",
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "date_expense": "2026-01-15",
                                "product_id": cls.product.id,
                                "name": line_name,
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
        """Run the create tour for ``hr.cash_advance_settlement``.

        IK: docs/hr_cash_advance_settlement/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_settlement_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``hr.cash_advance_settlement``.

        IK: docs/hr_cash_advance_settlement/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_settlement_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``hr.cash_advance_settlement``.

        IK: docs/hr_cash_advance_settlement/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_settlement_approve",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``hr.cash_advance_settlement``.

        IK: docs/hr_cash_advance_settlement/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_settlement_cancel",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.cash_advance_settlement``.

        IK: docs/hr_cash_advance_settlement/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_settlement_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``hr.cash_advance_settlement``.

        IK: docs/hr_cash_advance_settlement/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_settlement_delete",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``hr.cash_advance_settlement``.

        IK: docs/hr_cash_advance_settlement/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_settlement_reject",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``hr.cash_advance_settlement``.

        IK: docs/hr_cash_advance_settlement/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_settlement_restart",
            login="admin",
        )

    def test_reset_number(self):
        """Run the reset document number tour for
        ``hr.cash_advance_settlement``.

        IK: docs/hr_cash_advance_settlement/13-reset-number.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_cash_advance_hr_cash_advance_settlement_reset_number",
            login="admin",
        )
