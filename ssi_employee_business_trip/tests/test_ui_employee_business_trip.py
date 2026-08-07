# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeBusinessTrip(HttpSavepointCase):
    """Tour tests for the ``employee_business_trip`` work instructions.

    Covers the base create/confirm/approve/cancel flow
    (``docs/employee_business_trip/01-create.md``, ``04-confirm.md``,
    ``05-approve.md``, ``10-cancel.md``). All master data is built from
    scratch in ``setUpClass`` -- no demo data is relied upon. There is no
    tour for ``09-done.md``: the Done transition is purely automatic
    (``base.automation`` triggered by the ``realized`` field), so no
    button exists to drive from the UI.
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

    @classmethod
    def _create_business_trip(cls, employee, with_per_diem=False):
        """Create a draft ``employee_business_trip`` for ``employee``.

        Built entirely in Python (Pre-Condition setup), not by clicking
        through the UI, per Keputusan Desain (issue
        open-synergy/opnsynid-hr-expense#132).

        :param employee: ``hr.employee`` the record is submitted for
        :param with_per_diem: when ``True``, add one Per Diem line
            using the shared product/usage/account fixtures
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
            values["per_diem_ids"] = [
                (
                    0,
                    0,
                    {
                        "product_id": cls.product.id,
                        "name": "Tour EBT Per Diem Line",
                        "usage_id": cls.usage_type.id,
                        "account_id": cls.line_account.id,
                        "uom_quantity": 1.0,
                        "uom_id": cls.product.uom_id.id,
                        "price_unit": 100.0,
                    },
                )
            ]
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
