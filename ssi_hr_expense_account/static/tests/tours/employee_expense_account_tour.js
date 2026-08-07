/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_hr_expense_account.employee_expense_account_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/employee_expense_account/01-create.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_create",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the Human Resource > Expense > Expense Accounts
            // menu. "Expense" (level 2) has children, so it is a clickable
            // section header; "Expense Accounts" (level 3) is a leaf.
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
                content: "Open the Expense Accounts menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_expense_account.employee_expense_account_menu"]',
            },
            {
                // Gate: wait for the Expense Accounts action to actually be
                // mounted, not just any list view left over from the
                // landing action (patterns.md §A).
                content: "Expense Accounts list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Expense Accounts)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Click the New button. (14.0: "Create")
            {
                content: "Click New",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Fill in the required fields: Employee, Type, Date
            // Start, Date End, Currency, Limit. Department/Manager/Job
            // Position are auto-filled from Employee and left as-is per
            // the IK.
            {
                content: "Select the Employee",
                trigger: ".o_field_many2one[name='employee_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour EEA Employee Create",
            },
            {
                content: "Pick the Employee from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour EEA Employee Create)",
                in_modal: false,
            },
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text Tour EEA Expense Type",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour EEA Expense Type)",
                in_modal: false,
            },
            {
                content: "Fill in Date Start",
                trigger: ".o_field_widget[name='date_start'] input",
                run: "text 01/01/2026",
            },
            {
                content: "Fill in Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                run: "text 12/31/2026",
            },
            {
                content: "Select the Currency",
                trigger: ".o_field_many2one[name='currency_id'] input",
                run: "text TUR",
            },
            {
                content: "Pick the Currency from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TUR)",
                in_modal: false,
            },
            {
                content: "Fill in Limit",
                trigger: ".o_field_widget[name='amount_limit'] input",
                run: "text 1000",
            },

            // Flow 4 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },

            // Post-Condition — A new record is created in Draft status.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/employee_expense_account/04-confirm.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_confirm",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the Human Resource > Expense > Expense Accounts
            // menu.
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
                content: "Open the Expense Accounts menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_expense_account.employee_expense_account_menu"]',
            },
            {
                content: "Expense Accounts list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Expense Accounts)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Open the record to confirm. The fixture record is
            // tagged with a unique Employee name (setUpClass).
            {
                content: "Open the record to confirm",
                trigger:
                    ".o_data_row:contains(Tour EEA Employee Confirm) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
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

            // Post-Condition — Status changes to Waiting for Approval.
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },

            // Negative (Skenario Uji): once Waiting for Approval, the
            // Confirm button is no longer shown.
            {
                content: "The Confirm button is no longer shown",
                trigger:
                    ".o_statusbar_buttons:not(:has(button[name='action_confirm']:visible))",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/employee_expense_account/05-approve.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_approve",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the Human Resource > Expense > Expense Accounts
            // menu.
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
                content: "Open the Expense Accounts menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_expense_account.employee_expense_account_menu"]',
            },
            {
                content: "Expense Accounts list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Expense Accounts)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Open the record to approve. The fixture record is
            // already Waiting for Approval (setUpClass).
            {
                content: "Open the record to approve",
                trigger:
                    ".o_data_row:contains(Tour EEA Employee Approve) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
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

            // Post-Condition — Only one approval level is configured and
            // the tour user (admin) fulfils it, so status changes
            // straight to In Progress.
            {
                content: "Status is In Progress",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/employee_expense_account/10-cancel.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_cancel",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the Human Resource > Expense > Expense Accounts
            // menu.
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
                content: "Open the Expense Accounts menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_expense_account.employee_expense_account_menu"]',
            },
            {
                content: "Expense Accounts list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Expense Accounts)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Open the record to cancel. The fixture record is
            // Draft (setUpClass) — the simplest state the IK allows for
            // cancellation.
            {
                content: "Open the record to cancel",
                trigger:
                    ".o_data_row:contains(Tour EEA Employee Cancel) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Cancel button. It opens the "Select
            // Cancel Reason" wizard directly (type="action"), so its
            // rendered `name` is a numeric action id — select by text.
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:contains(Cancel)",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — In the wizard, select the Cancellation Reason.
            {
                content: "Wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Select the cancellation reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item label:contains(Tour Cancel Reason)",
            },

            // Flow 5 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // Flow 6 — Click OK on the confirmation dialog. The wizard's
            // Confirm button carries confirm="Are you sure?", so a second
            // dialog stacks on top (IK fix — see docs/employee_expense_
            // account/10-cancel.md step 6).
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
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/employee_expense_account/11-terminate.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_terminate",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the Human Resource > Expense > Expense Accounts
            // menu.
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
                content: "Open the Expense Accounts menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_expense_account.employee_expense_account_menu"]',
            },
            {
                content: "Expense Accounts list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Expense Accounts)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Open the record to terminate. The fixture record
            // is In Progress (setUpClass) — the earliest state the IK
            // allows for termination, and the only one where the
            // Terminate button is guaranteed to be shown.
            {
                content: "Open the record to terminate",
                trigger:
                    ".o_data_row:contains(Tour EEA Employee Terminate) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Terminate button. It opens the "Select
            // Termination Reason" wizard directly (type="action"), so its
            // rendered `name` is a numeric action id — select by text.
            {
                content: "Click the Terminate button",
                trigger: ".o_statusbar_buttons button:contains(Terminate)",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — In the wizard, select the Termination Reason.
            {
                content: "Wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Select the termination reason",
                trigger:
                    ".o_field_widget[name='terminate_reason_id'] .o_radio_item label:contains(Tour Terminate Reason)",
            },

            // Flow 5 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // Flow 6 — Click OK on the confirmation dialog. The wizard's
            // Confirm button carries confirm="Are you sure?", so a second
            // dialog stacks on top (IK fix — see docs/employee_expense_
            // account/11-terminate.md step 6).
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Terminated.
            {
                content: "Status is Terminated",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='terminate'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});
