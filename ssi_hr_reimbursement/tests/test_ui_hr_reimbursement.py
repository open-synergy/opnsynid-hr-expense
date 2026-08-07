# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrReimbursement(HttpSavepointCase):
    """Tour tests for the ``hr.reimbursement`` work instructions.

    Covers the base create/confirm/approve/cancel flow
    (``docs/hr_reimbursement/01-create.md``, ``04-confirm.md``,
    ``05-approve.md``, ``10-cancel.md``). All master data is built from
    scratch in ``setUpClass`` -- no demo data is relied upon.
    """

    @classmethod
    def setUpClass(cls):
        """Create shared master data and one fixture record per tour.

        Grants the Reimbursements menu group to ``admin`` (already
        implied by ``hr_reimbursement_validator_group`` membership from
        ``security/res_group_data.xml``, repeated here so the tour does
        not depend on that implication chain), then builds the
        accounting, product, and expense-type master data shared by all
        four tours, and one ``hr.reimbursement`` record per tour with a
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
        cls.expense_type = (
            cls.env["hr.expense_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour Reimbursement Type",
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
        # ``hr.reimbursement`` record via the UI.
        cls._create_employee_with_bank("Tour Reimbursement Create Employee")

        # Fixture for the confirm tour -- Pre-Condition: Draft status.
        employee_confirm, bank_confirm = cls._create_employee_with_bank(
            "Tour Reimbursement Confirm Employee"
        )
        cls.reimbursement_confirm = cls._create_reimbursement(
            employee_confirm, bank_confirm
        )

        # Fixture for the approve tour -- Pre-Condition: Waiting for
        # Approval status, reached in Python via ``action_confirm()``,
        # not by clicking through the UI.
        employee_approve, bank_approve = cls._create_employee_with_bank(
            "Tour Reimbursement Approve Employee"
        )
        cls.reimbursement_approve = cls._create_reimbursement(
            employee_approve, bank_approve
        )
        cls.reimbursement_approve.action_confirm()

        # Fixture for the cancel tour -- Pre-Condition: any of Draft,
        # Waiting for Approval, or In Progress status; Draft is used
        # since no extra state transition is required for it.
        employee_cancel, bank_cancel = cls._create_employee_with_bank(
            "Tour Reimbursement Cancel Employee"
        )
        cls.reimbursement_cancel = cls._create_reimbursement(
            employee_cancel, bank_cancel
        )

    @classmethod
    def _create_employee_with_bank(cls, name):
        """Create an employee and a bank account tied to its address.

        The bank account is linked to the employee's home-address
        contact, matching the domain ``mixin.employee_bank_account``
        uses to compute ``allowed_bank_account_ids``, so it appears as
        a selectable option for ``employee_bank_account_id``. The
        employee's own ``bank_account_id`` is left unset so the tour's
        manual Bank Account selection step is not a no-op.

        :param name: unique employee name, also used as the tour's
            list-row marker
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
                    "acc_number": "TOURRMBBANK" + str(employee.id),
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
