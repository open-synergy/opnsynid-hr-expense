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
        Expense Account** with no matching ``employee_expense_account``
        -- the Pre-Condition that makes this module's
        ``_check_expense_account`` (``pre_confirm_action`` hook,
        ``models/hr_reimbursement.py``) reject the Confirm action with
        "No expense account". All master data is built from scratch
        in Python (Keputusan Desain, issue
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
        """Run the Additional Validation delta tour for confirm.

        IK: docs/hr_reimbursement/04-confirm.md

        Navigation is the base IK Flow (open menu, open the record,
        click Confirm, click OK on the confirmation dialog); the
        assertion is this module's delta: the fixture line requires
        an expense account it does not have, so the server rejects
        Confirm with a visible warning dialog and the record stays in
        Draft. The tour does not read the warning's specific message
        text -- that remains unit-test territory
        (``odoo-development-unit-test``, ``expect_error``).
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_reimbursement_hr_reimbursement_confirm",
            login="admin",
        )
