/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_employee_business_trip.employee_business_trip_type_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/employee_business_trip_type/01-create.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_type_create",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the Human Resource > Configuration > Expense >
            // Business Trip Types menu. "Expense" is a grouping header
            // (menuitem without an action) that nests "Business Trip Types",
            // so it has no step of its own (patterns.md §A).
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
                content: "Open the Business Trip Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_employee_business_trip.employee_business_trip_type_menu"]',
            },
            {
                // Gate: wait for the Business Trip Types action to actually
                // be mounted, not just any list view left over from the
                // landing action (patterns.md §A).
                content: "Business Trip Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Business Trip Types)",
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

            // Flow 3 — Fill in the required Name and Code fields.
            {
                content: "Fill in Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour Business Trip Type",
            },
            {
                content: "Fill in Code with /",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text /",
            },

            // Flow 4 — Product tab (Product Selection Method keeps its
            // Domain default; only the tab render is verified here).
            {
                content: "Open the Product tab",
                trigger: ".o_notebook .nav-link:contains(Product)",
            },
            {
                content: "Product tab is displayed",
                trigger: ".o_horizontal_separator:contains(Product)",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 5 — Currencies & Pricelist tab (both Selection Methods
            // keep their Domain default; only the tab render is verified).
            {
                content: "Open the Currencies & Pricelist tab",
                trigger: ".o_notebook .nav-link:contains(Currencies & Pricelist)",
            },
            {
                content: "Currencies group is displayed",
                trigger: ".o_horizontal_separator:contains(Currencies)",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 6 — Origin & Destination tab (both Selection Methods
            // keep their Domain default; only the tab render is verified).
            {
                content: "Open the Origin & Destination tab",
                trigger: ".o_notebook .nav-link:contains(Origin & Destination)",
            },
            {
                content: "Origin group is displayed",
                trigger: ".o_horizontal_separator:contains(Origin)",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 7 — Accounting tab: fill in Journal and Payable Account.
            {
                content: "Open the Accounting tab",
                trigger: ".o_notebook .nav-link:contains(Accounting)",
            },
            {
                content: "Select the Journal",
                trigger: ".o_field_many2one[name='journal_id'] input",
                run: "text Tour Business Trip Journal",
            },
            {
                content: "Pick the Journal from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Business Trip Journal)",
                in_modal: false,
            },
            {
                content: "Select the Payable Account",
                trigger: ".o_field_many2one[name='payable_account_id'] input",
                run: "text Tour Business Trip Payable",
            },
            {
                content: "Pick the Payable Account from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Business Trip Payable)",
                in_modal: false,
            },

            // Flow 8 — Inline Action: click Generate Code to auto-assign the
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

            // Flow 9 — Click Save.
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
            // Business Trip Types list.
            {
                content:
                    "Click the Business Trip Types breadcrumb to return to the list",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Business Trip Types)",
            },
            {
                content: "New record is shown in the list",
                trigger: ".o_list_view .o_data_row:contains(Tour Business Trip Type)",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});
