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
        row marker in the list). The confirm, approve, reject, cancel,
        terminate, restart, and finish/start tours each get their own
        record already sitting at the Pre-Condition state their IK
        expects, reached by calling the workflow actions directly
        instead of clicking through the UI.
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
        cls.employee_edit = (
            cls.env["hr.employee"]
            .with_user(admin)
            .create({"name": "Tour EEA Employee Edit"})
        )
        cls.employee_delete = (
            cls.env["hr.employee"]
            .with_user(admin)
            .create({"name": "Tour EEA Employee Delete"})
        )
        cls.employee_reject = (
            cls.env["hr.employee"]
            .with_user(admin)
            .create({"name": "Tour EEA Employee Reject"})
        )
        cls.employee_finish = (
            cls.env["hr.employee"]
            .with_user(admin)
            .create({"name": "Tour EEA Employee Finish"})
        )
        cls.employee_start = (
            cls.env["hr.employee"]
            .with_user(admin)
            .create({"name": "Tour EEA Employee Start"})
        )
        cls.employee_restart = (
            cls.env["hr.employee"]
            .with_user(admin)
            .create({"name": "Tour EEA Employee Restart"})
        )
        cls.employee_reset_number = (
            cls.env["hr.employee"]
            .with_user(admin)
            .create({"name": "Tour EEA Employee Reset Number"})
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

        # Pre-Condition (02-edit.md): record is in Draft.
        cls.edit_record = (
            cls.env["employee_expense_account"]
            .with_user(admin)
            .create(dict(common_values, employee_id=cls.employee_edit.id))
        )

        # Pre-Condition (03-delete.md): record is Draft, document number
        # still "/" (not yet generated).
        cls.delete_record = (
            cls.env["employee_expense_account"]
            .with_user(admin)
            .create(dict(common_values, employee_id=cls.employee_delete.id))
        )

        # Pre-Condition (06-reject.md): record is Waiting for Approval.
        cls.reject_record = (
            cls.env["employee_expense_account"]
            .with_user(admin)
            .create(dict(common_values, employee_id=cls.employee_reject.id))
        )
        cls.reject_record.with_user(admin).action_confirm()

        # Pre-Condition (13-reset-number.md): record is Draft.
        cls.reset_number_record = (
            cls.env["employee_expense_account"]
            .with_user(admin)
            .create(dict(common_values, employee_id=cls.employee_reset_number.id))
        )

        # Pre-Condition (12-restart.md): record is Cancelled. Reached
        # directly via ``action_cancel()`` from Draft (mixin.transaction
        # allows cancelling from Draft), no approval chain involved so
        # no ``invalidate_cache()`` is needed here.
        cls.restart_record = (
            cls.env["employee_expense_account"]
            .with_user(admin)
            .create(dict(common_values, employee_id=cls.employee_restart.id))
        )
        cls.restart_record.with_user(admin).action_cancel(cls.cancel_reason)

        # Pre-Condition (09-finish.md): record is In Progress (Open),
        # then transitioned to Done exactly as the
        # ``employee_expense_account_to_done`` automation would run it
        # (data/base_automation_data.xml / data/ir_actions_server_data.xml):
        # ``action_done()`` under ``bypass_policy_check`` context, no UI
        # action drives it (odoo-development-ui-test,
        # scope-and-boundaries.md §1 aturan 6).
        cls.finish_record = (
            cls.env["employee_expense_account"]
            .with_user(admin)
            .create(dict(common_values, employee_id=cls.employee_finish.id))
        )
        cls.finish_record.with_user(admin).action_confirm()
        cls.finish_record.invalidate_cache()
        cls.finish_record.with_user(admin).action_approve_approval()
        cls.finish_record.with_context(bypass_policy_check=True).action_done()

        # Pre-Condition (07-start.md): record is Done, then transitioned
        # back to In Progress exactly as the
        # ``employee_expense_account_to_open`` automation would run it,
        # under ``bypass_policy_check`` context (same reasoning as
        # ``finish_record`` above -- ``open_ok`` has no policy template
        # detail configured for this model, so calling ``action_open()``
        # would otherwise always be rejected regardless of user).
        cls.start_record = (
            cls.env["employee_expense_account"]
            .with_user(admin)
            .create(dict(common_values, employee_id=cls.employee_start.id))
        )
        cls.start_record.with_user(admin).action_confirm()
        cls.start_record.invalidate_cache()
        cls.start_record.with_user(admin).action_approve_approval()
        cls.start_record.with_context(bypass_policy_check=True).action_done()
        cls.start_record.with_context(bypass_policy_check=True).action_open()

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

    def test_edit(self):
        """Run the edit tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_employee_expense_account_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_employee_expense_account_delete",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_employee_expense_account_reject",
            login="admin",
        )

    def test_start(self):
        """Run the start tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/07-start.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_employee_expense_account_start",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_employee_expense_account_finish",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_employee_expense_account_restart",
            login="admin",
        )

    def test_reset_number(self):
        """Run the reset document number tour for ``employee_expense_account``.

        IK: docs/employee_expense_account/13-reset-number.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_expense_account_employee_expense_account_reset_number",
            login="admin",
        )
