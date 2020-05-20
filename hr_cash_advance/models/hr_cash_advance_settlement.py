# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class HrCashAdvanceSettlement(models.Model):
    _name = "hr.cash_advance_settlement"
    _description = "Employee Cash Advance Settlement"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "base.terminate.reason_common",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["done"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_employee_id(self):
        employees = self.env.user.employee_ids
        if len(employees) > 0:
            return employees[0].id

    @api.multi
    def _compute_policy(self):
        _super = super(HrCashAdvanceSettlement, self)
        _super._compute_policy()

    @api.depends(
        "line_ids",
        "line_ids.price_subtotal",
    )
    @api.multi
    def _compute_amount_total(self):
        for document in self:
            total = 0.0
            for line in document.line_ids:
                total += line.price_subtotal
            document.amount_total = total

    @api.depends(
        "employee_id",
        "type_id",
    )
    def _compute_allowed_cash_advance_ids(self):
        obj_advance = self.env["hr.cash_advance"]
        for document in self:
            result = []
            if document.employee_id and document.type_id:
                criteria = [
                    ("type_id", "=", document.type_id.id),
                    ("employee_id", "=", document.employee_id.id),
                    ("state", "=", "open"),
                ]
                result = obj_advance.search(criteria).ids
            document.allowed_cash_advance_ids = result

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        copy=True,
        required=True,
        default=lambda self: self._default_company_id(),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="cash_advance_id.currency_id",
        readonly=True,
    )
    date_expense = fields.Date(
        string="Date Expense",
        copy=True,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="hr.cash_advance_type",
        copy=True,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_cash_advance_ids = fields.Many2many(
        string="Allowed Cash Advance",
        comodel_name="hr.cash_advance",
        compute="_compute_allowed_cash_advance_ids",
        store=False,
    )
    cash_advance_id = fields.Many2one(
        string="# Cash Advance",
        comodel_name="hr.cash_advance",
        copy=True,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        default=lambda self: self._default_employee_id(),
        copy=True,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    line_ids = fields.One2many(
        string="Realization Details",
        comodel_name="hr.cash_advance_settlement_line",
        inverse_name="settlement_id",
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    # Accounting Setting
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        domain=[
            ("type", "=", "general"),
        ],
        copy=True,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    move_id = fields.Many2one(
        string="# Expense Move",
        comodel_name="account.move",
        readonly=True,
    )
    employee_advance_move_line_id = fields.Many2one(
        string="Employee Advance Move Line",
        comodel_name="account.move.line",
        readonly=True,
    )
    amount_total = fields.Float(
        string="Total",
        compute="_compute_amount_total",
        store=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        copy=False,
        required=True,
        readonly=True,
    )
    # Log Fields
    # Log Fields
    confirm_date = fields.Datetime(
        string="Confirm Date",
        readonly=True,
        copy=False,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    approve_date = fields.Datetime(
        string="Approve Date",
        readonly=True,
        copy=False,
    )
    approve_user_id = fields.Many2one(
        string="Approve By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    done_date = fields.Datetime(
        string="Finish Date",
        readonly=True,
        copy=False,
    )
    done_user_id = fields.Many2one(
        string="Finished By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
        copy=False,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    terminate_date = fields.Datetime(
        string="Terminate Date",
        readonly=True,
        copy=False,
    )
    terminate_user_id = fields.Many2one(
        string="Terminated By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    # Policy Field
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    restart_approval_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )
    terminate_ok = fields.Boolean(
        string="Can Terminate",
        compute="_compute_policy",
    )

    @api.multi
    def action_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())
            document.request_validation()

    @api.multi
    def action_approve(self):
        for document in self:
            document.write(document._prepare_approve_data())
            document._create_accounting_entry()

    @api.multi
    def action_cancel(self):
        for document in self:
            document.write(document._prepare_cancel_data())
            document._unlink_accounting_entry()

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())
            document.restart_validation()

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_approve_data(self):
        self.ensure_one()
        return {
            "state": "done",
            "approve_date": fields.Datetime.now(),
            "approve_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
        }

    @api.multi
    def _create_accounting_entry(self):
        self.ensure_one()
        self._create_account_move()
        self._create_advance_move_line()
        for line in self.line_ids:
            line._create_accounting_entry()
        self._reconcile_advance()

    @api.multi
    def _reconcile_advance(self):
        self.ensure_one()
        lines = self.employee_advance_move_line_id + \
            self.cash_advance_id.employee_advance_move_line_id

        lines.reconcile_partial()

    @api.multi
    def _unlink_accounting_entry(self):
        self.ensure_one()
        self._unlink_account_move()

    @api.multi
    def _unlink_account_move(self):
        self.ensure_one()
        move = self.move_id
        obj_ml = self.env["account.move.line"]
        obj_ml._remove_move_reconcile(
            move_ids=[self.employee_advance_move_line_id.id])
        self.write({"move_id": False})
        move.unlink()

    @api.multi
    def _create_account_move(self):
        self.ensure_one()
        obj_move = self.env["account.move"]
        move = obj_move.create(self._prepare_account_move())
        self.write({"move_id": move.id})

    @api.multi
    def _prepare_account_move(self):
        self.ensure_one()
        period = self.env["account.period"].find(self.date_expense)
        return {
            "date": self.date_expense,
            "journal_id": self.journal_id.id,
            "name": self.name,
            "period_id": period.id,
        }

    @api.multi
    def _get_currency(self):
        self.ensure_one()
        result = False
        if self.company_id.currency_id != \
                self.currency_id:
            result = self.currency_id
        return result

    @api.multi
    def _get_advance_amount(self):
        debit = credit = amount_currency = 0.0
        currency = self._get_currency()

        if currency:
            amount_currency = self.amount_total
            amount = currency.with_context(date=self.date_expense).compute(
                amount_currency,
                self.company_id.currency_id,
            )
        else:
            amount = self.amount_total

        if amount >= 0.0:
            credit = amount
            amount_currency *= -1.0
        else:
            debit = amount

        return debit, credit, amount_currency

    @api.multi
    def _create_advance_move_line(self):
        self.ensure_one()
        obj_line = self.env["account.move.line"]
        line = obj_line.create(
            self._prepare_advance_move_lines())
        self.write({
            "employee_advance_move_line_id": line.id,
        })

    @api.multi
    def _get_partner(self):
        self.ensure_one()
        if not self.employee_id.address_home_id:
            err_msg = _("No home address defined for employee")
            raise UserError(err_msg)
        return self.employee_id.address_home_id

    @api.multi
    def _prepare_advance_move_lines(self):
        self.ensure_one()
        debit, credit, amount_currency = self._get_advance_amount()
        employee_advance_account = \
            self.cash_advance_id.employee_advance_account_id
        currency = self._get_currency()
        name = _("Settlement with %s" % (self.cash_advance_id.name))
        return {
            "name": name,
            "move_id": self.move_id.id,
            "partner_id": self._get_partner().id,
            "account_id": employee_advance_account.id,
            "debit": debit,
            "credit": credit,
            "currency_id": currency and currency.id or False,
            "amount_currency": amount_currency,
        }

    @api.onchange(
        "type_id",
    )
    def onchange_journal_id(self):
        self.journal_id = False
        if self.type_id:
            self.journal_id = self.type_id.cash_advance_settlement_journal_id

    @api.onchange(
        "type_id",
    )
    def onchange_cash_advance_id(self):
        self.cash_advance_id = False

    @api.onchange(
        "cash_advance_id",
    )
    def onchange_line_ids(self):
        self.update({"line_ids": [(5, 0, 0)]})

        if self.cash_advance_id:
            result = []
            for line in self.cash_advance_id.line_ids:
                result.append((0, 0, {
                    "sequence": line.sequence,
                    "line_id": line.id,
                    "quantity": line.quantity,
                    "price_unit": line.price_unit,
                    "uom_id": line.uom_id.id,
                }))
            self.update({"line_ids": result})

            for line in self.line_ids:
                line.onchange_account_id()
                line.onchange_approve_quantity()
                line.onchange_approve_price_unit()

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(HrCashAdvanceSettlement, self)
        _super.unlink()

    @api.model
    def create(self, values):
        _super = super(HrCashAdvanceSettlement, self)
        result = _super.create(values)
        sequence = result._create_sequence()
        result.write({
            "name": sequence,
        })
        return result

    @api.multi
    def validate_tier(self):
        _super = super(HrCashAdvanceSettlement, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.action_approve()
