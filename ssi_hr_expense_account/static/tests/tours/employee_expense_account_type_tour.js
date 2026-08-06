/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_hr_expense_account.employee_expense_account_type_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/employee_expense_account_type/01-create.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_type_create",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the Human Resource > Configuration > Expense >
            // Expense Account Types menu. "Expense" is a grouping header
            // (menuitem without an action) that nests "Expense Account
            // Types", so it has no step of its own (patterns.md §A).
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr.menu_human_resource_configuration"]',
            },
            {
                content: "Open the Expense Account Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_expense_account.employee_expense_account_type_menu"]',
            },
            {
                // Gate: wait for the Expense Account Types action to
                // actually be mounted, not just any list view left over
                // from the landing action (patterns.md §A).
                content: "Expense Account Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Expense Account Types)",
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

            // Flow 3 — Fill in Name, Code, and the optional Accounts field.
            {
                content: "Fill in Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour Expense Account Type",
            },
            {
                content: "Fill in Code with /",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text /",
            },
            {
                content: "Open the Accounts tag input",
                trigger: ".o_field_many2manytags[name='account_ids'] input",
                run: "text Tour Expense Type Account",
            },
            {
                content: "Pick the Account from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Expense Type Account)",
                in_modal: false,
            },
            {
                content: "Account tag is added",
                trigger:
                    ".o_field_many2manytags[name='account_ids'] .badge:contains(Tour Expense Type Account)",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 4 — Inline Action: click Generate Code to auto-assign the
            // code left as "/" from the sequence.template prepared in
            // setUpClass.
            {
                content: "Click the Generate Code button",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                extra_trigger: ".o_form_view",
            },
            {
                // Gate: the object button auto-saves the still-new record
                // before running the method, so the breadcrumb keeps reading
                // "New" until that save lands (patterns.md §P, row 1).
                content: "Record is saved by Generate Code",
                trigger: ".o_control_panel .breadcrumb-item.active:not(:contains(New))",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 5 — Click Save.
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

            // Post-Condition — A new record is created and appears in the
            // Expense Account Types list.
            {
                content:
                    "Click the Expense Account Types breadcrumb to return to the list",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Expense Account Types)",
            },
            {
                content: "New record is shown in the list",
                trigger: ".o_list_view .o_data_row:contains(Tour Expense Account Type)",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});
