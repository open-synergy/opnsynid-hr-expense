# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSSIEmployeeBusinessTripOperatingUnit(YamlTransactionCase):
    """Scenario tests for the business trip operating unit propagation."""

    def test_ssi_employee_business_trip_operating_unit(self):
        """Run the operating unit propagation scenarios."""
        self.run_yaml_scenario(
            "test_data_ssi_employee_business_trip_operating_unit.yaml"
        )

    def _create_business_trip(self, operating_unit=False, prefix="P3"):
        """Shared fixture for the python-pure test below. Built fresh
        here (not taken from the YAML registry, which only lives
        during ``run_yaml_scenario``).

        :param operating_unit: ``operating.unit`` record to assign, or
            ``False`` to leave it empty.
        :param prefix: string used to keep created records unique.
        :return: tuple ``(trip, per_diem)``.
        :rtype: tuple
        """
        payable_acc_type = self.env.ref("account.data_account_type_payable")
        expense_acc_type = self.env.ref("account.data_account_type_expenses")
        payable_account = self.env["account.account"].create(
            {
                "code": "%sP%d"
                % (prefix, self.env["account.account"].search_count([])),
                "name": "%s Business Trip OU Payable" % prefix,
                "user_type_id": payable_acc_type.id,
                "reconcile": True,
            }
        )
        per_diem_account = self.env["account.account"].create(
            {
                "code": "%sE%d"
                % (prefix, self.env["account.account"].search_count([])),
                "name": "%s Business Trip OU Per Diem Expense" % prefix,
                "user_type_id": expense_acc_type.id,
            }
        )
        journal = self.env["account.journal"].create(
            {
                "name": "%s Business Trip OU Journal" % prefix,
                "code": "%sJ%d"
                % (prefix, self.env["account.journal"].search_count([])),
                "type": "general",
            }
        )
        trip_type = self.env["employee_business_trip_type"].create(
            {
                "name": "%s Business Trip OU Type" % prefix,
                "code": "/",
                "journal_id": journal.id,
                "payable_account_id": payable_account.id,
            }
        )
        product = self.env["product.product"].create(
            {"name": "%s Business Trip OU Product" % prefix}
        )
        indonesia = self.env.ref("base.id")
        origin_city = self.env["res.city"].create(
            {
                "name": "%s Business Trip OU Origin" % prefix,
                "country_id": indonesia.id,
            }
        )
        destination_city = self.env["res.city"].create(
            {
                "name": "%s Business Trip OU Destination" % prefix,
                "country_id": indonesia.id,
            }
        )
        pricelist = self.env["product.pricelist"].create(
            {"name": "%s Business Trip OU Pricelist" % prefix}
        )
        employee_partner = self.env["res.partner"].create(
            {"name": "%s Business Trip OU Employee Address" % prefix}
        )
        employee = self.env["hr.employee"].create(
            {
                "name": "%s Business Trip OU Employee" % prefix,
                "address_home_id": employee_partner.id,
            }
        )
        trip = self.env["employee_business_trip"].create(
            {
                "employee_id": employee.id,
                "type_id": trip_type.id,
                "date": "2026-01-15",
                "date_due": "2026-02-15",
                "date_start": "2026-01-16",
                "date_end": "2026-01-18",
                "origin_id": origin_city.id,
                "destination_id": destination_city.id,
                "currency_id": self.env.company.currency_id.id,
                "pricelist_id": pricelist.id,
                "journal_id": journal.id,
                "payable_account_id": payable_account.id,
                "operating_unit_id": operating_unit.id if operating_unit else False,
            }
        )
        per_diem = self.env["employee_business_trip.per_diem"].create(
            {
                "employee_business_trip_id": trip.id,
                "name": "%s Per Diem Line" % prefix,
                "product_id": product.id,
                "account_id": per_diem_account.id,
                "uom_quantity": 1,
                "price_unit": 500000.0,
            }
        )
        return trip, per_diem

    def test_every_move_line_shares_the_business_trips_operating_unit(self):
        """Python murni -- pemicu P3 (L-06: perbandingan o2m berbasis
        `set`, tidak ada assert per-baris; membaca isi SETIAP baris
        `move_id.line_ids` butuh iterasi Python, tidak bisa diungkapkan
        sebagai satu assert YAML).

        Setelah `action_open`, baris hutang (dari
        `employee_business_trip`) maupun baris per diem (dari
        `employee_business_trip.per_diem`) pada `move_id.line_ids`
        harus seluruhnya membawa `operating_unit_id` yang sama dengan
        dokumen induknya -- bukan hanya salah satu baris.
        """
        ou_partner = self.env["res.partner"].create(
            {"name": "P3 Business Trip OU Partner"}
        )
        ou = self.env["operating.unit"].create(
            {
                "name": "P3 Business Trip Operating Unit",
                "code": "EBTOUP3",
                "partner_id": ou_partner.id,
            }
        )
        trip, _per_diem = self._create_business_trip(operating_unit=ou, prefix="P3")
        trip.with_context(bypass_policy_check=True).action_open()

        self.assertEqual(trip.state, "open")
        self.assertTrue(trip.move_id)
        self.assertTrue(trip.move_id.line_ids)

        for move_line in trip.move_id.line_ids:
            self.assertEqual(
                move_line.operating_unit_id,
                ou,
                "Move line %s does not carry the business trip's operating unit"
                % move_line.name,
            )
