/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_hr_cash_advance.hr_cash_advance_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block, reused verbatim by every tour below --
    // Flow step 1 of every IK in docs/hr_cash_advance/: "Open the Human
    // Resource > Expense > Cash Advances menu." "Expense" is a section
    // menuitem (has its own data-menu-xmlid, not a grouping header), so
    // it is its own step (odoo-development-ui-test, patterns.md §A).
    function openCashAdvancesList() {
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
                content: "Open the Cash Advances menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_cash_advance.hr_cash_advance_menu"]',
            },
            {
                // Gate: wait for the Cash Advances action to actually be
                // mounted, not just any list view left over from the
                // landing action (odoo-development-ui-test, patterns.md
                // §A).
                content: "Cash Advances list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Cash Advances)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/hr_cash_advance/01-create.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvancesList(), [
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
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 3 — Fill in the required fields in the header.
            // Employee/Department/Manager/Job are auto-filled from the
            // current user's employee and Currency keeps its default
            // (company currency) -- all left as-is (Keputusan Desain,
            // issue open-synergy/opnsynid-hr-expense#131). Pricelist
            // and Duration are optional and intentionally skipped.
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour Cash Advance Create Type",
            },
            {
                content: "Pick the type from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Cash Advance Create Type)",
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

            // Flow 4 — Add lines in the Details tab. The Journal, Cash
            // Advance Account, and Payable Account fields in the
            // Accounting tab are auto-filled from Type via onchange
            // and are intentionally left as-is; the Details tab
            // itself is out of scope for this tour (Keputusan Desain,
            // issue open-synergy/opnsynid-hr-expense#131).

            // Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Post-Condition — A new record is created in Draft
            // status.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // IK: docs/hr_cash_advance/04-confirm.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvancesList(), [
            // Flow 2 — Open the record to confirm.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Cash Advance Confirm Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
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
                    // Assertion only; do not trigger the default click action.
                },
            },
            // Negative (visible): the Confirm button is no longer
            // shown once the record left Draft.
            {
                content: "The Confirm button is no longer shown",
                trigger:
                    ".o_statusbar_buttons:not(:has(button[name='action_confirm']:visible))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // IK: docs/hr_cash_advance/05-approve.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvancesList(), [
            // Flow 2 — Open the record to approve.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Cash Advance Approve Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
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

            // Post-Condition (all approval levels fulfilled) --
            // status changes to Open. The fixture's approval template
            // has a single validator level and the tour user (admin)
            // is the sole approver, so this branch is always the one
            // exercised.
            {
                content: "Status is Open",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // IK: docs/hr_cash_advance/10-cancel.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvancesList(), [
            // Flow 2 — Open the record to cancel.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Cash Advance Cancel Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
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
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                // The wizard renders `cancel_reason_id` with
                // `widget="radio"` (base_select_cancel_reason_views.xml),
                // not the default many2one autocomplete -- select the
                // matching radio item by its label text.
                content: "Select the Cancellation Reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(Tour Cash Advance Cancel Reason) input",
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
            // docs/hr_cash_advance/10-cancel.md was missing -- added
            // there as step 6 to keep the IK the accurate source of
            // truth (odoo-development-ui-test, patterns.md §G), same
            // as the existing fix in
            // docs/hr_reimbursement/10-cancel.md (issue
            // open-synergy/opnsynid-hr-expense#130). This second
            // dialog stacks on top of the wizard; 14.0 scopes the
            // trigger search to the topmost visible modal, so the
            // selector below resolves to it automatically.
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
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );
});
