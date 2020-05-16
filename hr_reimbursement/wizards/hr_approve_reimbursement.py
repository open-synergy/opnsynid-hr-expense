# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class HrApproveReimbursement(models.TransientModel):
    _name = "hr.approve_reimbursement"
    _description = "Approved Employee Reimbursement"

    @api.model
    def _default_reimbursement_id(self):
        return self.env.context.get("active_id", False)

    reimbursement_id = fields.Many2one(
        string="# Reimbursement",
        comodel_name="hr.reimbursement",
        default=lambda self: self._default_reimbursement_id(),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="reimbursement_id.currency_id",
        readonly=True,
    )
    line_ids = fields.One2many(
        string="Details",
        comodel_name="hr.approve_reimbursement_line",
        inverse_name="wizard_id",
    )

    @api.onchange(
        "reimbursement_id",
    )
    def onchange_line_ids(self):
        result = []
        if self.reimbursement_id:
            for line in self.reimbursement_id.line_ids:
                result.append((0, 0, {
                    "line_id": line.id,
                    "approve_price_unit": line.approve_price_unit,
                    "approve_quantity": line.approve_quantity,
                }))
            self.update({"line_ids": result})

    @api.multi
    def action_confirm(self):
        for document in self:
            document._update_amount()

    @api.multi
    def _update_amount(self):
        self.ensure_one()
        self.reimbursement_id.restart_validation()
        for line in self.line_ids:
            line.line_id.write({
                "approve_price_unit": line.approve_price_unit,
                "approve_quantity": line.approve_quantity,
            })


class HrApproveAdvanceDetailLine(models.TransientModel):
    _name = "hr.approve_reimbursement_line"
    _description = "Approved Employee Reimbursement Line"

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="hr.approve_reimbursement",
        ondelete="cascade",
    )
    line_id = fields.Many2one(
        string="Reimbursement Line",
        comodel_name="hr.reimbursement_line",
        ondelete="cascade",
        readonly=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        related="line_id.product_id",
        readonly=True,
        store=False,
    )
    price_unit = fields.Float(
        string="Unit Price",
        related="line_id.price_unit",
        store=False,
        readonly=True,
    )
    approve_price_unit = fields.Float(
        string="Approved Price Unit",
        required=True,
    )
    quantity = fields.Float(
        string="Quantity",
        related="line_id.quantity",
        store=False,
        readonly=True,
    )
    approve_quantity = fields.Float(
        string="Approved Quantity",
        required=True,
    )
