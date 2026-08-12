# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models


class HrReimbursementLine(models.Model):
    """
    Detail line for employee reimbursement requests.
    Captures product, expense date, quantity, unit price, and account
    information for each expense item in the reimbursement.
    """

    _name = "hr.reimbursement_line"
    _inherit = [
        "mixin.product_line_account",
    ]
    _description = "Employee Reimbursement Line"

    reimbursement_id = fields.Many2one(
        string="# Reimbursement",
        comodel_name="hr.reimbursement",
        required=True,
        ondelete="cascade",
    )
    pricelist_id = fields.Many2one(
        related="reimbursement_id.pricelist_id",
        store=True,
        compute_sudo=True,
    )
    date_expense = fields.Date(
        string="Date Expense",
    )
    type_id = fields.Many2one(
        string="Type", related="reimbursement_id.type_id", compute_sudo=True
    )
    product_id = fields.Many2one(
        required=True,
    )

    @api.onchange(
        "allowed_pricelist_ids",
        "currency_id",
    )
    def onchange_pricelist_id(self):
        """Force a client-side refresh of the ``pricelist_id`` domain.

        Registered on ``allowed_pricelist_ids``/``currency_id`` so the
        UI re-evaluates the ``pricelist_id`` field's domain whenever
        either changes; the body is intentionally empty because the
        value itself is not reset here.

        :return: None
        """

    def _create_expense_move_line(self):
        """Create the expense ``account.move.line`` for this line.

        Uses ``_prepare_expense_move_lines`` to build the values and
        attaches the resulting line to the parent document's move.
        """
        self.ensure_one()
        obj_line = self.env["account.move.line"].with_context(check_move_validity=False)
        obj_line.create(self._prepare_expense_move_lines())

    def _prepare_expense_move_lines(self):
        """Build the expense ``account.move.line`` values.

        Extension point: override in a glue module to add fields
        without touching ``_create_expense_move_line``.

        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        reimbursement = self.reimbursement_id
        currency = reimbursement._get_currency()
        debit, credit, amount_currency = self._get_expense_amount()
        move_name = _(
            "Employee reimbursement %s: %s" % (reimbursement.name, self.product_id.name)
        )
        aa = self.analytic_account_id
        return {
            "name": move_name,
            "move_id": reimbursement.move_id.id,
            "partner_id": reimbursement._get_partner_id(),
            "account_id": self.account_id.id,
            "product_id": self.product_id.id,
            "quantity": self.uom_quantity,
            "price_unit": self.price_unit,
            "product_uom_id": self.uom_id and self.uom_id.id or False,
            "credit": credit,
            "debit": debit,
            "currency_id": currency and currency.id or False,
            "amount_currency": amount_currency,
            "analytic_account_id": aa and aa.id or False,
        }

    def _get_expense_amount(self):
        """Compute debit/credit/foreign amount for this expense line.

        Converts ``price_subtotal`` to company currency when the
        parent document has a foreign currency, then splits the
        result into debit or credit depending on its sign.

        :return: tuple ``(debit, credit, amount_currency)``
        """
        debit = credit = amount = amount_currency = 0.0
        reimbursement = self.reimbursement_id
        currency = reimbursement._get_currency()
        move_date = reimbursement.date
        if currency:
            amount_currency = self.price_subtotal
            amount = currency.with_context(date=move_date).compute(
                amount_currency,
                reimbursement.company_id.currency_id,
            )
        else:
            amount = self.price_subtotal

        if amount >= 0.0:
            debit = amount
        else:
            credit = amount
            amount_currency *= -1.0

        return debit, credit, amount_currency

    @api.onchange(
        "product_id",
    )
    def onchange_line_usage_id(self):
        self.usage_id = False
        if self.product_id:
            self.usage_id = self.type_id.default_product_usage_id.id
