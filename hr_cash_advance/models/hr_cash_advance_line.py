# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class HrCashAdvanceLine(models.Model):
    _name = "hr.cash_advance_line"
    _description = "Employee Cash Advance Request Line"

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

    advance_id = fields.Many2one(
        string="# Cash Advance",
        comodel_name="hr.cash_advance",
        ondelete="cascade",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        related="advance_id.employee_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
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
    type_id = fields.Many2one(
        string="Type",
        comodel_name="hr.cash_advance_type",
        related="advance_id.type_id",
        store=False,
    )
    advance_state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Waiting for Realization"),
            ("open", "Waiting for Settlement"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        related="advance_id.state",
        store=False,
    )

    @api.onchange(
        "product_id",
    )
    def onchange_uom_id(self):
        self.uom_id = False
        if self.product_id:
            self.uom_id = self.product_id.uom_id

    @api.onchange(
        "quantity",
    )
    def onchange_approve_quantity(self):
        self.approve_quantity = self.quantity

    @api.onchange(
        "price_unit",
    )
    def onchange_approve_price_unit(self):
        self.approve_price_unit = self.price_unit
