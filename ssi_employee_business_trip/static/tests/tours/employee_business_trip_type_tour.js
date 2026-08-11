/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_employee_business_trip.employee_business_trip_type_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block, reused verbatim by every tour below --
    // Flow step 1 of every IK in docs/employee_business_trip_type/:
    // "Open the Human Resource > Configuration > Expense > Business Trip
    // Types menu." "Expense" is a grouping header (menuitem without an
    // action) that nests "Business Trip Types", so it has no step of
    // its own (odoo-development-ui-test, patterns.md §A).
    function openBusinessTripTypesList() {
        return [
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
        ];
    }

    // IK: docs/employee_business_trip_type/01-create.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_type_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripTypesList(), [
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
        ])
    );

    // IK: docs/employee_business_trip_type/02-edit.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_type_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripTypesList(), [
            // Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(Tour EBT Type Edit) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Edit button. (14.0 only — the form opens
            // directly editable on 16.0+)
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

            // Flow 4 — Change the required fields: rename to a value
            // different from the fixture's, so the Post-Condition below
            // actually proves the change landed.
            {
                content: "Change the Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour EBT Type Edited",
            },

            // Flow 5 — Reassigning Code is optional (Keputusan Desain,
            // issue open-synergy/opnsynid-hr-expense#191); skipped here.

            // Flow 6 — Click Save.
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

            // Post-Condition — The record is updated with the new
            // values: go back to the list and read the renamed row as a
            // genuine text node (odoo-development-ui-test, patterns.md
            // §L).
            {
                content: "Go back to the list",
                trigger:
                    ".breadcrumb-item:not(.active):contains('Business Trip Types')",
            },
            {
                content: "Renamed record is shown in the list",
                trigger: ".o_list_view .o_data_row:contains(Tour EBT Type Edited)",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/employee_business_trip_type/03-delete.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_type_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripTypesList(), [
            // Flow 2 — Open the record to delete.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour EBT Type Delete) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
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
                // not always open on a synthetic click (odoo-development-
                // ui-test, patterns.md §I).
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

            // Flow 5 — Click the Business Trip Types breadcrumb to
            // return to the list. 14.0 can show the next record in the
            // list after a form-level delete instead of returning to
            // the list on its own (odoo-development-ui-test,
            // patterns.md §I).
            {
                content: "Click the Business Trip Types breadcrumb",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Business Trip Types)",
            },

            // Post-Condition — The record is permanently removed and no
            // longer shown in the list.
            {
                content: "Record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(Tour EBT Type Delete)))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/employee_business_trip_type/04-deactivate.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_type_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripTypesList(), [
            // Flow 2 — Select the record to deactivate (check the
            // checkbox).
            {
                content: "Select the record to deactivate",
                trigger:
                    ".o_data_row:contains(Tour EBT Type Deactivate) .o_list_record_selector input",
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
            // (odoo-development-ui-test, patterns.md §G/§J), so a
            // dialog genuinely appears here.
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
                    ".o_list_view:not(:has(.o_data_row:contains(Tour EBT Type Deactivate)))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/employee_business_trip_type/05-activate.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_type_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripTypesList(), [
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

            // Flow 3 — Select the record to reactivate (checkbox).
            {
                content: "Select the record to reactivate",
                trigger:
                    ".o_data_row:contains(Tour EBT Type Activate) .o_list_record_selector input",
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
            // (docs/employee_business_trip_type/05-activate.md step 5),
            // the same pattern already documented in
            // ssi_customer_invoice's customer_invoice_type_tour.js and
            // ssi_vendor_bill's vendor_bill_type_tour.js. Out of scope
            // for this tour-pairing change (issue
            // open-synergy/opnsynid-hr-expense#191).

            // Post-Condition — The record is restored and appears again
            // in the default (active) list view.
            {
                content: "Record appears again in the active list",
                trigger: ".o_list_view .o_data_row:contains(Tour EBT Type Activate)",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );
});
