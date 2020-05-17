# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _


class HrCashAdvanceSettlementLine(models.Model):
    _name = "hr.cash_advance_settlement_line"
    _description = "Employee Cash Advance Settlement Line"

    @api.depends(
        "approve_quantity",
        "approve_price_unit",
    )
    @api.multi
    def _compute_price_subtotal(self):
        for document in self:
            document.price_subtotal = document.approve_quantity * \
                document.approve_price_unit

    @api.depends(
        "product_id",
    )
    @api.multi
    def _compute_allowed_uom_ids(self):
        obj_uom = self.env["product.uom"]
        for document in self:
            result = []
            if document.product_id:
                categ = document.product_id.uom_id.category_id
                criteria = [
                    ("category_id", "=", categ.id),
                ]
                result = obj_uom.search(criteria).ids
            document.allowed_uom_ids = result

    settlement_id = fields.Many2one(
        string="# Settlement",
        comodel_name="hr.cash_advance_settlement",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        related="settlement_id.employee_id",
        store=True,
    )
    line_id = fields.Many2one(
        string="CA Line",
        comodel_name="hr.cash_advance_line",
        readonly=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        related="line_id.product_id",
        readonly=True,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
    )
    price_unit = fields.Float(
        string="Unit Price",
        required=True,
    )
    approve_price_unit = fields.Float(
        string="Approved Price Unit",
        readonly=True,
    )
    quantity = fields.Float(
        string="Qty",
        required=True,
        default=1.0,
    )
    approve_quantity = fields.Float(
        string="Approved Quantity",
        readonly=True,
    )
    allowed_uom_ids = fields.Many2many(
        string="Allowed UoM",
        comodel_name="product.uom",
        compute="_compute_allowed_uom_ids",
        store=False,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        required=True,
    )
    price_subtotal = fields.Float(
        string="Subtotal",
        compute="_compute_price_subtotal",
        store=True,
    )

    @api.multi
    def _create_accounting_entry(self):
        self.ensure_one()
        self._create_expense_move_line()

    @api.multi
    def _prepare_expense_move_lines(self):
        self.ensure_one()
        settlement = self.settlement_id
        debit, credit, amount_currency = self._get_expense_amount()
        currency = settlement._get_currency()
        name = _("Settlement %s with %s" %
                 (settlement.name, self.product_id.name))
        return {
            "name": name,
            "move_id": settlement.move_id.id,
            "partner_id": settlement._get_partner().id,
            "account_id": self.account_id.id,
            "product_id": self.product_id.id,
            "quantity": self.approve_quantity,
            "debit": debit,
            "credit": credit,
            "currency_id": currency and currency.id or False,
            "amount_currency": amount_currency,
        }

    @api.multi
    def _get_expense_amount(self):
        debit = credit = amount = amount_currency = 0.0
        currency = self.settlement_id._get_currency()

        if currency:
            amount_currency = self.price_subtotal
            amount = currency.with_context(date=self.date_expense).compute(
                amount_currency,
                self.settlement_id.company_id.currency_id,
            )
        else:
            amount = self.price_subtotal

        if amount >= 0.0:
            debit = amount
        else:
            credit = amount

        return debit, credit, amount_currency

    @api.multi
    def _create_expense_move_line(self):
        self.ensure_one()
        obj_line = self.env["account.move.line"]
        obj_line.create(
            self._prepare_expense_move_lines())

    @api.onchange(
        "product_id",
    )
    def onchange_uom_id(self):
        self.uom_id = False
        if self.product_id:
            self.uom_id = self.product_id.uom_id

    @api.onchange(
        "product_id",
    )
    def onchange_account_id(self):
        result = False
        if self.product_id:
            result = self.product_id.property_account_expense

        if not result and \
                self.product_id:
            result = self.product_id.categ_id.property_account_expense_categ

        self.account_id = result

    @api.onchange(
        "price_unit",
    )
    def onchange_approve_price_unit(self):
        self.approve_price_unit = self.price_unit

    @api.onchange(
        "quantity",
    )
    def onchange_approve_quantity(self):
        self.approve_quantity = self.quantity
