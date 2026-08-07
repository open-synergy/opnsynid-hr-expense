# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrCashAdvanceSettlement(HttpSavepointCase):
    """Tour tests for the ``hr.cash_advance_settlement`` work instructions.

    Covers the base create/confirm/approve/cancel flow
    (``docs/hr_cash_advance_settlement/01-create.md``, ``04-confirm.md``,
    ``05-approve.md``, ``10-cancel.md``). All master data is built from
    scratch in ``setUpClass`` -- no demo data is relied upon, except the
    employee ``base.user_admin`` already resolves to via
    ``mixin.employee_document._default_employee_id`` (Keputusan Desain,
    issue open-synergy/opnsynid-hr-expense#136).
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
