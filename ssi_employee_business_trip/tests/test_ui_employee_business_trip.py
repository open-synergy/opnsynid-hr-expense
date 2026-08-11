# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeBusinessTrip(HttpSavepointCase):
    """Tour tests for the ``employee_business_trip`` work instructions.

    Covers create/edit/delete/confirm/approve/reject/cancel/restart/
    reset-number (``docs/employee_business_trip/01-create.md`` through
    ``13-reset-number.md``). All master data is built from scratch in
    ``setUpClass`` -- no demo data is relied upon.

    ``09-done.md`` is the one exception: the Done transition is purely
    automatic (``base.automation`` triggered by the ``realized`` field),
    so its tour drives no button -- it only prepares the Done state in
    Python and observes the result (odoo-development-ui-test,
    scope-and-boundaries.md §1 aturan 6).
    """

    @classmethod
    def setUpClass(cls):
        """Create shared master data and one fixture record per tour.

        Grants the Business Trips menu group to ``admin`` (already
        implied by ``employee_business_trip_validator_group`` membership
        from ``security/res_group_data.xml``, repeated here so the tour
        does not depend on that implication chain), then builds the
        accounting, type, city, product, and pricelist master data shared
        by all four tours, and one ``employee_business_trip`` record per
        tour with a unique employee name used as the list-row marker
        (Keputusan Desain, issue open-synergy/opnsynid-hr-expense#132).

        The approve tour's fixture is the only one given a Per Diem
        line: without one, ``_10_skip_open`` raises a ``UserError``
        instead of transitioning the record (bug tracked separately in
        issue #149, out of scope here).
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_employee_business_trip.employee_business_trip_viewer_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

        account_type_payable = cls.env.ref("account.data_account_type_payable")
        account_type_expenses = cls.env.ref("account.data_account_type_expenses")
        cls.payable_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Payable Account",
                    "code": "TOUREBTPAY",
                    "user_type_id": account_type_payable.id,
                    "reconcile": True,
                }
            )
        )
        cls.line_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Line Account",
                    "code": "TOUREBTLN",
                    "user_type_id": account_type_expenses.id,
                }
            )
        )
        cls.journal = (
            cls.env["account.journal"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Journal",
                    "code": "TEBTJ",
                    "type": "general",
                }
            )
        )
        # Config: default Selection Method ("Domain" with an empty "[]"
        # domain) on every Type selection field means any city, product,
        # currency, or pricelist qualifies -- no explicit domain
        # overrides are needed for the tour to find the records below.
        cls.trip_type = (
            cls.env["employee_business_trip_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Type",
                    "code": "TOUREBTTYPE",
                    "journal_id": cls.journal.id,
                    "payable_account_id": cls.payable_account.id,
                }
            )
        )
        cls.currency = (
            cls.env["res.currency"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "EBT",
                    "symbol": "E$",
                }
            )
        )
        cls.pricelist = (
            cls.env["product.pricelist"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Pricelist",
                    "currency_id": cls.currency.id,
                }
            )
        )
        country = cls.env.ref("base.us")
        cls.origin_city = (
            cls.env["res.city"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Origin City",
                    "country_id": country.id,
                }
            )
        )
        cls.destination_city = (
            cls.env["res.city"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Destination City",
                    "country_id": country.id,
                }
            )
        )
        cls.usage_type = (
            cls.env["product.usage_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Usage",
                    "code": "TOUREBTUSAGE",
                    "account_id": cls.line_account.id,
                }
            )
        )
        cls.product = (
            cls.env["product.product"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Product",
                    "type": "consu",
                }
            )
        )
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Cancel Reason",
                    "code": "TOUREBTCANCEL",
                    "global_use": True,
                }
            )
        )

        # Fixture for the create tour: only the master data the tour
        # picks from dropdowns is needed -- the tour itself creates the
        # ``employee_business_trip`` record via the UI.
        cls.employee_create = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour EBT Create Employee"})
        )

        # Fixture for the confirm tour -- Pre-Condition: Draft status.
        cls.employee_confirm = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour EBT Confirm Employee"})
        )
        cls.trip_confirm = cls._create_business_trip(cls.employee_confirm)

        # Fixture for the approve tour -- Pre-Condition: Waiting for
        # Approval status, reached in Python via ``action_confirm()``,
        # not by clicking through the UI. One Per Diem line is required
        # (Keputusan Desain, issue open-synergy/opnsynid-hr-expense#132).
        cls.employee_approve = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour EBT Approve Employee"})
        )
        cls.trip_approve = cls._create_business_trip(
            cls.employee_approve, with_per_diem=True
        )
        cls.trip_approve.with_user(cls.admin).action_confirm()

        # Fixture for the cancel tour -- Pre-Condition: any of Draft,
        # Waiting for Approval, or In Progress status; Draft is used
        # since no extra state transition is required for it.
        cls.employee_cancel = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour EBT Cancel Employee"})
        )
        cls.trip_cancel = cls._create_business_trip(cls.employee_cancel)

        # Fixture for the edit tour -- Pre-Condition: Draft status. A
        # second Type is the value the tour switches to; the model's
        # only ``type_id`` onchange touches Journal/Payable Account
        # (Config: Selection Method stays "Domain" with an empty "[]"
        # domain on every other Type field, so Origin/Destination/
        # Currency/Pricelist stay valid across the switch -- see
        # ``onchange_journal_id``/``onchange_payable_account_id`` in
        # models/employee_business_trip.py). The Per Diem line carries a
        # tax so the inline Compute Tax action
        # (docs/employee_business_trip/02-edit.md step 5) has something
        # to recompute.
        cls.trip_type_2 = (
            cls.env["employee_business_trip_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Edit Type 2",
                    "code": "TOUREBTTYPE2",
                    "journal_id": cls.journal.id,
                    "payable_account_id": cls.payable_account.id,
                }
            )
        )
        tax_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Tax Account",
                    "code": "TOUREBTTAX",
                    "user_type_id": account_type_expenses.id,
                }
            )
        )
        # ``account_id`` on the tax's own "tax" repartition line is what
        # ends up populating ``employee_business_trip.tax.account_id``
        # (required=True) when ``action_compute_tax`` calls
        # ``_recompute_standard_tax()`` -- without it, ``compute_all()``
        # returns no account and the auto-created tax row violates the
        # NOT NULL constraint (mirrors
        # tests/test_data_employee_business_trip_action_compute_tax.yaml).
        cls.tax = (
            cls.env["account.tax"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT VAT 10%",
                    "amount_type": "percent",
                    "amount": 10.0,
                    "type_tax_use": "purchase",
                    "invoice_repartition_line_ids": [
                        (0, 0, {"factor_percent": 100, "repartition_type": "base"}),
                        (
                            0,
                            0,
                            {
                                "factor_percent": 100,
                                "repartition_type": "tax",
                                "account_id": tax_account.id,
                            },
                        ),
                    ],
                    "refund_repartition_line_ids": [
                        (0, 0, {"factor_percent": 100, "repartition_type": "base"}),
                        (
                            0,
                            0,
                            {
                                "factor_percent": 100,
                                "repartition_type": "tax",
                                "account_id": tax_account.id,
                            },
                        ),
                    ],
                }
            )
        )
        cls.employee_edit = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour EBT Edit Employee"})
        )
        cls.trip_edit = cls._create_business_trip(
            cls.employee_edit, with_per_diem=True, tax_id=cls.tax.id
        )

        # Fixture for the delete tour -- Pre-Condition: Draft status,
        # document number still "/".
        cls.employee_delete = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour EBT Delete Employee"})
        )
        cls.trip_delete = cls._create_business_trip(cls.employee_delete)

        # Fixture for the reject tour -- Pre-Condition: Waiting for
        # Approval status, reached in Python via ``action_confirm()``,
        # same as the approve fixture above.
        cls.employee_reject = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour EBT Reject Employee"})
        )
        cls.trip_reject = cls._create_business_trip(cls.employee_reject)
        cls.trip_reject.with_user(cls.admin).action_confirm()

        # Fixture for the done tour -- Pre-Condition: In Progress status
        # with an accounting entry line. The Done transition itself is
        # reached exactly as the ``employee_business_trip_ready_2_done``
        # automation runs it (data/ir_actions_server_data.xml
        # ``employee_business_trip_action_done``): ``action_done()``
        # under ``bypass_policy_check`` context, no UI action drives it.
        # One Per Diem line is required so ``_10_skip_open`` does not
        # auto-finish the trip to Done on its own during approval
        # (mirrors the approve fixture above).
        cls.employee_done = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour EBT Done Employee"})
        )
        cls.trip_done = cls._create_business_trip(cls.employee_done, with_per_diem=True)
        cls.trip_done.with_user(cls.admin).action_confirm()
        # invalidate_cache() is required because approve_ok's
        # additional_python_code reads active_approver_user_ids, which is
        # computed from the approval.approval records action_confirm()
        # just created; without it the stale cached value from record
        # creation (still Draft) is reused (mirrors
        # ssi_hr_expense_account/tests/test_ui_employee_expense_account.py).
        cls.trip_done.invalidate_cache()
        cls.trip_done.with_user(cls.admin).action_approve_approval()
        cls.trip_done.with_context(bypass_policy_check=True).action_done()

        # Fixture for the restart tour -- Pre-Condition: Cancelled or
        # Rejected status; Rejected is used, reached in Python via
        # ``action_confirm()`` then ``action_reject_approval()``.
        cls.employee_restart = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour EBT Restart Employee"})
        )
        cls.trip_restart = cls._create_business_trip(cls.employee_restart)
        cls.trip_restart.with_user(cls.admin).action_confirm()
        # Same stale-cache reason as trip_done above, for reject_ok this
        # time.
        cls.trip_restart.invalidate_cache()
        cls.trip_restart.with_user(cls.admin).action_reject_approval()

        # Fixture for the reset document number tour -- Pre-Condition:
        # Draft status.
        cls.employee_reset_number = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour EBT Reset Number Employee"})
        )
        cls.trip_reset_number = cls._create_business_trip(cls.employee_reset_number)

    @classmethod
    def _create_business_trip(cls, employee, with_per_diem=False, tax_id=None):
        """Create a draft ``employee_business_trip`` for ``employee``.

        Built entirely in Python (Pre-Condition setup), not by clicking
        through the UI, per Keputusan Desain (issue
        open-synergy/opnsynid-hr-expense#132).

        :param employee: ``hr.employee`` the record is submitted for
        :param with_per_diem: when ``True``, add one Per Diem line
            using the shared product/usage/account fixtures
        :param tax_id: when given together with ``with_per_diem``, set
            it as the Per Diem line's ``tax_ids`` so the Compute Tax
            inline action has a tax to recompute from
        :return: the created ``employee_business_trip`` record, in Draft
        """
        values = {
            "employee_id": employee.id,
            "type_id": cls.trip_type.id,
            "date": "2026-01-01",
            "date_due": "2026-01-31",
            "date_start": "2026-01-01",
            "date_end": "2026-01-05",
            "origin_id": cls.origin_city.id,
            "destination_id": cls.destination_city.id,
            "currency_id": cls.currency.id,
            "pricelist_id": cls.pricelist.id,
            "journal_id": cls.journal.id,
            "payable_account_id": cls.payable_account.id,
        }
        if with_per_diem:
            per_diem_values = {
                "product_id": cls.product.id,
                "name": "Tour EBT Per Diem Line",
                "usage_id": cls.usage_type.id,
                "account_id": cls.line_account.id,
                "uom_quantity": 1.0,
                "uom_id": cls.product.uom_id.id,
                "price_unit": 100.0,
            }
            if tax_id:
                per_diem_values["tax_ids"] = [(6, 0, [tax_id])]
            values["per_diem_ids"] = [(0, 0, per_diem_values)]
        return cls.env["employee_business_trip"].with_user(cls.admin).create(values)

    def test_create(self):
        """Run the create tour for ``employee_business_trip``.

        IK: docs/employee_business_trip/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``employee_business_trip``.

        IK: docs/employee_business_trip/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``employee_business_trip``.

        IK: docs/employee_business_trip/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_approve",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``employee_business_trip``.

        IK: docs/employee_business_trip/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_cancel",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``employee_business_trip``.

        IK: docs/employee_business_trip/02-edit.md

        Inline Action ``action_compute_tax`` (Flow 5, optional) stops at
        asserting the button is visible and enabled; the tour does not
        click through its save+reload cycle. The fixture's Per Diem
        line's tax never changes, so the recompute is idempotent and
        has no data delta a gate could bind to, and the button's own
        enabled/disabled toggle is true both before and after the
        click -- no gate exists that passes the litmus test in
        odoo-development-ui-test, patterns.md §P, so per §Q this is a
        documented tour-can-only-approach-not-complete step.
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``employee_business_trip``.

        IK: docs/employee_business_trip/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_delete",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``employee_business_trip``.

        IK: docs/employee_business_trip/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_reject",
            login="admin",
        )

    def test_done(self):
        """Run the done tour for ``employee_business_trip``.

        IK: docs/employee_business_trip/09-done.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_done",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``employee_business_trip``.

        IK: docs/employee_business_trip/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_restart",
            login="admin",
        )

    def test_reset_number(self):
        """Run the reset document number tour for ``employee_business_trip``.

        IK: docs/employee_business_trip/13-reset-number.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_employee_business_trip_reset_number",
            login="admin",
        )
