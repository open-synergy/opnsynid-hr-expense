/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_hr_expense_account_work_log.employee_expense_account_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/employee_expense_account/01-create.md
    tour.register(
        "ssi_hr_expense_account_work_log_employee_expense_account_create",
        {
            test: true,
            url: "/web",
        },
        [
            // Base Flow 1 — Open the Human Resource > Expense > Expense
            // Accounts menu. "Expense" is a grouping header (menuitem
            // without an action) that nests "Expense Accounts", so it has
            // no step of its own (odoo-development-ui-test,
            // patterns.md §A).
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
                // Gate: wait for the Expense Accounts action to actually
                // be mounted, not just any list view left over from the
                // landing action (patterns.md §A).
                content: "Expense Accounts list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Expense Accounts)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Base Flow 2 — Click the New button. (14.0: "Create")
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

            // Additional Fields (docs/employee_expense_account/01-create.md,
            // delta of ssi_hr_expense_account_work_log) — the Work Log tab
            // added by mixin.work_object is rendered on the create form.
            // Delta-only tour: it stops here, it does not fill any field
            // and does not continue to Save (odoo-development-ui-test,
            // patterns.md §O).
            {
                content: "Work Log tab is displayed",
                trigger: ".o_notebook .nav-link:contains(Work Log)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ]
    );
});
