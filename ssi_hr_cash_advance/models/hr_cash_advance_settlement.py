# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrCashAdvanceSettlement(models.Model):
    _name = "hr.cash_advance_settlement"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.employee_document",
        "mixin.company_currency",
    ]
    _description = "Employee Cash Advance Settlement"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    # FIELD
    date = fields.Date(
        string="Date",
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
        comodel_name="hr.expense_type",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Product",
        comodel_name="product.product",
        related="type_id.allowed_product_ids",
        store=False,
    )
    allowed_product_category_ids = fields.Many2many(
        string="Allowed Product Category",
        comodel_name="product.category",
        related="type_id.allowed_product_category_ids",
        store=False,
    )

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self._default_currency_id(),
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "employee_id",
        "type_id",
    )
    def _compute_allowed_cash_advance_ids(self):
        CA = self.env["hr.cash_advance"]
        for record in self:
            result = []
            if record.employee_id and record.type_id:
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("type_id", "=", record.type_id.id),
                    ("state", "=", "open"),
                ]
                result = CA.search(criteria).ids
            record.allowed_cash_advance_ids = result

    allowed_cash_advance_ids = fields.Many2many(
        string="Allowed Cash Advance",
        comodel_name="hr.cash_advance",
        compute="_compute_allowed_cash_advance_ids",
        store=False,
        compute_sudo=True,
    )
    cash_advance_id = fields.Many2one(
        string="# Cash Advance",
        comodel_name="hr.cash_advance",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    # Accounting Configuration
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    move_id = fields.Many2one(
        string="# Journal Entry",
        comodel_name="account.move",
        readonly=True,
        ondelete="set null",
        copy=False,
    )
    cash_advance_move_line_id = fields.Many2one(
        string="Cash Advance Move Line",
        comodel_name="account.move.line",
        readonly=True,
        ondelete="set null",
        copy=False,
    )
    line_ids = fields.One2many(
        string="Details",
        comodel_name="hr.cash_advance_settlement_line",
        inverse_name="cash_advance_settlement_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        copy=True,
    )

    @api.depends(
        "line_ids",
        "line_ids.price_subtotal",
    )
    def _compute_amount_total(self):
        for document in self:
            amount_total = 0.0
            for line in document.line_ids:
                amount_total += line.price_total
            document.amount_total = amount_total

    amount_total = fields.Monetary(
        string="Amount Total",
        compute="_compute_amount_total",
        store=True,
        currency_field="currency_id",
    )
    state = fields.Selection(
        string="State",
        default="draft",
        required=True,
        readonly=True,
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
    )

    @api.model
    def _get_policy_field(self):
        res = super(HrCashAdvanceSettlement, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def action_done(self):
        _super = super(HrCashAdvanceSettlement, self)
        _super.action_done()
        for document in self.sudo():
            document._create_accounting_entry()

    def _create_accounting_entry(self):
        self.ensure_one()
        move = self._create_account_move()
        header_line = self._create_header_line(move)
        for line in self.line_ids:
            line._create_expense_line(move)
        pair = header_line + self.cash_advance_id.cash_advance_move_line_id
        self.write(
            {
                "move_id": move.id,
                "cash_advance_move_line_id": header_line.id,
            }
        )
        move.action_post()
        pair.reconcile()

    def _create_account_move(self):
        self.ensure_one()
        AccountMove = self.env["account.move"].with_context(check_move_validity=False)
        return AccountMove.create(self._prepare_create_account_move_data())

    def _prepare_create_account_move_data(self):
        self.ensure_one()
        data = {
            "name": self.name,
            "journal_id": self.journal_id.id,
            "date": self.date,
        }
        return data

    def _create_header_line(self, move):
        self.ensure_one()
        AML = self.env["account.move.line"].with_context(check_move_validity=False)
        return AML.create(self._prepare_create_header_line_data(move))

    def _get_currency(self):
        self.ensure_one()
        result = self.company_currency_id
        return result

    def _prepare_create_header_line_data(self, move):
        self.ensure_one()
        currency = self._get_currency()
        amount, amount_currency = self._get_header_amount(currency)
        move_name = _("Employee cash advance settlement %s" % (self.name))
        account = self.cash_advance_id.cash_advance_account_id
        data = {
            "name": move_name,
            "move_id": move.id,
            "partner_id": self._get_partner_id(),
            "account_id": account.id,
            "debit": 0.0,
            "credit": amount,
            "currency_id": currency and currency.id or False,
            "amount_currency": amount_currency,
        }
        return data

    def _get_header_amount(self, currency):
        self.ensure_one()
        amount = amount_currency = 0.0
        move_date = self.date

        if currency:
            amount_currency = self.amount_total
            amount = currency.with_context(date=move_date).compute(
                amount_currency,
                self.company_id.currency_id,
            )
        else:
            amount = self.amount_total

        return amount, amount_currency

    def _get_partner_id(self):
        self.ensure_one()
        if not self.employee_id.address_home_id:
            err_msg = _("No home address defined for employee")
            raise UserError(err_msg)
        return self.employee_id.address_home_id.id

    def action_cancel(self, cancel_reason=False):
        _super = super(HrCashAdvanceSettlement, self)
        _super.action_cancel(cancel_reason=cancel_reason)
        for document in self.sudo():
            document._delete_accounting_entry()

    def _delete_accounting_entry(self):
        self.ensure_one()
        if not self.move_id:
            return True

        self.cash_advance_move_line_id.remove_move_reconcile()

        if self.move_id.state == "posted":
            self.move_id.button_draft()
            self.move_id.button_cancel()

        self.move_id.with_context(force_delete=True).unlink()

    @api.onchange(
        "type_id",
    )
    def onchange_journal_id(self):
        self.journal_id = False
        if self.type_id and self.type_id.cash_advance_settlement_journal_id:
            self.journal_id = self.type_id.cash_advance_settlement_journal_id
