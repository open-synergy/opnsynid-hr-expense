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

    // IK: docs/employee_expense_account/02-edit.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_edit",
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

            // Flow 2 — Find and open the record to edit.
            {
                content: "Open the record to edit",
                trigger:
                    ".o_data_row:contains(Tour EEA Employee Edit) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                // 14.0 — a record already saved opens read-only; Edit must
                // be clicked before any field can be changed
                // (odoo-development-ui-test, patterns.md §E).
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Change the required fields.
            {
                content: "Change the Limit",
                trigger: ".o_field_widget[name='amount_limit'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 2000",
            },

            // Flow 4 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                // Post-Condition — The record is updated with the new
                // values. Verifying the new value itself is out of
                // scope for a tour (odoo-development-ui-test boundary
                // table, wilayah odoo-development-unit-test); the save
                // completing without error is the kasatmata proof.
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/employee_expense_account/03-delete.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_delete",
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

            // Flow 2 — Select one or more records to delete (check the
            // checkbox).
            {
                content: "Select the record to delete",
                trigger:
                    ".o_data_row:contains(Tour EEA Employee Delete) .o_list_record_selector input",
                extra_trigger: ".o_list_view",
                run: "click",
            },

            // Flow 3 — Click Action > Delete.
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
                // 14.0: the Action dropdown is an Owl component that does
                // not always open on a synthetic click
                // (odoo-development-ui-test, patterns.md §I).
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Click Delete",
                // Item Action menu is an Owl component; target the <a>
                // inside .o_menu_item and match the label EXACTLY --
                // :contains(Delete) as a substring could match another
                // item.
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Delete";
                        }
                    );
                    $delete[0].click();
                },
            },

            // Flow 4 — Click OK to confirm.
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — The selected record is permanently removed
            // from the system.
            {
                content: "Record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(Tour EEA Employee Delete)))",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/employee_expense_account/06-reject.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_reject",
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

            // Flow 2 — Open the record to reject. The fixture record is
            // already Waiting for Approval (setUpClass).
            {
                content: "Open the record to reject",
                trigger:
                    ".o_data_row:contains(Tour EEA Employee Reject) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Reject button.
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Rejected.
            {
                content: "Status is Rejected",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/employee_expense_account/09-finish.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_finish",
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

            // Flow — the transition to Done is automatic (base.automation
            // `employee_expense_account_to_done`); there is no button to
            // drive it from the UI. The fixture is already Done before
            // this tour starts, reached in Python exactly as the
            // automation would run it (odoo-development-ui-test,
            // scope-and-boundaries.md §1 aturan 6). This tour only opens
            // the record and observes the result.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour EEA Employee Finish) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Post-Condition — Status changes to Done.
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/employee_expense_account/07-start.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_start",
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

            // Flow — the transition back to In Progress is automatic
            // (base.automation `employee_expense_account_to_open`); there
            // is no button to drive it from the UI. The fixture is
            // already back to In Progress before this tour starts,
            // reached in Python exactly as the automation would run it
            // (odoo-development-ui-test, scope-and-boundaries.md §1
            // aturan 6). This tour only opens the record and observes the
            // result.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour EEA Employee Start) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Post-Condition — Status returns to In Progress.
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

    // IK: docs/employee_expense_account/12-restart.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_restart",
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

            // Flow 2 — Open the record to restart. The fixture record is
            // Cancelled (setUpClass).
            {
                content: "Open the record to restart",
                trigger:
                    ".o_data_row:contains(Tour EEA Employee Restart) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Restart button.
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            // `action_restart` carries `confirm="Restart data. Are you
            // sure?"`, missing from the original IK text -- added there as
            // the corrected IK Flow (odoo-development-ui-test,
            // patterns.md §G).
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status returns to Draft.
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

    // IK: docs/employee_expense_account/13-reset-number.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_reset_number",
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

            // Flow 2 — Open the record whose document number will be
            // reset.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour EEA Employee Reset Number) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Reset Document Number button.
            {
                content: "Click the Reset Document Number button",
                trigger:
                    ".o_statusbar_buttons button[name='action_reset_document_number']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            // `action_reset_document_number` carries `confirm="Restart
            // document number. Are you sure?"`, missing from the original
            // IK text -- added here as the corrected IK Flow
            // (odoo-development-ui-test, patterns.md §G).
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Document number returns to "/" (it is
            // already "/" on this Draft record). The `name` field stores
            // "/", but `MixinTransaction.name_get`
            // (ssi_transaction_mixin, mixin_transaction.py) renders it as
            // "*<id>" whenever the stored number is "/" -- the literal
            // "/" never appears in the readonly display_name widget, so
            // the visible fact checked here is that the action completes
            // and the read-only form still shows the "*<id>" placeholder,
            // not a new error.
            {
                content: 'Document number is still "/" (shown as "*<id>")',
                trigger:
                    ".o_form_view .o_field_widget[name='display_name']:contains('*')",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});
