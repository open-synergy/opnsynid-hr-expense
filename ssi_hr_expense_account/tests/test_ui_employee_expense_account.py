# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeExpenseAccount(HttpSavepointCase):
    """Tour tests for ``employee_expense_account`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Prepare the master data and per-tour state fixtures.

        Creates the expense account type, currency, cancel/terminate
        reasons, and one uniquely named employee per tour (used as the
        row marker in the list). The confirm, approve, cancel, and
        terminate tours each get their own record already sitting at
        the Pre-Condition state their IK expects, reached by calling
        the workflow actions directly instead of clicking through the
        UI.
        """
        super().setUpClass()
        admin = cls.env.ref("base.user_admin")
        cls.expense_type = (
            cls.env["employee_expense_account_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Tour EEA Expense Type",
                    "code": "/",
                }
            )
        )
        cls.currency = (
            cls.env["res.currency"]
            .with_user(admin)
            .create(
                {
                    "name": "TUR",
                    "symbol": "T$",
                }
            )
        )
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(admin)
            .create(
                {
                    "name": "Tour Cancel Reason",
                    "code": "TOURCANCEL",
                    "global_use": True,
                }
            )
        )
        cls.terminate_reason = (
            cls.env["base.terminate_reason"]
            .with_user(admin)
            .create(
                {
                    "name": "Tour Terminate Reason",
                    "code": "TOURTERMINATE",
                    "global_use": True,
                }
            )
        )
        cls.employee_confirm = (
            cls.env["hr.employee"]
            .with_user(admin)
            .create({"name": "Tour EEA Employee Confirm"})
        )
        cls.employee_approve = (
            cls.env["hr.employee"]
            .with_user(admin)
            .create({"name": "Tour EEA Employee Approve"})
        )
        cls.employee_cancel = (
            cls.env["hr.employee"]
            .with_user(admin)
            .create({"name": "Tour EEA Employee Cancel"})
        )
        cls.employee_terminate = (
            cls.env["hr.employee"]
            .with_user(admin)
            .create({"name": "Tour EEA Employee Terminate"})
        )
        # The create tour picks this employee from the UI, so it does
        # not need a matching employee_expense_account fixture.
        cls.env["hr.employee"].with_user(admin).create(
            {"name": "Tour EEA Employee Create"}
        )

        common_values = {
            "type_id": cls.expense_type.id,
            "currency_id": cls.currency.id,
            "date_start": "2026-01-01",
            "date_end": "2026-12-31",
            "amount_limit": 1000.0,
        }

        # Pre-Condition (04-confirm.md): record is in Draft.
        cls.confirm_record = (
            cls.env["employee_expense_account"]
            .with_user(admin)
            .create(dict(common_values, employee_id=cls.employee_confirm.id))
        )

        # Pre-Condition (05-approve.md): record is Waiting for Approval.
        cls.approve_record = (
            cls.env["employee_expense_account"]
            .with_user(admin)
            .create(dict(common_values, employee_id=cls.employee_approve.id))
        )
        cls.approve_record.with_user(admin).action_confirm()

        # Pre-Condition (10-cancel.md): Draft is the simplest state the
        # IK allows for cancellation.
        cls.cancel_record = (
            cls.env["employee_expense_account"]
            .with_user(admin)
            .create(dict(common_values, employee_id=cls.employee_cancel.id))
        )

        # Pre-Condition (11-terminate.md): In Progress is the earliest
        # state the IK allows for termination, and the only state where
        # the Terminate button is guaranteed to be shown.
        cls.terminate_record = (
            cls.env["employee_expense_account"]
            .with_user(admin)
            .create(dict(common_values, employee_id=cls.employee_terminate.id))
        )
        cls.terminate_record.with_user(admin).action_confirm()
        # invalidate_cache() is required because approve_ok's
        # additional_python_code reads active_approver_user_ids, which
        # is computed from the approval.approval records action_confirm()
        # just created; without it the stale cached value from record
        # creation (still Draft) is reused.
        cls.terminate_record.invalidate_cache()
        cls.terminate_record.with_user(admin).action_approve_approval()

    def test_create(self):
        """Run the create tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_employee_expense_account_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_employee_expense_account_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_employee_expense_account_approve",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_employee_expense_account_cancel",
            login="admin",
        )

    def test_terminate(self):
        """Run the terminate tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/11-terminate.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_employee_expense_account_terminate",
            login="admin",
        )
