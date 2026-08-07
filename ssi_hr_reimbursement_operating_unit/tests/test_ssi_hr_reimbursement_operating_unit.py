# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSSIHrReimbursementOperatingUnit(YamlTransactionCase):
    """Scenario tests for the reimbursement operating unit propagation."""

    def test_ssi_hr_reimbursement_operating_unit(self):
        """Run the operating unit propagation scenarios."""
        self.run_yaml_scenario("test_data_ssi_hr_reimbursement_operating_unit.yaml")

    def _create_reimbursement(self, operating_unit=False, prefix="P3"):
        """Shared fixture for the python-pure test below. Built fresh
        here (not taken from the YAML registry, which only lives
        during ``run_yaml_scenario``).

        :param operating_unit: ``operating.unit`` record to assign, or
            ``False`` to leave it empty.
        :param prefix: string used to keep created records unique.
        :return: tuple ``(reimbursement, line)``.
        :rtype: tuple
        """
        payable_acc_type = self.env.ref("account.data_account_type_payable")
        expense_acc_type = self.env.ref("account.data_account_type_expenses")
        payable_account = self.env["account.account"].create(
            {
                "code": "%sP%d"
                % (prefix, self.env["account.account"].search_count([])),
                "name": "%s Reimbursement OU Payable" % prefix,
                "user_type_id": payable_acc_type.id,
                "reconcile": True,
            }
        )
        expense_account = self.env["account.account"].create(
            {
                "code": "%sE%d"
                % (prefix, self.env["account.account"].search_count([])),
                "name": "%s Reimbursement OU Expense" % prefix,
                "user_type_id": expense_acc_type.id,
            }
        )
        journal = self.env["account.journal"].create(
            {
                "name": "%s Reimbursement OU Journal" % prefix,
                "code": "%sJ%d"
                % (prefix, self.env["account.journal"].search_count([])),
                "type": "general",
            }
        )
        expense_type = self.env["hr.expense_type"].create(
            {
                "name": "%s Reimbursement OU Type" % prefix,
                "code": "/",
                "reimbursement_journal_id": journal.id,
                "reimbursement_account_id": payable_account.id,
            }
        )
        product = self.env["product.product"].create(
            {"name": "%s Reimbursement OU Product" % prefix}
        )
        employee_partner = self.env["res.partner"].create(
            {"name": "%s Reimbursement OU Employee Address" % prefix}
        )
        employee = self.env["hr.employee"].create(
            {
                "name": "%s Reimbursement OU Employee" % prefix,
                "address_home_id": employee_partner.id,
            }
        )
        reimbursement = self.env["hr.reimbursement"].create(
            {
                "employee_id": employee.id,
                "date": "2026-01-15",
                "date_due": "2026-02-15",
                "type_id": expense_type.id,
                "journal_id": journal.id,
                "account_id": payable_account.id,
                "operating_unit_id": operating_unit.id if operating_unit else False,
            }
        )
        line = self.env["hr.reimbursement_line"].create(
            {
                "reimbursement_id": reimbursement.id,
                "name": "%s Line 1" % prefix,
                "product_id": product.id,
                "account_id": expense_account.id,
                "uom_quantity": 1,
                "price_unit": 100000.0,
            }
        )
        return reimbursement, line

    def test_every_move_line_shares_the_reimbursements_operating_unit(self):
        """Python murni -- pemicu P3 (L-06: perbandingan o2m berbasis
        `set`, tidak ada assert per-baris; membaca isi SETIAP baris
        `move_id.line_ids` butuh iterasi Python, tidak bisa diungkapkan
        sebagai satu assert YAML).

        Setelah `action_open`, baris hutang (dari `hr.reimbursement`)
        maupun baris beban (dari `hr.reimbursement_line`) pada
        `move_id.line_ids` harus seluruhnya membawa `operating_unit_id`
        yang sama dengan dokumen induknya -- bukan hanya salah satu
        baris.
        """
        ou_partner = self.env["res.partner"].create(
            {"name": "P3 Reimbursement OU Partner"}
        )
        ou = self.env["operating.unit"].create(
            {
                "name": "P3 Reimbursement Operating Unit",
                "code": "RMOUP3",
                "partner_id": ou_partner.id,
            }
        )
        reimbursement, _line = self._create_reimbursement(
            operating_unit=ou, prefix="P3"
        )
        reimbursement.with_context(bypass_policy_check=True).action_open()

        self.assertEqual(reimbursement.state, "open")
        self.assertTrue(reimbursement.move_id)
        self.assertTrue(reimbursement.move_id.line_ids)

        for move_line in reimbursement.move_id.line_ids:
            self.assertEqual(
                move_line.operating_unit_id,
                ou,
                "Move line %s does not carry the reimbursement's operating unit"
                % move_line.name,
            )
