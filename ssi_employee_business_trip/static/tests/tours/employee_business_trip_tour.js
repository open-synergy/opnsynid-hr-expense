/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_employee_business_trip.employee_business_trip_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block, reused verbatim by every tour below -- Flow
    // step 1 of every IK in docs/employee_business_trip/: "Open the Human
    // Resource > Expense > Business Trips menu." "Expense" is a section
    // menuitem (has its own data-menu-xmlid, not a grouping header), so it
    // is its own step (odoo-development-ui-test, patterns.md §A).
    function openBusinessTripsList() {
        return [
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
                content: "Open the Business Trips menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_employee_business_trip.employee_business_trip_menu"]',
            },
            {
                // Gate: wait for the Business Trips action to actually be
                // mounted, not just any list view left over from the
                // landing action (odoo-development-ui-test, patterns.md
                // §A).
                content: "Business Trips list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Business Trips)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ];
    }

    // IK: docs/employee_business_trip/01-create.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripsList(), [
            // Flow 2 — Click the New button.
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

            // Flow 3 — Fill in the required fields in the header. Department,
            // Manager, and Job Position auto-fill from Employee and are
            // read-only, so they are left as-is.
            {
                content: "Select the Employee",
                trigger: ".o_field_many2one[name='employee_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour EBT Create Employee",
            },
            {
                content: "Pick the Employee from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour EBT Create Employee)",
                in_modal: false,
            },
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text Tour EBT Type",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(Tour EBT Type)",
                in_modal: false,
            },
            {
                content: "Fill in the Date",
                trigger: ".o_field_widget[name='date'] input",
                run: "text 01/15/2026",
            },

            // Flow 4 — In the Trip Information tab, fill in Date Start,
            // Date End, Origin, and Destination.
            {
                content: "Open the Trip Information tab",
                trigger: ".o_notebook .nav-link:contains(Trip Information)",
            },
            {
                content: "Fill in Date Start",
                trigger: ".o_field_widget[name='date_start'] input",
                run: "text 01/15/2026",
            },
            {
                content: "Fill in Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                run: "text 01/20/2026",
            },
            {
                content: "Select the Origin",
                trigger: ".o_field_many2one[name='origin_id'] input",
                run: "text Tour EBT Origin City",
            },
            {
                content: "Pick the Origin from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour EBT Origin City)",
                in_modal: false,
            },
            {
                content: "Select the Destination",
                trigger: ".o_field_many2one[name='destination_id'] input",
                run: "text Tour EBT Destination City",
            },
            {
                content: "Pick the Destination from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour EBT Destination City)",
                in_modal: false,
            },

            // Flow 5 — In the Per Diem tab, fill in Currency, Pricelist,
            // Date Due, and add one Per Diem line. Analytic Account is
            // optional and is intentionally skipped (Keputusan Desain,
            // issue open-synergy/opnsynid-hr-expense#132).
            {
                content: "Open the Per Diem tab",
                trigger: ".o_notebook .nav-link:contains(Per Diem)",
            },
            {
                content: "Select the Currency",
                trigger: ".o_field_many2one[name='currency_id'] input",
                run: "text EBT",
            },
            {
                content: "Pick the Currency from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(EBT)",
                in_modal: false,
            },
            {
                content: "Select the Pricelist",
                trigger: ".o_field_many2one[name='pricelist_id'] input",
                run: "text Tour EBT Pricelist",
            },
            {
                content: "Pick the Pricelist from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour EBT Pricelist)",
                in_modal: false,
            },
            {
                content: "Fill in Date Due",
                trigger: ".o_field_widget[name='date_due'] input",
                run: "text 01/31/2026",
            },
            {
                content: "Click Add a line",
                trigger:
                    ".o_field_x2many[name='per_diem_ids'] .o_field_x2many_list_row_add a",
            },
            {
                content: "Select the Product",
                trigger: ".o_selected_row .o_field_widget[name='product_id'] input",
                run: "text Tour EBT Product",
            },
            {
                content: "Pick the Product from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(Tour EBT Product)",
                in_modal: false,
            },
            // Description and UoM auto-fill from the selected Product and
            // are left as-is.
            {
                content: "Select the Usage",
                trigger: ".o_selected_row .o_field_widget[name='usage_id'] input",
                run: "text Tour EBT Usage",
            },
            {
                content: "Pick the Usage from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(Tour EBT Usage)",
                in_modal: false,
            },
            // Account auto-fills from Product + Usage and is left as-is.
            {
                // Root IS the input for this Float cell inside the editable
                // list row, same rendering core Odoo relies on
                // (addons/sale/static/src/js/tours/sale.js) -- no nested
                // ` input` suffix (odoo-development-ui-test, patterns.md
                // §C).
                content: "Fill in the Qty",
                trigger: ".o_selected_row .o_field_widget[name='uom_quantity']",
                run: "text 2",
            },
            {
                // `price_unit` is a Monetary field, NOT a plain Float:
                // `FieldMonetary` renders its edit-mode root as a `<div
                // class="o_input">` wrapping the currency symbol AND a
                // nested `<input>` (web/static/src/js/fields/
                // basic_fields.js `FieldMonetary.init` -- "They are a
                // div containing a span with the currency symbol and
                // the actual input."). Targeting the bare
                // `.o_field_widget` div (correct for `uom_quantity`
                // above, a plain Float) makes the tour engine classify
                // it as non-input, and the built-in "text" run action
                // then crashes calling `.focusIn()` on the div (verified
                // in CI: TypeError: values.$element.focusIn is not a
                // function). The nested `input` targets the real input.
                content: "Fill in the Price",
                trigger: ".o_selected_row .o_field_widget[name='price_unit'] input",
                run: "text 100.0",
            },

            // Flow 6 — In the Accounting tab, verify Journal and Payable
            // Account (auto-filled from Type). Opening this tab also blurs
            // the still-focused Price cell above, committing it before
            // Save (odoo-development-ui-test, patterns.md §C Jebakan 2).
            {
                content: "Open the Accounting tab",
                trigger: ".o_notebook .nav-link:contains(Accounting)",
            },
            {
                content: "Accounting tab is displayed",
                trigger: ".o_form_label:contains(Journal)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 7 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Post-Condition — A new record is created in Draft status.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/employee_business_trip/04-confirm.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripsList(), [
            // Flow 2 — Open the record to confirm.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour EBT Confirm Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
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
                    // Assertion only; do not trigger the default click.
                },
            },
            // Negative (visible): the Confirm button is no longer shown
            // once the record left Draft.
            {
                content: "The Confirm button is no longer shown",
                trigger:
                    ".o_statusbar_buttons:not(:has(button[name='action_confirm']:visible))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/employee_business_trip/05-approve.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripsList(), [
            // Flow 2 — Open the record to approve.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour EBT Approve Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
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

            // Post-Condition (all approval levels fulfilled) — status
            // changes to In Progress. The fixture has one Per Diem line
            // (Keputusan Desain, issue open-synergy/opnsynid-hr-expense#132)
            // so the post_open_action accounting entry hook sets move_id,
            // which keeps the record In Progress instead of the no-line
            // branch auto-finishing it to Done -- that branch raises a
            // UserError instead (tracked separately in issue #149, out of
            // scope here).
            {
                content: "Status is In Progress",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/employee_business_trip/10-cancel.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripsList(), [
            // Flow 2 — Open the record to cancel.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour EBT Cancel Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Cancel button. It is a `type="action"`
            // button, so its `name` attribute is a numeric action id in
            // the DOM; target it by label instead (odoo-development-ui-test,
            // selectors.md §4).
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — In the wizard that appears, select the
            // Cancellation Reason.
            {
                // Wizard: do not prefix the trigger with `.modal`
                // (odoo-development-ui-test, patterns.md §H).
                content: "The Select Cancel Reason wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                // The wizard renders `cancel_reason_id` with
                // `widget="radio"` (base_select_cancel_reason_views.xml),
                // not the default many2one autocomplete -- select the
                // matching radio item by its label text.
                content: "Select the Cancellation Reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(Tour EBT Cancel Reason) input",
            },

            // Flow 5 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // Flow 6 — Click OK on the confirmation dialog. The wizard's
            // Confirm button carries confirm="Are you sure?" (mixin
            // ssi_transaction_cancel_mixin), which
            // docs/employee_business_trip/10-cancel.md was missing --
            // added there as step 6 to keep the IK the accurate source of
            // truth (odoo-development-ui-test, patterns.md §G), same as
            // the existing fix in docs/hr_reimbursement/10-cancel.md
            // (issue open-synergy/opnsynid-hr-expense#130). This second
            // dialog stacks on top of the wizard; 14.0 scopes the trigger
            // search to the topmost visible modal, so the selector below
            // resolves to it automatically.
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
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/employee_business_trip/02-edit.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripsList(), [
            // Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour EBT Edit Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Edit button. 14.0 only: a record that
            // already exists opens readonly (odoo-development-ui-test,
            // patterns.md §E).
            {
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 5 — Inline Action: click Compute Tax to recompute the
            // Taxes table from the Per Diem line's tax (the fixture's
            // Per Diem line already has one tax selected). IK step 5
            // marks this "Optionally" -- run it here, on the still-clean
            // record, so its own implicit save (Odoo 14 `type="object"`
            // buttons always save-then-execute-then-reload, see
            // form_controller.js `_onButtonClicked` /
            // basic_controller.js `_saveRecord`) has nothing to persist
            // and completes as a cheap no-write round trip.
            {
                content: "Open the Accounting tab",
                trigger: ".o_notebook .nav-link:contains(Accounting)",
            },
            {
                content: "Click the Compute Tax button",
                trigger: ".o_form_view button[name='action_compute_tax']",
            },
            {
                // Gate: Odoo 14 disables a `type="object"` button
                // synchronously on click and only re-enables it once its
                // full save + call_button + reload cycle lands
                // (odoo-development-ui-test, patterns.md §P) --
                // `:enabled` is therefore impossible while the cycle is
                // still running.
                content: "Compute Tax finished",
                trigger: "button[name='action_compute_tax']:enabled",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 4 — Change the required fields: switch Type to a
            // value different from the fixture's, so the Post-Condition
            // reopen-and-read below actually proves the change landed
            // (odoo-development-ui-test, patterns.md §L). Done *after*
            // Compute Tax so the explicit Save below is the only save
            // with real changes to persist -- chaining two back-to-back
            // save+reload cycles (Compute Tax's implicit one immediately
            // followed by this explicit one) was observed in CI to leave
            // the form stuck in edit mode indefinitely (reproduced with
            // a 30s wait, well above the tour engine's 10s default), a
            // known class of Odoo 14 client race between overlapping
            // reloads; not chaining them removes the race instead of
            // papering over it with a longer timeout.
            {
                content: "Select a different Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text Tour EBT Edit Type 2",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour EBT Edit Type 2)",
                in_modal: false,
            },

            // Flow 6 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Post-Condition — The record is updated with the new
            // values. Reading a many2one immediately after selecting it
            // is unreliable (odoo-development-ui-test, patterns.md §L):
            // go back to the list and reopen the record, which always
            // renders read-only at 14.0, to read a genuine text node.
            {
                content: "Go back to the list",
                trigger: ".breadcrumb-item:not(.active):contains('Business Trips')",
            },
            {
                content: "Reopen the record",
                trigger:
                    ".o_data_row:contains(Tour EBT Edit Employee) .o_data_cell:first",
            },
            {
                content: "Type shows the new value",
                trigger:
                    ".o_form_readonly .o_field_widget[name='type_id']:contains('Tour EBT Edit Type 2')",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/employee_business_trip/03-delete.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripsList(), [
            // Flow 2 — Select the record to delete (check the checkbox).
            {
                content: "Select the record to delete",
                trigger:
                    ".o_data_row:contains(Tour EBT Delete Employee) .o_list_record_selector input",
                extra_trigger: ".o_list_view",
                run: "click",
            },

            // Flow 3 — Click Action > Delete.
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
                // 14.0: the Action dropdown is an Owl component that
                // does not always open on a synthetic click
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

            // Post-Condition — The selected record is permanently
            // removed from the system.
            {
                content: "Record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(Tour EBT Delete Employee)))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/employee_business_trip/06-reject.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripsList(), [
            // Flow 2 — Open the record to reject.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour EBT Reject Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
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
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/employee_business_trip/09-done.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_done",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripsList(), [
            // Flow — the transition to Done is automatic
            // (base.automation `employee_business_trip_ready_2_done`);
            // there is no button to drive it from the UI. The fixture
            // is already Done before this tour starts, reached in
            // Python exactly as the automation would run it
            // (odoo-development-ui-test, scope-and-boundaries.md §1
            // aturan 6). This tour only opens the record and observes
            // the result.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour EBT Done Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Post-Condition — Status is Done.
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/employee_business_trip/12-restart.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripsList(), [
            // Flow 2 — Open the record to restart.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour EBT Restart Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Restart button.
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog. `action_restart`
            // carries `confirm="Restart data. Are you sure?"`, missing from
            // the original IK text -- added here as the corrected IK Flow
            // (odoo-development-ui-test, patterns.md §G names this exact
            // button as the canonical example of the gap).
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
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/employee_business_trip/13-reset-number.md
    tour.register(
        "ssi_employee_business_trip_employee_business_trip_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(openBusinessTripsList(), [
            // Flow 2 — Open the record whose document number will be
            // reset.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour EBT Reset Number Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
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
            // document number. Are you sure?"`, missing from the
            // original IK text -- added here as the corrected IK Flow
            // (odoo-development-ui-test, patterns.md §G).
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Document number returns to "/" (it is
            // already "/" on this Draft record). `name` field stores
            // "/", but `MixinTransaction.name_get` (ssi_transaction_mixin,
            // mixin_transaction.py) renders it as "*<id>" whenever the
            // stored number is "/" -- the literal "/" never appears in
            // the readonly display_name widget, so the visible fact
            // checked here is that the action completes and the
            // read-only form still shows the "*<id>" placeholder, not a
            // new error.
            {
                content: 'Document number is still "/" (shown as "*<id>")',
                trigger:
                    ".o_form_view .o_field_widget[name='display_name']:contains('*')",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );
});
