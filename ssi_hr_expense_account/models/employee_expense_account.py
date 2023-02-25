# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EmployeeExpenseAccount(models.Model):
    _name = "employee_expense_account"
    _description = "Employee Expense Account"
    _inherit = [
        "mixin.date_duration",
        "mixin.employee_document",
        "mixin.company_currency",
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    _statusbar_visible_label = "draft,open,confirm,done"

    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "open_ok",
        "done_ok",
        "manual_number_ok",
    ]

    _header_button_order = [
        "action_open",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    type_id = fields.Many2one(
        comodel_name="employee_expense_account_type",
        string="Type",
        required=True,
        ondelete="restrict",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        required=True,
        ondelete="restrict",
    )
    amount_limit = fields.Monetary(
        string="Amount Limit",
        required=True,
    )
    amount_realized = fields.Monetary(
        string="Amount Realized",
        compute="_compute_amount",
        store=True,
    )
    amount_residual = fields.Monetary(
        string="Amount Residual",
        compute="_compute_amount",
        store=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("terminate", "Terminate"),
            ("reject", "Rejected"),
        ],
    )

    @api.model
    def _get_policy_field(self):
        res = super(EmployeeExpenseAccount, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "terminate_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.depends("employee_id", "date_start", "date_end")
    def _compute_amount(self):
        for record in self:
            amount_realized = 0.0
            amount_residual = 0.0
            if not record.type_id:
                continue
            for expense_field in record.type_id.expense_field_ids:
                amount_realized = amount_realized + getattr(record, expense_field.name)
            amount_residual = amount_residual - amount_realized
            record.amount_realized = amount_realized
            record.amount_residual = amount_residual

    @api.constrains("employee_id", "date_start", "date_end")
    def constrains_expense_duration_overlap(self):
        for record in self.sudo():
            check = self.search(
                [
                    ("employee_id", "=", record.employee_id.id),
                    ("type_id", "=", record.type_id.id),
                    ("date_start", "<=", record.date_end),
                    ("date_end", ">=", record.date_start),
                ]
            )
            if check:
                error_message = _(
                    """
                    Employee: %s
                    Type: %s
                    Problem: Date start and date end can't overlap
                    Solution: Change date start and date end
                    """
                    % (record.employee_id.name, record.type_id.name)
                )
                raise UserError(error_message)
