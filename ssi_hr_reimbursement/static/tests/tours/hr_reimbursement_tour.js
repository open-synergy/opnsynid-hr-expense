/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_hr_reimbursement.hr_reimbursement_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block, reused verbatim by every tour below --
    // Flow step 1 of every IK in docs/hr_reimbursement/: "Open the Human
    // Resource > Expense > Reimbursements menu." "Expense" is a section
    // menuitem (has its own data-menu-xmlid, not a grouping header), so
    // it is its own step (odoo-development-ui-test, patterns.md §A).
    function openReimbursementsList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Expense menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_expense.expense_menu"]',
            },
            {
                content: "Open the Reimbursements menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_reimbursement.hr_reimbursement_menu"]',
            },
            {
                // Gate: wait for the Reimbursements action to actually be
                // mounted, not just any list view left over from the
                // landing action (odoo-development-ui-test, patterns.md
                // §A).
                content: "Reimbursements list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Reimbursements)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ];
    }

    // IK: docs/hr_reimbursement/01-create.md
    tour.register(
        "ssi_hr_reimbursement_hr_reimbursement_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openReimbursementsList(), [
            // Flow 2 — Click the New button.
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Fill in the required fields in the header.
            // Currency keeps its default (company currency); the
            // Pricelist and Duration fields are optional and are
            // intentionally skipped (Keputusan Desain, issue
            // open-synergy/opnsynid-hr-expense#130).
            {
                content: "Select the Employee",
                trigger: ".o_field_many2one[name='employee_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour Reimbursement Create Employee",
            },
            {
                content: "Pick the employee from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Reimbursement Create Employee)",
                in_modal: false,
            },
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text Tour Reimbursement Create Type",
            },
            {
                content: "Pick the type from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Reimbursement Create Type)",
                in_modal: false,
            },
            {
                content: "Select the Bank Account",
                trigger: ".o_field_many2one[name='employee_bank_account_id'] input",
                run: "text TOURRMBCREATEBANK",
            },
            {
                content: "Pick the bank account from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOURRMBCREATEBANK)",
                in_modal: false,
            },
            {
                content: "Fill in the Date",
                trigger: ".o_field_widget[name='date'] input",
                run: "text 01/15/2026",
            },
            {
                content: "Fill in the Date Due",
                trigger: ".o_field_widget[name='date_due'] input",
                run: "text 01/31/2026",
            },

            // Flow 4 — Fill in the Accounting tab. Journal and
            // Account are auto-filled from Type and are
            // intentionally left as-is (Keputusan Desain, issue
            // open-synergy/opnsynid-hr-expense#130).

            // Flow 5 — Add an expense line in the Details tab. The
            // line list has no `editable` tree, so "Add a line"
            // opens the line as a dialog form, not an inline row.
            {
                content: "Open the Details tab",
                trigger: ".o_notebook .nav-link:contains(Details)",
            },
            {
                content: "Click Add a line",
                trigger: ".o_field_x2many .o_field_x2many_list_row_add a",
            },
            {
                // Wizard-style dialog: do not prefix the trigger with
                // `.modal` -- 14.0 searches inside the modal already
                // (odoo-development-ui-test, patterns.md §H).
                content: "The expense line dialog is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Fill in the Date Expense",
                trigger: ".o_field_widget[name='date_expense'] input",
                run: "text 01/15/2026",
            },
            {
                content: "Select the Product",
                trigger: ".o_field_widget[name='product_id'] input",
                run: "text Tour Reimbursement Product",
            },
            {
                content: "Pick the product from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Reimbursement Product)",
                in_modal: false,
            },
            {
                content: "Fill in the Description",
                trigger: ".o_field_widget[name='name']",
                run: "text Tour Reimbursement Expense Line",
            },
            {
                content: "Fill in the Price Unit",
                trigger: ".o_field_widget[name='price_unit'] input",
                run: "text 100.0",
            },
            {
                // Placed inside a plain <div> (not the usual auto
                // wrapped <label>/<td> pair), this Float field's root
                // element is the <input> itself (same rendering as a
                // Char field in 14.0, odoo-development-ui-test,
                // patterns.md §C) -- no nested ` input` suffix.
                content: "Fill in the Qty",
                trigger: ".o_field_widget[name='uom_quantity']",
                run: "text 1.0",
            },
            {
                content: "Select the UoM",
                trigger: ".o_field_widget[name='uom_id'] input",
                run: "text Units",
            },
            {
                content: "Pick the UoM from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(Units)",
                in_modal: false,
            },
            {
                content: "Save the line",
                trigger: ".modal-footer button.btn-primary:contains('Save & Close')",
            },
            {
                content: "The line is added to the Details tab",
                trigger:
                    ".o_field_x2many .o_data_row:contains(Tour Reimbursement Expense Line)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 6 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Post-Condition — A new record is created in Draft
            // status.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/hr_reimbursement/04-confirm.md
    tour.register(
        "ssi_hr_reimbursement_hr_reimbursement_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openReimbursementsList(), [
            // Flow 2 — Open the record to confirm.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Reimbursement Confirm Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Confirm button.
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Waiting for
            // Approval.
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            // Negative (visible): the Confirm button is no longer
            // shown once the record left Draft.
            {
                content: "The Confirm button is no longer shown",
                trigger:
                    ".o_statusbar_buttons:not(:has(button[name='action_confirm']:visible))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/hr_reimbursement/05-approve.md
    tour.register(
        "ssi_hr_reimbursement_hr_reimbursement_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openReimbursementsList(), [
            // Flow 2 — Open the record to approve.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Reimbursement Approve Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition (all approval levels fulfilled) —
            // status changes to In Progress. The fixture's approval
            // template has a single validator level and the tour
            // user (admin) is the sole approver, so this branch is
            // always the one exercised.
            {
                content: "Status is In Progress",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/hr_reimbursement/10-cancel.md
    tour.register(
        "ssi_hr_reimbursement_hr_reimbursement_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openReimbursementsList(), [
            // Flow 2 — Open the record to cancel.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Reimbursement Cancel Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Cancel button. It is a
            // `type="action"` button, so its `name` attribute is a
            // numeric action id in the DOM; target it by label
            // instead (odoo-development-ui-test, selectors.md §4).
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — In the wizard that appears, select the
            // Cancellation Reason.
            {
                // Wizard: do not prefix the trigger with `.modal`
                // (odoo-development-ui-test, patterns.md §H).
                content: "The Select Cancel Reason wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                // The wizard renders `cancel_reason_id` with
                // `widget="radio"` (base_select_cancel_reason_views.xml),
                // not the default many2one autocomplete -- select the
                // matching radio item by its label text.
                content: "Select the Cancellation Reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(Tour Reimbursement Cancel Reason) input",
            },

            // Flow 5 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // Flow 6 — Click OK on the confirmation dialog. The
            // wizard's Confirm button carries
            // `confirm="Are you sure?"` (mixin
            // ssi_transaction_cancel_mixin), which
            // docs/hr_reimbursement/10-cancel.md was missing --
            // added there as step 6 to keep the IK the accurate
            // source of truth (odoo-development-ui-test,
            // patterns.md §G). This second dialog stacks on top of
            // the wizard; 14.0 scopes the trigger search to the
            // topmost visible modal, so the selector below
            // resolves to it automatically.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Cancelled.
            {
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );
});
