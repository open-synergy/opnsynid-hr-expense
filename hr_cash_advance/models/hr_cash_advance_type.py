# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class HrCashAdvanceType(models.Model):
    _name = "hr.cash_advance_type"
    _description = "Employee Cash Advance Type"

    name = fields.Char(
        string="Employee Cash Advance Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_emp_advance_type_2_product_categ",
        column1="type_id",
        column2="category_id",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        relation="rel_emp_advance_type_2_product",
        column1="type_id",
        column2="product_id",
    )

    # Cash Advance
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        company_dependent=True,
        required=True,
        domain=[
            ("type", "=", "general"),
        ],
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    employee_advance_payable_account_id = fields.Many2one(
        string="Employee Advance Payable Account",
        comodel_name="account.account",
        company_dependent=True,
        domain=[
            ("reconcile", "=", True),
        ],
        required=True,
    )
    employee_advance_account_id = fields.Many2one(
        string="Employee Advance Account",
        comodel_name="account.account",
        company_dependent=True,
        domain=[
            ("reconcile", "=", True),
        ],
        required=True,
    )
    cash_advance_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Cash Advance",
        comodel_name="res.groups",
        relation="rel_cash_advance_type_confirm_cash_advance",
        column1="type_id",
        column2="group_id",
    )
    cash_advance_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Cash Advance Approval",
        comodel_name="res.groups",
        relation="rel_cash_advance_type_restart_approval_cash_advance",
        column1="type_id",
        column2="group_id",
    )
    cash_advance_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Cash Advance",
        comodel_name="res.groups",
        relation="rel_cash_advance_type_cancel_cash_advance",
        column1="type_id",
        column2="group_id",
    )
    cash_advance_terminate_grp_ids = fields.Many2many(
        string="Allow To Terminate Cash Advance",
        comodel_name="res.groups",
        relation="rel_cash_advance_type_terminate_cash_advance",
        column1="type_id",
        column2="group_id",
    )
    cash_advance_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Cash Advance",
        comodel_name="res.groups",
        relation="rel_cash_advance_type_restart_cash_advance",
        column1="type_id",
        column2="group_id",
    )

    # Cash Advance Settlement
    cash_advance_settlement_journal_id = fields.Many2one(
        string="Cash Advance Settlement Journal",
        comodel_name="account.journal",
        company_dependent=True,
        domain=[
            ("type", "=", "general"),
        ],
    )
    cash_advance_sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    cash_advance_settlement_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Cash Advance Settlement",
        comodel_name="res.groups",
        relation="rel_cash_advance_type_confirm_ca_settlement",
        column1="type_id",
        column2="group_id",
    )
    cash_advance_settlement_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Cash Advance Settlement Approval",
        comodel_name="res.groups",
        relation="rel_cash_advance_type_restart_approval_ca_settlement",
        column1="type_id",
        column2="group_id",
    )
    cash_advance_settlement_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Cash Advance Settlement",
        comodel_name="res.groups",
        relation="rel_cash_advance_type_cancel_ca_settlement",
        column1="type_id",
        column2="group_id",
    )
    cash_advance_settlement_terminate_grp_ids = fields.Many2many(
        string="Allow To Terminate Cash Advance Settlement",
        comodel_name="res.groups",
        relation="rel_cash_advance_type_terminate_ca_settlement",
        column1="type_id",
        column2="group_id",
    )
    cash_advance_settlement_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Cash Advance Settlement",
        comodel_name="res.groups",
        relation="rel_cash_advance_type_restart_ca_settlement",
        column1="type_id",
        column2="group_id",
    )
