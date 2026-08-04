odoo.define("ssi_hr_expense.hr_expense_type_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_expense_type/01-create.md
    tour.register(
        "ssi_hr_expense_hr_expense_type_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Human Resource > Configuration >
            // Expense > Types menu
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
                // "Expense" is a grouping header without its own action
                // (level 3+ with children, no data-menu-xmlid) — go
                // straight to the "Types" leaf item flattened below it.
                content: "Open the Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_expense.hr_expense_type_menu"]',
            },
            {
                // Gerbang: tunggu action TUJUAN benar-benar terpasang.
                content: "Expense Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Expense Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 2 — Click the New button
            {
                content: "Click Create",
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

            // ── Flow 3 — Fill in the Expense Type and Code fields
            {
                content: "Fill in the Expense Type field",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour Expense Type",
            },
            {
                content: "Fill in the Code field with /",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text /",
            },

            // ── Flow 4 — Click Save
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

            // ── Flow 5 — Click Generate Code (inline action)
            {
                content: "Click the Generate Code button",
                trigger: "button[name='action_generate_code']",
                extra_trigger: ".o_form_view.o_form_readonly",
            },
            {
                // Gerbang: Code field no longer shows the literal "/"
                // placeholder typed at Flow 3 — only true after
                // Generate Code has actually run. The generated value
                // itself is not asserted; that is unit-test territory.
                content: "Code is generated automatically",
                trigger: ".o_field_widget[name='code']:not(:contains(/))",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Post-Condition — A new record is created
            {
                content: "Return to the Expense Types list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Expense Types)",
            },
            {
                content: "New record appears in the list",
                trigger: ".o_data_row:contains(Tour Expense Type)",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});
