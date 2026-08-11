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

    // IK: docs/hr_expense_type/02-edit.md
    tour.register(
        "ssi_hr_expense_hr_expense_type_edit",
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

            // ── Flow 2 — Find and open the Expense Type record to edit
            {
                content: "Open the Expense Type record",
                trigger:
                    ".o_data_row:contains(TOUR-EDIT-EXPENSE-TYPE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 3 — Click the Edit button
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

            // ── Flow 4 — Change the required Expense Type field
            {
                content: "Change the Expense Type field",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-EDIT-EXPENSE-TYPE UPDATED",
            },

            // ── Flow 5 — Click the Generate Code button (Code is still
            // "/" from the fixture, so this inline action has
            // something to do)
            {
                content: "Click the Generate Code button",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                // Gerbang: sama seperti tour create — tunggu Code field
                // tak lagi menampilkan literal "/" yang diset di
                // setUpClass, baru benar setelah Generate Code selesai
                // jalan. Nilai hasil generate sendiri bukan wilayah
                // tour. Tombol ini menyimpan lewat auto-save dengan
                // `stayInEdit: true` (form_controller.js), jadi form
                // tetap dalam mode edit sesudah step ini.
                content: "Code is generated automatically",
                trigger: ".o_field_widget[name='code']:not(:contains(/))",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 7 — Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — The record is updated with the new
            // values
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/hr_expense_type/03-delete.md
    tour.register(
        "ssi_hr_expense_hr_expense_type_delete",
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

            // ── Flow 2 — Open the Expense Type record to delete
            {
                content: "Open the Expense Type record",
                trigger:
                    ".o_data_row:contains(TOUR-DELETE-EXPENSE-TYPE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 3 — Click Action > Delete
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                // Item Action menu adalah komponen Owl; cocokkan LABEL
                // PERSIS -- :contains(Delete) sebagai substring bisa
                // keliru menunjuk item lain.
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

            // ── Flow 4 — Click OK to confirm
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Flow 5 (implicit) — after delete, 14.0 form may show the
            // next record in the list rather than navigating back on
            // its own; return to the list explicitly before asserting
            // it.
            {
                content: "Click the Expense Types breadcrumb",
                trigger: ".breadcrumb-item.o_back_button a:contains(Expense Types)",
            },

            // ── Post-Condition — The record is permanently removed;
            // list no longer shows it
            {
                content: "Record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR-DELETE-EXPENSE-TYPE)))",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/hr_expense_type/04-deactivate.md
    tour.register(
        "ssi_hr_expense_hr_expense_type_deactivate",
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

            // ── Flow 2 — Open the Expense Type record to deactivate
            {
                content: "Open the Expense Type record",
                trigger:
                    ".o_data_row:contains(TOUR-DEACTIVATE-EXPENSE-TYPE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 3 — Click the Edit button
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

            // ── Flow 4 — Toggle the Active field off
            {
                content: "Toggle the Active field off",
                trigger: ".o_field_widget[name='active'] input",
                run: "click",
            },

            // ── Flow 5 — Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — Archived ribbon appears on the form
            {
                content: "Archived ribbon is displayed",
                trigger: ".o_form_view .ribbon:visible:contains(Archived)",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );

    // IK: docs/hr_expense_type/05-activate.md
    tour.register(
        "ssi_hr_expense_hr_expense_type_activate",
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

            // ── Flow 2 — Enable the Archived filter in the search bar
            {
                // Tunggu list awal selesai render lebih dulu supaya
                // dropdown Filters dibuka pada state yang stabil.
                content: "Wait for the list data to finish loading",
                trigger: ".o_list_view .o_data_row",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Open the Filters menu",
                trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                run: function () {
                    // Dropdown Owl 14.0 tidak selalu terbuka oleh klik
                    // sintetis default -- pakai klik browser asli.
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
            {
                // Gerbang: `aria-checked` adalah atribut HTML sungguhan
                // yang di-toggle Owl secara sinkron, tunggu sampai
                // facet Archived benar-benar tertandai sebelum lanjut.
                content: "Archived filter is checked",
                trigger:
                    ".o_filter_menu .o_menu_item a:contains(Archived)[aria-checked='true']",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 3 — Open the archived Expense Type record to
            // reactivate
            {
                content: "Open the archived Expense Type record",
                trigger:
                    ".o_data_row:contains(TOUR-ACTIVATE-EXPENSE-TYPE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Flow 4 — Click the Edit button
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

            // ── Flow 5 — Toggle the Active field on
            {
                content: "Toggle the Active field on",
                trigger: ".o_field_widget[name='active'] input",
                run: "click",
            },

            // ── Flow 6 — Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — Archived ribbon no longer appears
            {
                content: "Archived ribbon is no longer displayed",
                trigger: ".o_form_view:not(:has(.ribbon:visible:contains(Archived)))",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});
