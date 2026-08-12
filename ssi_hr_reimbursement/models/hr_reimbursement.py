# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class HrReimbursement(models.Model):
    """
    Transactional model for managing employee expense reimbursement requests.
    Supports a full approval workflow (draft → confirm → open → done/cancel)
    and integrates with accounting for journal entry and bank payment creation.
    """

    _name = "hr.reimbursement"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_pricelist",
        "mixin.many2one_configurator",
        "mixin.employee_bank_account",
        "mixin.company_currency",
    ]
    _description = "Employee Reimbursement"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "open_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

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
    date_due = fields.Date(
        string="Date Due",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.model
    def _default_currency_id(self):
        """Return the default currency for ``currency_id``.

        :return: the ``res.currency`` of the current user's company
        """
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
    pricelist_id = fields.Many2one(
        required=False,
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Product",
        comodel_name="product.product",
        related="type_id.allowed_product_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_product_category_ids = fields.Many2many(
        string="Allowed Product Category",
        comodel_name="product.category",
        related="type_id.allowed_product_category_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_product_usage_ids = fields.Many2many(
        string="Allowed Product Usage",
        comodel_name="product.usage_type",
        related="type_id.allowed_product_usage_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelists",
        comodel_name="product.pricelist",
        compute="_compute_allowed_pricelist_ids",
        store=False,
        compute_sudo=True,
    )
    line_ids = fields.One2many(
        string="Details",
        comodel_name="hr.reimbursement_line",
        inverse_name="reimbursement_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        copy=True,
    )
    duration_id = fields.Many2one(
        string="Duration",
        comodel_name="base.duration",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
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
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    payable_move_line_id = fields.Many2one(
        string="# Move Line Payable",
        comodel_name="account.move.line",
        readonly=True,
        ondelete="set null",
        copy=False,
    )
    move_id = fields.Many2one(
        string="# Move",
        comodel_name="account.move",
        readonly=True,
        ondelete="set null",
        copy=False,
    )
    last_payment_date = fields.Date(
        string="Last Payment Date",
        related="move_id.last_payment_date",
        compute_sudo=True,
    )

    @api.depends(
        "payable_move_line_id",
        "payable_move_line_id.matched_debit_ids",
        "payable_move_line_id.matched_credit_ids",
    )
    def _compute_reconciled(self):
        """Compute ``reconciled`` from the payable move line state.

        ``reconciled`` is ``True`` when ``payable_move_line_id`` is
        fully reconciled against matching debit/credit move lines.
        """
        for record in self:
            result = False
            if record.payable_move_line_id.reconciled:
                result = True
            record.reconciled = result

    reconciled = fields.Boolean(
        string="Reconciled",
        compute="_compute_reconciled",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "line_ids",
        "line_ids.price_subtotal",
    )
    def _compute_amount_total(self):
        """Compute ``amount_total`` as the sum of ``line_ids`` totals.

        Sums ``price_total`` of every detail line into the document
        ``amount_total``.
        """
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
        compute_sudo=True,
    )

    @api.depends(
        "amount_total",
        "state",
        "payable_move_line_id",
        "payable_move_line_id.reconciled",
        "payable_move_line_id.amount_residual",
        "payable_move_line_id.amount_residual_currency",
    )
    def _compute_residual(self):
        """Compute ``amount_realized`` and ``amount_residual``.

        Derives the realized/residual amount from the outstanding
        balance of ``payable_move_line_id`` (in company currency or
        document currency, depending on whether ``currency_id`` is
        set), falling back to the full ``amount_total`` as residual
        when the document has no payable move line yet.
        """
        for document in self:
            realized = 0.0
            residual = document.amount_total
            currency = document._get_currency()
            if document.payable_move_line_id:
                move_line = document.payable_move_line_id
                if not currency:
                    residual = -1.0 * move_line.amount_residual
                else:
                    residual = -1.0 * move_line.amount_residual_currency
                realized = document.amount_total - residual
            document.amount_realized = realized
            document.amount_residual = residual

    amount_realized = fields.Monetary(
        string="Amount Realized",
        compute="_compute_residual",
        store=True,
        currency_field="currency_id",
        compute_sudo=True,
    )
    amount_residual = fields.Monetary(
        string="Amount Residual",
        compute="_compute_residual",
        store=True,
        currency_field="currency_id",
        compute_sudo=True,
    )

    @api.depends(
        "type_id",
        "employee_id",
    )
    def _compute_allowed_analytic_account_ids(self):
        """Compute ``allowed_analytic_account_ids`` from ``type_id``.

        Delegates to the m2o configurator on ``type_id``
        (``analytic_account_selection_method``: manual/domain/code).
        When ``type_id`` is empty, falls back to ``search([])`` on
        ``account.analytic.account`` (every analytic account),
        matching the "no restriction" default of a fresh
        ``hr.expense_type`` (``selection_method="domain"``,
        ``domain="[]"``) rather than an empty result.
        """
        AnalyticAccount = self.env["account.analytic.account"]
        for document in self:
            result = AnalyticAccount.search([])
            if document.type_id:
                type_id = document.type_id
                result = document._m2o_configurator_get_filter(
                    object_name="account.analytic.account",
                    method_selection=type_id.analytic_account_selection_method,
                    manual_recordset=type_id.analytic_account_ids,
                    domain=type_id.analytic_account_domain,
                    python_code=type_id.analytic_account_python_code,
                )
            document.allowed_analytic_account_ids = result

    allowed_analytic_account_ids = fields.Many2many(
        string="Allowed Analytic Accounts",
        comodel_name="account.analytic.account",
        compute="_compute_allowed_analytic_account_ids",
        store=False,
        compute_sudo=True,
    )
    state = fields.Selection(
        string="State",
        default="draft",
        required=True,
        readonly=True,
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
    )

    @api.depends("type_id", "currency_id", "employee_id")
    def _compute_allowed_pricelist_ids(self):
        """Compute ``allowed_pricelist_ids`` from ``type_id``.

        Resolves the allowed pricelists through the m2o configurator
        of ``type_id`` (selection method, manual recordset, domain or
        Python code), then keeps only pricelists matching
        ``currency_id``.
        """
        for record in self:
            result = False
            if record.type_id and record.currency_id and record.employee_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.pricelist",
                    method_selection=record.type_id.pricelist_selection_method,
                    manual_recordset=record.type_id.pricelist_ids,
                    domain=record.type_id.pricelist_domain,
                    python_code=record.type_id.pricelist_python_code,
                )

                if result:
                    result = result.filtered(
                        lambda r: r.currency_id.id == record.currency_id.id
                    )
            record.allowed_pricelist_ids = result

    @api.model
    def _get_policy_field(self):
        res = super(HrReimbursement, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange(
        "duration_id",
        "date",
    )
    def onchange_date_due(self):
        """Recompute ``date_due`` from ``duration_id`` and ``date``.

        :return: None, sets ``date_due`` when ``duration_id`` is set
        """
        if self.duration_id:
            self.date_due = self.duration_id.get_duration(self.date)

    def action_recompute_realization(self):
        """Re-evaluate the realized/reconciled state of each record.

        Calls ``_recompute_realization`` (with ``sudo``) on every
        record in the current recordset, which may auto-transition
        the document between ``open`` and ``done``.
        """
        for record in self.sudo():
            record._recompute_realization()

    def _recompute_realization(self):
        """Auto-transition state based on ``reconciled``.

        Moves the document to ``done`` when it is ``open`` and fully
        ``reconciled``, or back to ``open`` when it is ``done`` and
        no longer ``reconciled``.
        """
        self.ensure_one()

        if self.state == "open" and self.reconciled:
            self.action_done()
        elif self.state == "done" and not self.reconciled:
            self.action_open()

    def _get_partner_id(self):
        """Resolve the partner used for the payable move line.

        :return: id of the employee's home address partner
        :raises UserError: when the employee has no home address
        """
        self.ensure_one()
        if not self.employee_id.address_home_id:
            err_msg = _("No home address defined for employee")
            raise UserError(err_msg)
        return self.employee_id.address_home_id.id

    def _get_currency(self):
        """Return the currency used to build the accounting entry.

        :return: the ``res.currency`` set on ``currency_id``
        """
        self.ensure_one()
        result = self.currency_id
        return result

    def _get_reimbursement_payable_amount(self, currency):
        """Compute debit/credit/foreign amount for the payable line.

        Converts ``amount_total`` to company currency when
        ``currency`` is set, then splits the result into debit or
        credit depending on its sign.

        :param currency: foreign ``res.currency``, or falsy
        :return: tuple ``(debit, credit, amount_currency)``
        """
        self.ensure_one()
        debit = credit = amount = amount_currency = 0.0
        move_date = self.date

        if currency:
            amount_currency = self.amount_total
            amount = currency.with_context(date=move_date).compute(
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

    def _prepare_account_move_data(self):
        """Build the ``account.move`` values for this document.

        Extension point: override in a glue module to add fields
        (e.g. operating unit) without touching ``_create_account_move``.

        :return: dict of ``account.move`` values
        """
        self.ensure_one()
        data = {
            "name": self.name,
            "ref": self.name,
            "journal_id": self.journal_id.id,
            "date": self.date,
        }
        return data

    def _prepare_payable_move_line_data(self):
        """Build the payable ``account.move.line`` values.

        Extension point: override in a glue module to add fields
        without touching ``_create_payable_reimbursement_move_line``.

        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        currency = self._get_currency()
        debit, credit, amount_currency = self._get_reimbursement_payable_amount(
            currency
        )
        move_name = _("Employee reimbursement %s" % (self.name))
        data = {
            "name": move_name,
            "move_id": self.move_id.id,
            "partner_id": self._get_partner_id(),
            "account_id": self.account_id.id,
            "debit": debit,
            "credit": credit,
            "currency_id": currency and currency.id or False,
            "amount_currency": amount_currency,
            "date_maturity": self.date_due,
        }
        return data

    def _create_accounting_entry(self):
        """Create and post the journal entry for this document.

        Creates ``move_id`` (if missing), the payable move line, an
        expense move line per detail line, then posts the move. Does
        nothing when ``move_id`` is already set.
        """
        self.ensure_one()
        if not self.move_id:
            self._create_account_move()
            self._create_payable_reimbursement_move_line()
            for line in self.line_ids:
                line._create_expense_move_line()
            self.move_id.action_post()

    def _create_account_move(self):
        """Create ``move_id`` from ``_prepare_account_move_data``.

        Does nothing when ``move_id`` is already set.
        """
        self.ensure_one()
        if not self.move_id:
            obj_move = self.env["account.move"].with_context(check_move_validity=False)
            move = obj_move.create(self._prepare_account_move_data())
            self.write({"move_id": move.id})

    def _create_payable_reimbursement_move_line(self):
        """Create ``payable_move_line_id`` on ``move_id``.

        Does nothing when ``payable_move_line_id`` is already set.
        """
        self.ensure_one()
        if not self.payable_move_line_id:
            obj_line = self.env["account.move.line"].with_context(
                check_move_validity=False
            )
            line = obj_line.create(self._prepare_payable_move_line_data())
            self.write({"payable_move_line_id": line.id})

    def action_open(self):
        """Confirm the document, then create its accounting entry.

        Overridden to call ``_create_accounting_entry`` after the
        base transition to ``open`` succeeds.
        """
        _super = super(HrReimbursement, self)
        _super.action_open()
        for document in self.sudo():
            document._create_accounting_entry()

    def action_cancel(self, cancel_reason=False):
        """Cancel the document and remove its accounting entry.

        Overridden to force-delete ``move_id`` (if any) after the
        base cancel transition succeeds, so a cancelled document
        leaves no dangling journal entry.
        """
        _super = super(HrReimbursement, self)
        _super.action_cancel()
        for document in self.sudo():
            if document.move_id:
                document.move_id.with_context(force_delete=True).unlink()

    @api.onchange(
        "type_id",
    )
    def onchange_journal_id(self):
        self.journal_id = False
        if self.type_id and self.type_id.reimbursement_journal_id:
            self.journal_id = self.type_id.reimbursement_journal_id

    @api.onchange(
        "type_id",
    )
    def onchange_account_id(self):
        self.account_id = False
        if self.type_id and self.type_id.reimbursement_account_id:
            self.account_id = self.type_id.reimbursement_account_id

    @api.onchange(
        "type_id",
    )
    def onchange_line_usage_id(self):
        self.line_ids.usage_id = False
        if self.type_id:
            self.line_ids.usage_id = self.type_id.default_product_usage_id.id

    @api.onchange(
        "type_id",
    )
    def onchange_line_analytic_account_id(self):
        if self.type_id:
            self.line_ids.analytic_account_id = False

    @api.onchange(
        "employee_id",
        "type_id",
        "currency_id",
    )
    def onchange_pricelist_id(self):
        self.pricelist_id = False

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
