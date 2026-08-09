/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_employee_business_trip_work_log.employee_business_trip_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/employee_business_trip/01-create.md
        tour.register(
            "ssi_employee_business_trip_work_log_employee_business_trip_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Human Resource > Expense > Business Trips
                // menu, then click the New button. "Expense" is a grouping
                // header (menuitem without an action) that nests "Business
                // Trips", so it has no step of its own (odoo-development-ui-
                // test, patterns.md §A).
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
                },
                {
                    content: "Open the Expense menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_hr_expense.expense_menu"]',
                },
                {
                    content: "Open the Business Trips menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_employee_business_trip.employee_business_trip_menu"]',
                },
                {
                    // Gate: wait for the Business Trips action to actually be
                    // mounted, not just any list view left over from the
                    // landing action (patterns.md §A).
                    content: "Business Trips list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Business Trips)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },
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

                // Flow 2 — Click the Work Log tab.
                {
                    content: "Click the Work Log tab",
                    trigger: ".o_notebook .nav-link:contains(Work Log)",
                },

                // Flow 3 — Enter a value in the Estimation field.
                {
                    content: "Fill in Estimation",
                    trigger: ".o_field_widget[name='work_estimation']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 8:00",
                },

                // Flow 4 — Select an account in the Work Log Analytic Account
                // field. Record prepared in setUpClass (Pre-Condition data,
                // not the focus of this tour — odoo-development-ui-test,
                // patterns.md §C).
                {
                    content: "Select the Work Log Analytic Account",
                    trigger:
                        ".o_field_many2one[name='work_log_analytic_account_id'] input",
                    run: "text TOUR Work Log Analytic Account",
                },
                {
                    content: "Pick the analytic account from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR Work Log Analytic Account)",
                    in_modal: false,
                },

                // Flow 5 — Click Add a line below Work Log Analytic Account to
                // open the Work Log entry dialog.
                {
                    content: "Click Add a line",
                    trigger:
                        ".o_field_x2many[name='work_log_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    // Wizard opened. 14.0: do NOT prefix the trigger with
                    // `.modal` — the tour engine already scopes the search
                    // inside the currently visible modal
                    // (odoo-development-ui-test, patterns.md §H).
                    content: "The Work Log entry dialog is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 6 — Click Discard to close the dialog without saving a
                // line. Work Log lines are optional at create time; this tour
                // stops here (odoo-development-ui-test, patterns.md §Q) — it
                // does not fill in or save a Work Log line, and does not
                // continue through the rest of the base create Flow (Trip
                // Information, Per Diem, Accounting, Save).
                {
                    content: "Discard the Work Log entry dialog",
                    trigger: ".modal-footer button.btn-secondary",
                },

                // Post-Condition — the dialog is closed and the create form
                // remains open.
                {
                    content: "Work Log entry dialog is closed",
                    trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Create form remains open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
