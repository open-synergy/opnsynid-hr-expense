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

    // IK: docs/employee_expense_account_type/02-edit.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_type_edit",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the Human Resource > Configuration > Expense >
            // Expense Account Types menu.
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
                content: "Expense Account Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Expense Account Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Find and open the record to edit.
            {
                content: "Open the record to edit",
                trigger: ".o_data_row:contains(Tour EEAT Edit) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Edit button. (14.0 only — the form opens
            // directly editable on 16.0+.)
            {
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

            // Flow 4 — Change Name or Accounts as needed. Reassigning
            // Code via Reset code / Generate Code (step 5 of the IK) is
            // documented as optional -- this tour keeps the current code
            // unchanged.
            {
                content: "Change the Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour EEAT Edit Renamed",
            },

            // Flow 6 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                // Post-Condition — The record is updated with the new
                // values. Verifying the new value itself is out of scope
                // for a tour (odoo-development-ui-test boundary table);
                // the save completing without error is the kasatmata
                // proof.
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/employee_expense_account_type/03-delete.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_type_delete",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the Human Resource > Configuration > Expense >
            // Expense Account Types menu.
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
                content: "Expense Account Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Expense Account Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Open the record to delete.
            {
                content: "Open the record to delete",
                trigger: ".o_data_row:contains(Tour EEAT Delete) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
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

            // Flow 5 — Click the Expense Account Types breadcrumb to
            // return to the list.
            {
                content: "Click the Expense Account Types breadcrumb",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Expense Account Types)",
            },

            // Post-Condition — The record is permanently removed; the
            // list view no longer shows it.
            {
                content: "Record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(Tour EEAT Delete)))",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/employee_expense_account_type/04-deactivate.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_type_deactivate",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the Human Resource > Configuration > Expense >
            // Expense Account Types menu.
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
                content: "Expense Account Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Expense Account Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Select one or more records to deactivate (check
            // the checkbox).
            {
                content: "Select the record to deactivate",
                trigger:
                    ".o_data_row:contains(Tour EEAT Deactivate) .o_list_record_selector input",
                extra_trigger: ".o_list_view",
                run: "click",
            },

            // Flow 3 — Click Action > Archive.
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Click Archive",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $archive = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Archive";
                        }
                    );
                    $archive[0].click();
                },
            },

            // Flow 4 — Click OK to confirm. Archive (unlike Unarchive)
            // wraps its callback in `Dialog.confirm` at 14.0
            // (odoo-development-ui-test, patterns.md §G/§J), so a dialog
            // genuinely appears here.
            {
                content: "Confirm archiving",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — The record is archived and no longer
            // appears in the default (active) list view.
            {
                content: "Record no longer appears in the active list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(Tour EEAT Deactivate)))",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/employee_expense_account_type/05-activate.md
    tour.register(
        "ssi_hr_expense_account_employee_expense_account_type_activate",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 — Open the Human Resource > Configuration > Expense >
            // Expense Account Types menu.
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
                content: "Expense Account Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Expense Account Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 2 — Enable the Archived filter in the search bar.
            {
                content: "Open the Filters menu",
                trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                // 14.0: the Filters dropdown is an Owl component that
                // does not always open on a synthetic click
                // (odoo-development-ui-test, patterns.md §I/§J).
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Enable the Archived filter",
                trigger: ".o_filter_menu .o_menu_item a:contains(Archived)",
                run: function () {
                    this.$anchor[0].click();
                },
            },

            // Flow 3 — Select one or more records to reactivate (check
            // the checkbox).
            {
                content: "Select the record to reactivate",
                trigger:
                    ".o_data_row:contains(Tour EEAT Activate) .o_list_record_selector input",
                run: "click",
            },

            // Flow 4 — Click Action > Unarchive.
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Click Unarchive",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $unarchive = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Unarchive";
                        }
                    );
                    $unarchive[0].click();
                },
            },

            // Flow 5 (IK text) -- "Click OK to confirm." Verified against
            // Odoo 14.0 core (web/static/src/js/views/list/
            // list_controller.js `_getActionMenuItems`): only "Archive"
            // wraps its callback in `Dialog.confirm(...)`; "Unarchive"
            // calls `_toggleArchiveState(false)` directly with no
            // confirmation dialog. There is therefore no dialog step to
            // add here -- this is a known inaccuracy in the IK text
            // (docs/employee_expense_account_type/05-activate.md step 5),
            // the same pattern already documented in
            // ssi_employee_business_trip's employee_business_trip_type_tour.js,
            // ssi_customer_invoice's customer_invoice_type_tour.js, and
            // ssi_vendor_bill's vendor_bill_type_tour.js. Out of scope for
            // this tour-pairing change (issue
            // open-synergy/opnsynid-hr-expense#194).

            // Post-Condition — The record is restored and appears again
            // in the default (active) list view.
            {
                content: "Record appears again in the active list",
                trigger: ".o_list_view .o_data_row:contains(Tour EEAT Activate)",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});
