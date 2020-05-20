# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class HrCashAdvance(models.Model):
    _name = "hr.cash_advance"
    _description = "Employee Advance Request"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "base.terminate.reason_common",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["approve"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    @api.model
    def _default_employee_id(self):
        employees = self.env.user.employee_ids
        if len(employees) > 0:
            return employees[0].id

    @api.multi
    def _compute_policy(self):
        _super = super(HrCashAdvance, self)
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
        "employee_advance_payable_move_line_id.reconcile_id",
        "employee_advance_payable_move_line_id.reconcile_partial_id",
        "employee_advance_payable_move_line_id",
        "amount_total",
        "state",
    )
    @api.multi
    def _compute_residual(self):
        for document in self:
            realized = 0.0
            residual = document.amount_total
            currency = document._get_currency()
            if document.employee_advance_payable_move_line_id:
                move_line = document.employee_advance_payable_move_line_id
                if not currency:
                    residual = move_line.amount_residual
                else:
                    residual = move_line.amount_residual_currency
                realized = document.amount_total - residual
            document.amount_realized = realized
            document.amount_residual = residual

    @api.depends(
        "employee_advance_move_line_id.reconcile_id",
        "employee_advance_move_line_id.reconcile_partial_id",
        "employee_advance_move_line_id",
        "state",
        "amount_total",
    )
    @api.multi
    def _compute_settlement(self):
        for document in self:
            currency = document._get_currency()
            settled = 0.0
            due = document.amount_total
            if document.employee_advance_move_line_id:
                move_line = document.employee_advance_move_line_id
                if not currency:
                    due = move_line.amount_residual
                else:
                    due = move_line.amount_residual_currency
                settled = document.amount_total - due
            document.amount_due = due
            document.amount_settled = settled

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
        required=True,
        default=lambda self: self._default_company_id(),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self._default_currency_id(),
        required=False,
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
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    manager_id = fields.Many2one(
        string="Manager",
        comodel_name="hr.employee",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    job_id = fields.Many2one(
        string="Job Position",
        comodel_name="hr.job",
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
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        related="type_id.allowed_product_categ_ids",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        related="type_id.allowed_product_ids",
    )
    date_request = fields.Date(
        string="Date Request",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_total = fields.Float(
        string="Total",
        compute="_compute_amount_total",
        store=True,
    )
    amount_realized = fields.Float(
        string="Total Payment",
        compute="_compute_residual",
        store=True,
    )
    amount_residual = fields.Float(
        string="Total Residual",
        compute="_compute_residual",
        store=True,
    )
    amount_settled = fields.Float(
        string="Total Realized",
        compute="_compute_settlement",
        store=True,
    )
    amount_due = fields.Float(
        string="Total Due",
        compute="_compute_settlement",
        store=True,
    )
    note = fields.Text(
        string="Note",
    )

    # Accounting Setting
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        domain=[
            ("type", "=", "general"),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    employee_advance_payable_account_id = fields.Many2one(
        string="Employee Advance Payable Account",
        comodel_name="account.account",
        domain=[
            ("reconcile", "=", True),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    employee_advance_account_id = fields.Many2one(
        string="Employee Advance Account",
        comodel_name="account.account",
        domain=[
            ("reconcile", "=", True),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    move_id = fields.Many2one(
        string="# Move",
        comodel_name="account.move",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    employee_advance_payable_move_line_id = fields.Many2one(
        string="Employee Advance Payable Move Line",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    employee_advance_move_line_id = fields.Many2one(
        string="Employee Advance Move Line",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    line_ids = fields.One2many(
        string="Advance Details",
        comodel_name="hr.cash_advance_line",
        inverse_name="advance_id",
        copy=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Waiting for Realization"),
            ("open", "Waiting for Settlement"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )
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
    open_user_id = fields.Many2one(
        string="Open By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    open_date = fields.Datetime(
        string="Open Date",
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
    def action_open(self):
        for document in self:
            document.write(document._prepare_open_data())

    @api.multi
    def action_done(self):
        for document in self:
            document.write(document._prepare_done_data())

    @api.multi
    def action_cancel(self):
        for document in self:
            move = document.move_id
            document.write(document._prepare_cancel_data())
            if move:
                move.unlink()

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
            "state": "approve",
            "approve_date": fields.Datetime.now(),
            "approve_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_done_data(self):
        self.ensure_one()
        return {
            "state": "done",
            "done_date": fields.Datetime.now(),
            "done_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_open_data(self):
        self.ensure_one()
        return {
            "state": "open",
            "open_date": fields.Datetime.now(),
            "open_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
            "move_id": False,
            "employee_advance_payable_move_line_id": False,
            "employee_advance_move_line_id": False,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "approve_date": False,
            "approve_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
        }

    @api.multi
    def _create_accounting_entry(self):
        self.ensure_one()
        self._create_account_move()
        self._create_payable_advance_move_line()
        self._create_advance_move_line()

    @api.multi
    def _create_account_move(self):
        self.ensure_one()
        obj_move = self.env["account.move"]
        move = obj_move.create(self._prepare_account_move())
        self.write({"move_id": move.id})

    @api.multi
    def _create_payable_advance_move_line(self):
        self.ensure_one()
        obj_line = self.env["account.move.line"]
        line = obj_line.create(
            self._prepare_payable_advance_move_lines())
        self.write({
            "employee_advance_payable_move_line_id": line.id})

    @api.multi
    def _create_advance_move_line(self):
        self.ensure_one()
        obj_line = self.env["account.move.line"]
        line = obj_line.create(
            self._prepare_advance_move_lines())
        self.write({
            "employee_advance_move_line_id": line.id})

    @api.multi
    def _get_currency(self):
        self.ensure_one()
        result = False
        if self.company_id.currency_id != self.currency_id:
            result = self.currency_id
        return result

    @api.multi
    def _get_advance_amount(self):
        debit = credit = amount = amount_currency = 0.0
        currency = self._get_currency()

        if currency:
            amount_currency = self.amount_total
            amount = currency.compute(
                amount_currency,
                self.company_id.currency_id,
            )
        else:
            amount = self.amount_total

        if amount >= 0.0:
            debit = amount
        else:
            credit = amount
            amount_currency *= -1.0

        return debit, credit, amount_currency

    @api.multi
    def _get_advance_payable_amount(self):
        debit = credit = amount = amount_currency = 0.0
        currency = self._get_currency()

        if currency:
            amount_currency = self.amount_total
            amount = currency.compute(
                amount_currency,
                self.company_id.currency_id,
            )
        else:
            amount = self.amount_total

        if amount < 0.0:
            debit = amount
        else:
            credit = amount
            amount_currency *= -1.0

        return debit, credit, amount_currency

    @api.multi
    def _prepare_account_move(self):
        self.ensure_one()
        period = self.env["account.period"].find(fields.Date.today())
        return {
            "date": fields.Date.today(),
            "journal_id": self.journal_id.id,
            "name": self.name,
            "period_id": period.id,
        }

    @api.multi
    def _get_move_line_name(self):
        self.ensure_one()
        return _("Cash advance %s" % (self.name))

    @api.multi
    def _prepare_advance_move_lines(self):
        self.ensure_one()
        currency = self._get_currency()
        debit, credit, amount_currency = self._get_advance_amount()
        return {
            "name": self._get_move_line_name(),
            "move_id": self.move_id.id,
            "partner_id": self._get_partner().id,
            "account_id": self.employee_advance_account_id.id,
            "credit": credit,
            "debit": debit,
            "currency_id": currency and currency.id or False,
            "amount_currency": amount_currency,
            "cash_advance_id": self.id,
        }

    @api.multi
    def _prepare_payable_advance_move_lines(self):
        self.ensure_one()
        currency = self._get_currency()
        debit, credit, amount_currency = self._get_advance_payable_amount()
        return {
            "name": self._get_move_line_name(),
            "move_id": self.move_id.id,
            "partner_id": self._get_partner().id,
            "account_id": self.employee_advance_payable_account_id.id,
            "debit": debit,
            "credit": credit,
            "currency_id": currency and currency.id or False,
            "amount_currency": amount_currency,
            "cash_advance_payable_id": self.id,
        }

    @api.multi
    def _get_partner(self):
        self.ensure_one()
        if not self.employee_id.address_home_id:
            err_msg = _("No home address defined for employee")
            raise UserError(err_msg)
        return self.employee_id.address_home_id

    @api.onchange(
        "type_id",
    )
    def onchange_journal_id(self):
        self.journal_id = False
        if self.type_id:
            self.journal_id = self.type_id.journal_id

    @api.onchange(
        "type_id",
        "employee_id",
    )
    def onchange_employee_advance_payable_account_id(self):
        result = False
        if self.employee_id:
            result = self.employee_id.employee_advance_payable_account_id

        if not result and self.type_id:
            result = self.type_id.employee_advance_payable_account_id

        self.employee_advance_payable_account_id = result

    @api.onchange(
        "type_id",
        "employee_id",
    )
    def onchange_employee_advance_account_id(self):
        result = False
        if self.employee_id:
            result = self.employee_id.employee_advance_account_id

        if not result and self.type_id:
            result = self.type_id.employee_advance_account_id

        self.employee_advance_account_id = result

    @api.onchange(
        "employee_id",
    )
    def onchange_department_id(self):
        self.department_id = False
        if self.employee_id:
            self.department_id = self.employee_id.department_id

    @api.onchange(
        "employee_id",
    )
    def onchange_manager_id(self):
        self.manager_id = False
        if self.employee_id:
            self.manager_id = self.employee_id.parent_id

    @api.onchange(
        "employee_id",
    )
    def onchange_job_id(self):
        self.job_id = False
        if self.employee_id:
            self.job_id = self.employee_id.job_id

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(HrCashAdvance, self)
        _super.unlink()

    @api.model
    def create(self, values):
        _super = super(HrCashAdvance, self)
        result = _super.create(values)
        sequence = result._create_sequence()
        result.write({
            "name": sequence,
        })
        return result

    @api.multi
    def validate_tier(self):
        _super = super(HrCashAdvance, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.action_approve()
