# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeBusinessTripDocumenso(HttpSavepointCase):
    """Tour test for the ``employee_business_trip`` Documenso signing delta."""

    @classmethod
    def setUpClass(cls):
        """Create one business trip already Waiting for Approval.

        ``base.user_admin`` is already a member of
        ``employee_business_trip_validator_group`` (which implies the
        ``User`` group) via ``ssi_employee_business_trip``'s
        ``security/res_group_data.xml``, so it can confirm the record
        directly, without extra group setup. The viewer grant is
        repeated explicitly below so the tour does not depend on that
        implication chain. The record is moved to ``confirm`` here in
        Python (``action_confirm()``), not via UI clicks, and the
        accounting/master data below is created from scratch rather than
        relying on demo data, per Keputusan Desain (issue
        open-synergy/opnsynid-hr-expense#106).
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_employee_business_trip.employee_business_trip_viewer_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

        account_type_payable = cls.env.ref("account.data_account_type_payable")
        payable_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Documenso Payable",
                    "code": "TOUREBTDPAY",
                    "user_type_id": account_type_payable.id,
                    "reconcile": True,
                }
            )
        )
        journal = (
            cls.env["account.journal"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Documenso Journal",
                    "code": "TEBTDJ",
                    "type": "general",
                }
            )
        )
        pricelist = (
            cls.env["product.pricelist"]
            .with_user(cls.admin)
            .create({"name": "Tour EBT Documenso Pricelist"})
        )
        indonesia = cls.env.ref("base.id")
        origin_city = (
            cls.env["res.city"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Documenso Origin City",
                    "country_id": indonesia.id,
                }
            )
        )
        destination_city = (
            cls.env["res.city"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Documenso Destination City",
                    "country_id": indonesia.id,
                }
            )
        )
        trip_type = (
            cls.env["employee_business_trip_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour EBT Documenso Trip Type",
                    "code": "TOUREBTDTYPE",
                    "journal_id": journal.id,
                    "payable_account_id": payable_account.id,
                }
            )
        )
        employee = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour EBT Documenso Employee Approve"})
        )

        # Pre-Condition IK 05-approve.md (delta): record already Waiting
        # for Approval. The "Standard" approval template used by
        # ssi_employee_business_trip demo data has no Documenso Signing
        # Template configured, so the Signature Requests tab is present
        # (``_documenso_signing_create_page = True``) but the base
        # Approve/OK Flow is unaffected -- this tour does not exercise it.
        cls.trip_approve = (
            cls.env["employee_business_trip"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": trip_type.id,
                    "date": "2026-01-01",
                    "date_due": "2026-01-31",
                    "date_start": "2026-01-05",
                    "date_end": "2026-01-07",
                    "origin_id": origin_city.id,
                    "destination_id": destination_city.id,
                    "pricelist_id": pricelist.id,
                    "journal_id": journal.id,
                    "payable_account_id": payable_account.id,
                }
            )
        )
        cls.trip_approve.action_confirm()

    def test_approve(self):
        """Run the approve tour for the Documenso signing delta.

        IK: docs/employee_business_trip/05-approve.md (E2a delta --
        Modified Flow)
        """
        self.start_tour(
            "/web",
            "ssi_employee_business_trip_documenso_signing_employee_business_trip_approve",
            login="admin",
        )
